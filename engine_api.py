import os

class GeminiVisionEngine:
    """
    Cloud Gemini Vision API engine.
    Used if user prefers cloud inference or doesn't have local GPU PyTorch setup.
    """
    def __init__(self, api_key: str = "", model_name: str = "gemini-2.0-flash"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.model_name = model_name
        self.client = None

    def load(self, status_callback=None):
        if not self.api_key:
            raise ValueError(
                "Gemini API key is required when using the API engine. "
                "Please configure 'gemini_api_key' in config.json or set the GEMINI_API_KEY environment variable."
            )
        if status_callback:
            status_callback("Connecting to Gemini Vision API...")
            
        from google import genai
        self.client = genai.Client(api_key=self.api_key)

    def describe_image(self, image_path: str) -> str:
        if self.client is None:
            self.load()

        prompt = (
            "Provide a concise, 1 to 5 word description of the main subject or scene in this image. "
            "Do not include filler words like 'a photo of' or 'image showing'. "
            "Output only the concise description."
        )

        from PIL import Image
        with Image.open(image_path) as img:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt, img]
            )
            return response.text.strip() if response.text else "unnamed_image"

    def unload(self, status_callback=None):
        self.client = None
        if status_callback:
            status_callback("API session closed.")

    def __enter__(self):
        self.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unload()
