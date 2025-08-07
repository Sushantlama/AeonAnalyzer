from datetime import datetime
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
from scraper import get_essay_content
from ai_analysis import analyze_essay
app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/essay-content")
def fetch_essay(url: str = Query(..., description="Aeon essay URL")):
    """
    Endpoint to fetch Aeon essay content from a URL.
    """
    try:
        essay_data = get_essay_content(url)
        if not essay_data:
            return JSONResponse(
                status_code=400,
                content={"error": "Failed to fetch essay. Please verify the URL."}
            )
        return essay_data

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Unexpected error while fetching essay: {str(e)}"}
        )

@app.get("/analyze-essay")
def analyze(url: str = Query(..., description="Aeon essay URL")):
    """
    Endpoint to fetch and analyze Aeon essay.
    """
    try:
        essay_data = get_essay_content(url)
        if not essay_data:
            return JSONResponse(
                status_code=400,
                content={"error": "Failed to fetch essay for analysis."}
            )

        # Strip HTML to plain text
        full_text = BeautifulSoup(essay_data['content'], "html.parser").get_text()

        # Run Gemini analysis
        result = analyze_essay(full_text)

        # Handle Gemini errors gracefully
        if "error" in result:
            return JSONResponse(
                status_code=500,
                content={"error": result["error"], "debug": result.get("raw_response", "")}
            )

        return result

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Unexpected error during analysis: {str(e)}"}
        )
