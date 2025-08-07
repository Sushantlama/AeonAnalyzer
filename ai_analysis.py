import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini model (1.5 Flash)
model = genai.GenerativeModel("gemini-1.5-flash")


def analyze_essay(text: str) -> dict:
    """
    Analyzes a given Aeon essay using Gemini and returns structured breakdown.

    Args:
        text (str): Raw HTML or plain text of the essay.

    Returns:
        dict: Structured JSON with summary, classification, etc.
    """
    prompt = f"""
    You are a CAT exam professor helping a serious CAT aspirant understand Aeon essays for VARC preparation.

    Given the following Aeon essay, provide a detailed academic breakdown in the following JSON format:

    {{
      "summary": "A concise overall summary of the essay.",
      "genre": "The type or domain of the essay (e.g., philosophy, psychology, science, history, etc.)",
      "classification": "Factual, Opinion, Analytical, Narrative, or Philosophical",
      "main_point": "The central idea or thesis of the essay.",
      "supporting_arguments": ["List of key arguments or evidence supporting the main point"],
      "contrasting_views": ["List of any opposing viewpoints or critiques mentioned"],
      "paragraph_summaries": ["One-line summary for each paragraph, in order"]
    }}

    Use clear, formal English. Do not include any explanation or notes. Only return pure JSON.

    Essay content:
    {text}
    """

    response_text = ""
    try:
        # Generate response from Gemini
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        # Strip ```json or other markdown formatting if present
        cleaned_text = re.sub(r"^```json\s*|\s*```$", "", response_text, flags=re.DOTALL).strip()

        # Try parsing to JSON
        return json.loads(cleaned_text)

    except json.JSONDecodeError as e:
        return {
            "error": f"Gemini response was not valid JSON: {str(e)}",
            "raw_response": response_text or "No response text"
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "raw_response": response_text or "No response text"
        }
