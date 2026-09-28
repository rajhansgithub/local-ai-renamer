import re
import string
from typing import List

# Common filler phrases from vision models to strip out
FILLER_PREFIXES = [
    r"^a photo of\b",
    r"^a photograph of\b",
    r"^an image of\b",
    r"^a picture of\b",
    r"^a close up of\b",
    r"^a close-up of\b",
    r"^a shot of\b",
    r"^a view of\b",
    r"^there is a\b",
    r"^there are\b",
    r"^an illustration of\b",
    r"^a drawing of\b",
    r"^a graphic of\b",
    r"^a capture of\b",
    r"^an aerial view of\b",
    r"^a portrait of\b",
]

# Words that can be safely filtered if word count exceeds target,
# or to make filenames cleaner and more punchy
STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", 
    "of", "with", "by", "from", "is", "are", "was", "were", "it", "its",
    "this", "that", "these", "those", "some", "very"
}

def clean_caption(caption: str) -> str:
    """Removes filler prefixes and cleans up the raw caption."""
    text = caption.strip().lower()
    
    # Strip common filler prefixes
    for prefix in FILLER_PREFIXES:
        text = re.sub(prefix, "", text, flags=re.IGNORECASE).strip()
    
    # Replace punctuation with spaces
    text = re.sub(r"[^\w\s-]", " ", text)
    # Collapse consecutive whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

def caption_to_filename(
    caption: str, 
    min_words: int = 1, 
    max_words: int = 5, 
    separator: str = "_",
    lowercase: bool = True
) -> str:
    """
    Converts a descriptive caption into a clean, 1-to-5 word filename with underscores.
    Example:
        'A photo of a cute orange cat sleeping on a sofa'
        -> 'cute_orange_cat_sleeping_sofa' (or 'orange_cat_sleeping_sofa')
    """
    cleaned = clean_caption(caption)
    raw_words = cleaned.split()
    
    if not raw_words:
        return "renamed_image"

    # Filter stop words if we have more than max_words,
    # but keep them if removing leaves fewer than min_words
    content_words = [w for w in raw_words if w not in STOP_WORDS]
    
    if len(content_words) >= min_words:
        chosen_words = content_words[:max_words]
    else:
        # If stop word filtering removed too much, fallback to original words
        chosen_words = raw_words[:max_words]

    # Ensure length is clamped between min_words and max_words
    if len(chosen_words) > max_words:
        chosen_words = chosen_words[:max_words]
    elif len(chosen_words) < min_words and len(raw_words) >= min_words:
        chosen_words = raw_words[:min_words]

    # Sanitize each word to contain only alphanumeric or hyphen
    sanitized_words: List[str] = []
    for word in chosen_words:
        w = re.sub(r"[^\w-]", "", word)
        if w:
            sanitized_words.append(w.lower() if lowercase else w)

    if not sanitized_words:
        return "renamed_image"

    result = separator.join(sanitized_words)
    # Remove any duplicate separators or leading/trailing separators
    result = re.sub(rf"\{separator}+", separator, result).strip(separator)
    
    # Final Windows filename safety check (no reserved device names like CON, PRN, etc.)
    reserved_names = {"con", "prn", "aux", "nul", "com1", "com2", "com3", "com4", 
                      "com5", "com6", "com7", "com8", "com9", "lpt1", "lpt2", 
                      "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9"}
    if result.lower() in reserved_names:
        result = f"{result}_img"

    return result or "renamed_image"
