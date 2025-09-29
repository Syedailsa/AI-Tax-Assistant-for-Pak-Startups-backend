import requests
from bs4 import BeautifulSoup

def scrape_page(url: str) -> str:
    """Scrape all visible text from a webpage."""
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts and styles
    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    return text.strip()

if __name__ == "__main__":
    url = "https://www.startup.pk/how-to-handle-taxes-in-pakistan-as-a-startup-and-freelancer-2025/"
    scraped_text = scrape_page(url)
    print(scraped_text[:1000])  # preview first 1000 chars
