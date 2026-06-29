import os
from typing import Optional

import httpx


class ProviderClient:
    def __init__(self, provider: str, api_key: str, model: str, base_url: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.base_url = base_url or self._default_base_url(provider)

    def _default_base_url(self, provider: str) -> str:
        return {
            "openai": "https://api.openai.com/v1/chat/completions",
            "groq": "https://api.groq.com/openai/v1/chat/completions",
            "claude": "https://api.anthropic.com/v1/messages",
            "gemini": "https://generativelanguage.googleapis.com/v1beta/models",
        }.get(provider, "")

    async def ask(self, prompt: str) -> str:
        if self.provider == "openai":
            return await self._openai(prompt)
        if self.provider == "groq":
            return await self._openai(prompt)
        if self.provider == "claude":
            return await self._claude(prompt)
        if self.provider == "gemini":
            return await self._gemini(prompt)
        return "Unsupported provider"

    async def _openai(self, prompt: str) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": self.model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.2}
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(self.base_url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            choices = data.get("choices") or []
            if choices:
                return choices[0].get("message", {}).get("content") or choices[0].get("text") or "(empty response)"
            return str(data)

    async def _claude(self, prompt: str) -> str:
        headers = {"x-api-key": self.api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
        payload = {"model": self.model, "max_tokens": 500, "messages": [{"role": "user", "content": prompt}]}
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(self.base_url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            content = data.get("content") or []
            if content and isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("text"):
                        return item["text"]
            return str(data)

    async def _gemini(self, prompt: str) -> str:
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            candidates = data.get("candidates") or []
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text") or "(empty response)"
            return str(data)
