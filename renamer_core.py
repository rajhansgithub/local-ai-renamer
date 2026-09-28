import os
import sys
import traceback
from typing import List, Tuple, Dict, Any, Callable, Optional

from config import load_config
from sanitizer import caption_to_filename
from engine_local import LocalVisionEngine
from engine_api import GeminiVisionEngine

def scan_images(
    folder_path: str, 
    recursive: bool = True, 
    supported_extensions: Optional[List[str]] = None
) -> List[str]:
    """
    Recursively scans folder_path for image files matching supported_extensions.
    Ignores non-image files entirely.
    """
    if supported_extensions is None:
        supported_extensions = [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"]
    
    ext_set = {ext.lower() for ext in supported_extensions}
    image_paths: List[str] = []

    if not os.path.exists(folder_path):
        return []

    if recursive:
        for root, _, files in os.walk(folder_path):
            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in ext_set:
                    image_paths.append(os.path.join(root, file))
    else:
        for item in os.listdir(folder_path):
            full_path = os.path.join(folder_path, item)
            if os.path.isfile(full_path):
                _, ext = os.path.splitext(item)
                if ext.lower() in ext_set:
                    image_paths.append(full_path)

    return image_paths

def get_unique_filename(directory: str, base_name: str, ext: str, original_path: str) -> Tuple[str, str]:
    """
    Resolves filename collisions in the target directory by appending _1, _2, etc.
    Returns (new_filename, full_target_path).
    """
    candidate_filename = f"{base_name}{ext}"
    candidate_path = os.path.join(directory, candidate_filename)

    # If the file already has this exact name, no collision
    if os.path.normpath(candidate_path) == os.path.normpath(original_path):
        return candidate_filename, candidate_path

    # If candidate doesn't exist, use it
    if not os.path.exists(candidate_path):
        return candidate_filename, candidate_path

    # Otherwise append counter
    counter = 1
    while True:
        candidate_filename = f"{base_name}_{counter}{ext}"
        candidate_path = os.path.join(directory, candidate_filename)
        if os.path.normpath(candidate_path) == os.path.normpath(original_path) or not os.path.exists(candidate_path):
            return candidate_filename, candidate_path
        counter += 1

def run_rename_process(
    folder_path: str,
    config: Optional[Dict[str, Any]] = None,
    on_status: Optional[Callable[[str], None]] = None,
    on_progress: Optional[Callable[[int, int, str], None]] = None,
    on_image_processed: Optional[Callable[[str, str, str, Optional[Any]], None]] = None,
    on_log: Optional[Callable[[str, str], None]] = None,
    is_cancelled: Optional[Callable[[], bool]] = None
) -> Dict[str, Any]:
    """
    Executes the full image renaming pipeline:
    1. Discovers image files (recursively or flat). Ignores non-image files.
    2. Only loads AI model into memory when images exist and renaming starts.
    3. Infers context, generates 1-to-5 word filenames with underscores.
    4. Handles duplicates safely.
    5. Frees AI model from memory immediately upon completion or cancellation.
    """
    if config is None:
        config = load_config()

    def log(msg: str, level: str = "INFO"):
        if on_log:
            on_log(msg, level)
        else:
            print(f"[{level}] {msg}")

    def update_status(msg: str):
        if on_status:
            on_status(msg)
        log(msg, "STATUS")

    stats = {
        "total_images": 0,
        "renamed": 0,
        "skipped": 0,
        "errors": 0,
        "cancelled": False
    }

    update_status("Scanning directory for image files...")
    images = scan_images(
        folder_path,
        recursive=config.get("recursive", True),
        supported_extensions=config.get("supported_extensions")
    )

    stats["total_images"] = len(images)

    if not images:
        update_status("No supported image files found in folder.")
        log("No images found to rename. Non-image files were left untouched.", "INFO")
        return stats

    log(f"Found {len(images)} image(s) to process in: {folder_path}", "INFO")

    # Select AI engine
    engine_type = config.get("engine", "local_florence2")
    engine = None

    if engine_type == "api_gemini":
        engine = GeminiVisionEngine(
            api_key=config.get("gemini_api_key", ""),
            model_name="gemini-2.0-flash"
        )
    else:
        engine = LocalVisionEngine(
            model_id=config.get("local_model_id", "microsoft/Florence-2-base"),
            device=config.get("device", "cuda")
        )

    # Strict Memory Management: Load model now, guarantee unload in finally block
    try:
        engine.load(status_callback=update_status)

        min_words = int(config.get("min_words", 1))
        max_words = int(config.get("max_words", 5))
        separator = config.get("word_separator", "_")
        lowercase = bool(config.get("lowercase", True))

        for idx, img_path in enumerate(images):
            if is_cancelled and is_cancelled():
                stats["cancelled"] = True
                log("Renaming process was cancelled by the user.", "WARNING")
                update_status("Cancelled by user.")
                break

            current_num = idx + 1
            original_dir = os.path.dirname(img_path)
            original_filename = os.path.basename(img_path)
            _, ext = os.path.splitext(original_filename)

            if on_progress:
                on_progress(current_num, len(images), original_filename)

            update_status(f"Processing ({current_num}/{len(images)}): {original_filename}")

            thumbnail = None
            try:
                # Open thumbnail for GUI display
                try:
                    from PIL import Image
                    with Image.open(img_path) as thumb_img:
                        thumb = thumb_img.copy()
                        thumb.thumbnail((120, 120))
                        thumbnail = thumb
                except Exception:
                    thumbnail = None

                # Generate AI description
                raw_description = engine.describe_image(img_path)
                log(f"[{original_filename}] AI Description: '{raw_description}'", "DEBUG")

                # Sanitize to 1-to-5 words
                new_base_name = caption_to_filename(
                    raw_description,
                    min_words=min_words,
                    max_words=max_words,
                    separator=separator,
                    lowercase=lowercase
                )

                # Ensure extension preservation (lowercased)
                clean_ext = ext.lower()
                new_filename, target_path = get_unique_filename(
                    original_dir, new_base_name, clean_ext, img_path
                )

                if os.path.normpath(img_path) == os.path.normpath(target_path):
                    log(f"Skipped (already named correctly): {original_filename}", "INFO")
                    stats["skipped"] += 1
                    if on_image_processed:
                        on_image_processed(original_filename, original_filename, img_path, thumbnail)
                    continue

                # Execute rename
                os.rename(img_path, target_path)
                log(f"Renamed: '{original_filename}' -> '{new_filename}'", "SUCCESS")
                stats["renamed"] += 1

                if on_image_processed:
                    on_image_processed(original_filename, new_filename, target_path, thumbnail)

            except Exception as e:
                stats["errors"] += 1
                error_msg = f"Failed to rename {original_filename}: {str(e)}"
                log(error_msg, "ERROR")
                log(traceback.format_exc(), "DEBUG")

    finally:
        # Crucial Requirement: AI model is freed up right after it is done renaming
        update_status("Freeing AI model from memory...")
        try:
            if engine is not None:
                engine.unload(status_callback=update_status)
        except Exception as e:
            log(f"Error while freeing model memory: {e}", "WARNING")

    summary = (
        f"Completed: Renamed {stats['renamed']} image(s), "
        f"Skipped {stats['skipped']}, Errors {stats['errors']}."
    )
    update_status(summary)
    log(summary, "INFO")
    return stats
