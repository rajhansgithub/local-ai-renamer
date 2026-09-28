import gc
import os
from typing import Optional

class LocalVisionEngine:
    """
    Local Vision Language Model (Florence-2 / Moondream).
    Strict lifecycle: Model is ONLY loaded when needed and completely freed when finished.
    """
    def __init__(self, model_id: str = "microsoft/Florence-2-base", device: str = "cuda"):
        self.model_id = model_id
        self.requested_device = device
        self.device = None
        self.model = None
        self.processor = None
        self.torch = None

    def load(self, status_callback=None):
        """Loads the vision model into GPU VRAM (or RAM if CPU)."""
        if self.model is not None:
            return  # Already loaded

        if status_callback:
            status_callback(f"Loading AI Vision Model ({self.model_id})...")

        import torch
        from transformers import AutoModelForCausalLM, AutoProcessor

        self.torch = torch

        # Determine best device
        if self.requested_device == "cuda" and torch.cuda.is_available():
            self.device = "cuda"
            torch_dtype = torch.float16
        else:
            self.device = "cpu"
            torch_dtype = torch.float32

        if status_callback:
            status_callback(f"Loading weights into {self.device.upper()} memory...")

        app_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(app_dir, "models")
        os.makedirs(models_dir, exist_ok=True)

        # Check if local folder models/Florence-2-base exists
        clean_name = self.model_id.replace("/", "--").split("--")[-1]
        local_subfolder = os.path.join(models_dir, clean_name)
        model_source = local_subfolder if os.path.exists(local_subfolder) else self.model_id

        self.processor = AutoProcessor.from_pretrained(
            model_source,
            cache_dir=models_dir,
            trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_source,
            cache_dir=models_dir,
            torch_dtype=torch_dtype, 
            trust_remote_code=True
        ).to(self.device)

        self.model.eval()

        if status_callback:
            status_callback(f"AI Model loaded into {self.device.upper()}. Ready for inference.")

    def describe_image(self, image_path: str, prompt_task: str = "<CAPTION>") -> str:
        """
        Runs vision inference on an image and returns a textual description.
        prompt_task can be '<CAPTION>' (short) or '<DETAILED_CAPTION>'.
        """
        if self.model is None or self.processor is None:
            raise RuntimeError("Model is not loaded. Call load() before running inference.")

        from PIL import Image
        with Image.open(image_path) as img:
            image = img.convert("RGB")

        inputs = self.processor(text=prompt_task, images=image, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        if self.device == "cuda":
            inputs["pixel_values"] = inputs["pixel_values"].to(self.torch.float16)

        with self.torch.inference_mode():
            generated_ids = self.model.generate(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                max_new_tokens=100,
                num_beams=3,
                do_sample=False
            )

        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
        parsed_answer = self.processor.post_process_generation(
            generated_text, 
            task=prompt_task, 
            image_size=(image.width, image.height)
        )
        
        # Florence-2 returns { '<CAPTION>': 'description text' }
        if isinstance(parsed_answer, dict) and prompt_task in parsed_answer:
            return str(parsed_answer[prompt_task])
        elif isinstance(parsed_answer, str):
            return parsed_answer
        return str(generated_text)

    def unload(self, status_callback=None):
        """
        Completely unloads the model from GPU VRAM and system RAM.
        Crucial requirement: frees up 100% of allocated AI memory.
        """
        if status_callback:
            status_callback("Unloading AI model and freeing GPU memory...")

        if self.model is not None:
            del self.model
            self.model = None

        if self.processor is not None:
            del self.processor
            self.processor = None

        # Force garbage collection
        gc.collect()

        # Free PyTorch CUDA cache
        if self.torch is not None and self.torch.cuda.is_available():
            self.torch.cuda.empty_cache()
            self.torch.cuda.ipc_collect()

        if status_callback:
            status_callback("GPU VRAM and system memory successfully freed.")

    def __enter__(self):
        self.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unload()
