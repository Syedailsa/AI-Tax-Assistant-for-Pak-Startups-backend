import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone
from urllib.parse import urlparse

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Init clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "tax-agent-index"
index = pc.Index(index_name)

# Step 1: Scrape website
url = "https://fbr.gov.pk/income-tax-basics/51147/61148"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Get only visible text (basic)
text = " ".join([p.get_text() for p in soup.find_all("p")])

# Split into chunks (optional: better for long pages)
chunks = [text[i:i+500] for i in range(0, len(text), 500)]

# ✅ Make IDs unique per website page (domain + slug)
parsed = urlparse(url)
domain = parsed.netloc.replace(".", "-")
slug = parsed.path.strip("/").replace("/", "-") or "root"  # fallback if path is empty

# Step 2: Generate embeddings and upsert
for i, chunk in enumerate(chunks):
    embedding = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=chunk
    ).data[0].embedding

    index.upsert(vectors=[{
        "id": f"{domain}-{slug}-doc-{i}",   # ✅ unique per page
        "values": embedding,
        "metadata": {
            "text": chunk,
            "source": url
        }
    }])

print("✅ Website content embedded into Pinecone successfully without overwriting old data!")
