from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .llm_client import LLMClient
from .provider_store import ProviderStore

app = FastAPI(title="Aide - Backend (Phase 2)")

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


class SessionContext(BaseModel):
    hint_level: str | None = "guided"
    challenge_context: str | None = None
    mode: str | None = "general"
    session_history: list[dict] | None = None
    session_summary: str | None = None
    session_id: str | None = None


class ChatRequest(BaseModel):
    message: str
    context: SessionContext | None = None
    provider: ProviderConfig | None = None


class ChatResponse(BaseModel):
    reply: str
    source: str | None = None


llm = LLMClient()
store = ProviderStore()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    context = req.context or SessionContext()
    reply = await llm.generate_reply(
        req.message,
        provider=req.provider,
        hint_level=context.hint_level,
        challenge_context=context.challenge_context,
        mode=context.mode,
        session_history=context.session_history,
        session_summary=context.session_summary,
    )
    return ChatResponse(reply=reply, source="mentor")


class ProviderSave(BaseModel):
    name: str
    provider: str
    api_key: str | None = None
    model: str | None = None
    base_url: str | None = None
    temperature: float | None = 0.2


@app.get("/providers")
async def list_providers():
    return store.list_providers()


@app.post("/providers")
async def save_provider(p: ProviderSave):
    metadata = {"provider": p.provider, "model": p.model, "base_url": p.base_url, "temperature": p.temperature}
    store.save_provider(p.name, metadata, api_key=p.api_key)
    return {"status": "ok", "name": p.name}


@app.get("/providers/{name}")
async def get_provider(name: str):
    prov = store.get_provider(name)
    if not prov:
        return {"error": "not found"}, 404
    # hide API key in this endpoint for safety
    prov_copy = {**prov}
    prov_copy["api_key"] = True if prov_copy.get("api_key") else False
    return prov_copy


@app.delete("/providers/{name}")
async def delete_provider(name: str):
    ok = store.delete_provider(name)
    return {"status": "deleted" if ok else "not found"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("aide.app.backend.main:app", host="127.0.0.1", port=8000, reload=True)
