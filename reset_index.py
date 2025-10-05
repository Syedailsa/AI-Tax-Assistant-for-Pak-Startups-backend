from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "tax-agent-index"  # <-- use your index name here

# Delete old index if it exists
if index_name in pc.list_indexes().names():
    print(f"Deleting old index: {index_name}")
    pc.delete_index(index_name)

# Create new index with correct dimension
print(f"Creating new index: {index_name}")
pc.create_index(
    name=index_name,
    dimension=1536,  
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)

print("✅ Index recreated successfully!")