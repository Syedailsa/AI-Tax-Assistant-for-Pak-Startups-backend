import os
from agents import Agent, Runner, function_tool, ModelSettings, RunConfig
from agents import AsyncOpenAI, OpenAIChatCompletionsModel   
from pinecone import Pinecone
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Init clients
pc = Pinecone(api_key=PINECONE_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Pinecone index
INDEX_NAME = "tax-agent-index"
index = pc.Index(name=INDEX_NAME)

# Embedding model (OpenAI for Pinecone search)
EMBED_MODEL = "text-embedding-3-small"


def get_embedding(text: str):
    """Use OpenAI to embed query text"""
    resp = openai_client.embeddings.create(
        model=EMBED_MODEL,
        input=text
    )
    return resp.data[0].embedding


@function_tool
def retrieve_context(query: str) -> str:
    """Look up relevant tax info from Pinecone given a query"""
    embedding = get_embedding(query)
    results = index.query(vector=embedding, top_k=3, include_metadata=True)

    if not results["matches"]:
        return "Sorry, currently we dont know about the matter."

    context = "\n".join([m["metadata"]["text"] for m in results["matches"]])
    return context


# Setup Gemini as an OpenAI-compatible client
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Use Gemini model with OpenAI wrapper
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",   
    openai_client=external_client
)

# Configure run
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Defining the Agent with Gemini model for cost effeciency
agent = Agent(
    name="Tax Agent",
    instructions=(
        "You are a Tax Education Assistant for freelancers and students in Pakistan. "
        "You must remember the user's previous questions and your own answers within the conversation. "
        "Use the retrieve_context tool for factual tax information, and answer follow-ups naturally. "
        "If you’re unsure, politely say so."
        "If context is missing, still try to answer politely."
    ),
    tools=[retrieve_context],
    model=model,
    model_settings=ModelSettings(
        temperature=0.3,
        max_tokens=1024
    )
)

if __name__ == "__main__":
    # Simple logs to test the agent
    print("🤖 Tax Agent (Gemini) running...\n")
    while True:
        user_input = input("Ask a tax question (or type 'exit'): ")
        if user_input.lower() == "exit":
            break
        try:
            result = Runner.run_sync(agent, user_input, run_config=config)   
            print(f"\n📘 {result.final_output}\n")
        except Exception as e:
            print(f"Error getting response: {e}")
