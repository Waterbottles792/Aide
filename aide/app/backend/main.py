from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .llm_client import LLMClient
from .provider_store import ProviderStore
from .session_store import SessionStore

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
session_store = SessionStore()


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


@app.get("/sessions")
def list_sessions():
    return session_store.list_sessions()


@app.get("/sessions/{session_id}")
def get_session(session_id: str):
    session = session_store.get_session(session_id)
    if not session:
        return {"error": "not found"}, 404
    return session


class SessionSave(BaseModel):
    session_id: str | None = None
    name: str | None = 'Untitled session'
    summary: str | None = ''
    hint_level: str | None = 'guided'
    challenge_context: str | None = None
    mode: str | None = 'general'
    history: list[dict] | None = None


@app.post("/sessions")
def create_session(session: SessionSave):
    result = session_store.create_session(
        name=session.name or "Untitled session",
        summary=session.summary or "",
        hint_level=session.hint_level or "guided",
        challenge_context=session.challenge_context,
        mode=session.mode or "general",
        history=session.history or [],
    )
    return result


@app.put("/sessions/{session_id}")
def save_session(session_id: str, session: SessionSave):
    stored = session_store.get_session(session_id)
    if not stored:
        return {"error": "not found"}, 404
    session_data = {
        **stored,
        **{
            "name": session.name or stored.get("name", "Untitled session"),
            "summary": session.summary or stored.get("summary", ""),
            "hint_level": session.hint_level or stored.get("hint_level", "guided"),
            "challenge_context": session.challenge_context if session.challenge_context is not None else stored.get("challenge_context"),
            "mode": session.mode or stored.get("mode", "general"),
            "history": session.history or stored.get("history", []),
        },
        "session_id": session_id,
    }
    return session_store.save_session(session_data)


@app.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    ok = session_store.delete_session(session_id)
    return {"status": "deleted" if ok else "not found"}


class ProviderSave(BaseModel):
    name: str
    provider: str
    api_key: str | None = None
    model: str | None = None
    base_url: str | None = None
    temperature: float | None = 0.2


class SessionSave(BaseModel):
    session_id: str | None = None
    name: str | None = 'Untitled session'
    summary: str | None = ''
    hint_level: str | None = 'guided'
    challenge_context: str | None = None
    mode: str | None = 'general'
    history: list[dict] | None = None


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
