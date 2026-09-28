import os
import sys

def download_model(model_id: str = "microsoft/Florence-2-base", target_dir: str = ""):
    """
    Downloads the vision model weights directly into the local models directory.
    """
    app_dir = os.path.dirname(os.path.abspath(__file__))
    if not target_dir:
        clean_name = model_id.replace("/", "--").split("--")[-1]
        target_dir = os.path.join(app_dir, "models", clean_name)

    os.makedirs(target_dir, exist_ok=True)
    print(f"========================================================")
    print(f" Downloading Vision Model: {model_id}")
    print(f" Target Directory: {target_dir}")
    print(f"========================================================")
    print("Fetching processor and model weights (approx. 460 MB)...")

    try:
        from transformers import AutoModelForCausalLM, AutoProcessor
        
        processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
        processor.save_pretrained(target_dir)
        print("[1/2] Processor downloaded and saved.")

        model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
        model.save_pretrained(target_dir)
        print("[2/2] Model weights downloaded and saved.")

        print(f"\n[SUCCESS] Model successfully saved to:\n  {target_dir}")
        print("The tool will now load weights directly from this local folder.")
    except Exception as e:
        print(f"\n[Error] Failed to download model: {e}")
        sys.exit(1)

if __name__ == "__main__":
    model = sys.argv[1] if len(sys.argv) > 1 else "microsoft/Florence-2-base"
    download_model(model)
