import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from agents import Runner
import agent as agent_module 

app = FastAPI(title="Tax Agent API")

# Allow your Next.js origin (dev + prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ai-tax-assistant-for-pak-startups-f.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

API_KEY = os.getenv("CHAT_API_KEY")

@app.post("/api/chat")
async def chat(req: ChatRequest, authorization: str | None = Header(None)):

    if API_KEY:
        if authorization is None or authorization != f"Bearer {API_KEY}":
            raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        # only last 10 messages for memory
        last_messages = req.messages[-10:]

        # Combine conversation for context
        conversation = "\n".join(
            [f"{m.role}: {m.content}" for m in last_messages]
        )

        result = await Runner.run(
            agent_module.agent,
            conversation,
            run_config=getattr(agent_module, "config", None)
        )

        reply_text = getattr(result, "final_output", None) or getattr(result, "output_text", None) or str(result)

        return {"reply": reply_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
