import requests
from bs4 import BeautifulSoup

def get_essay_content(url: str) -> dict | None:
    """
    Fetches the title, subheading, author, and main content of an Aeon essay.

    Args:
        url (str): Aeon essay URL.

    Returns:
        dict | None: Dictionary with metadata and content or None if fetch fails.
    """
    if not url.startswith("https://aeon.co/essays/"):
        return None

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        # --- Metadata Extraction ---
        meta_div = soup.find("div", class_="sc-1be6b0e7-3")

        title = meta_div.find("h2").get_text(strip=True) if meta_div and meta_div.find("h2") else "Title not found"
        subheading = meta_div.find("h1").get_text(strip=True) if meta_div and meta_div.find("h1") else "Subheading not found"

        author_tag = meta_div.find("p", class_="sc-1be6b0e7-5") if meta_div else None
        author = (
            author_tag.get_text(" ", strip=True).replace("+ BIO", "").strip()
            if author_tag else "Author not found"
        )

        # --- Main Content Extraction ---
        article_div = soup.find("div", id="article-content")
        if not article_div:
            return None

        content_html = ""
        for element in article_div.find_all(["p", "img"], recursive=True):
            if element.name == "p":
                text = element.get_text(strip=True)
                if text:
                    content_html += f"<p>{text}</p>\n"
            elif element.name == "img":
                img_url = element.get("src")
                if img_url:
                    if img_url.startswith("//"):
                        img_url = "https:" + img_url
                    elif img_url.startswith("/"):
                        img_url = "https://aeon.co" + img_url
                    content_html += f'<img src="{img_url}" style="max-width:100%; margin:10px 0;"/>\n'

        return {
            "title": title,
            "subheading": subheading,
            "author": author,
            "content": content_html or "<p>No content found.</p>"
        }

    except Exception as e:
        print(f"Error while scraping essay: {e}")
        return None
