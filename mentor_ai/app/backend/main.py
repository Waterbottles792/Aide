from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .llm_client import LLMClient

app = FastAPI(title="Mentor AI - Backend (Phase 1)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProviderConfig(BaseModel):
    provider: str
    api_key: str | None = None
    model: str | None = None
    base_url: str | None = None
    temperature: float | None = 0.2


class ChatRequest(BaseModel):
    message: str
    context: dict | None = None
    provider: ProviderConfig | None = None


class ChatResponse(BaseModel):
    reply: str
    source: str | None = None


llm = LLMClient()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # For Phase 1 we return a routed reply via the LLM client stub
    reply = await llm.generate_reply(req.message, provider=req.provider)
    return ChatResponse(reply=reply, source="stub")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("mentor_ai.app.backend.main:app", host="127.0.0.1", port=8000, reload=True)
