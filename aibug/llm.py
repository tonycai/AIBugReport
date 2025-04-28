"""
LLM integration for AIBugReport using Google Gemini Flash 2.0.
"""
import os
import json

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class LLMClient:
    """Client for interacting with Google Gemini Flash 2.0 via google-generativeai."""
    def __init__(self):
        if genai is None:
            raise ImportError("Please install the 'google-generativeai' package to use LLM features.")
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        # Default to Gemini Flash latest available model
        self.model = os.getenv("GOOGLE_API_MODEL", "gemini-1.5-flash-latest")
        genai.configure(api_key=self.api_key)

    def suggest(self, description: str) -> dict:
        """
        Send the bug description to the LLM and parse a JSON response with 'category' and 'severity'.
        """
        # Construct prompt for LLM
        prompt = (
            "Suggest a category and severity for the following bug description:\n"
            f"{description}\n"
            "Respond in strict JSON format with keys 'category' and 'severity'."
        )
        # Determine full model path
        model_name = (
            self.model
            if self.model.startswith("models/")
            else f"models/{self.model}"
        )
        # Initialize and call the LLM model
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        # Extract text from response
        text = getattr(response, 'text', None)
        if not text and hasattr(response, 'candidates'):
            text = response.candidates[0].output
        if not text:
            raise RuntimeError("Empty response from LLM")
        # Parse JSON response
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Fallback: simple parsing of 'key: value' lines
            category = None
            severity = None
            for line in text.splitlines():
                if ':' in line:
                    k, v = line.split(':', 1)
                    key = k.strip().lower()
                    val = v.strip()
                    if key == 'category':
                        category = val
                    elif key == 'severity':
                        severity = val
            return {'category': category, 'severity': severity}