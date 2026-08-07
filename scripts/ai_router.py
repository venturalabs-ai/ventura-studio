#!/usr/bin/env python3
"""Small multi-provider AI router with secret-by-environment configuration.

No credential is accepted as a function argument or stored in source. Providers
are tried in priority order and failures are returned without credential data.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass

TIMEOUT = 30


@dataclass(frozen=True)
class ProviderResponse:
    provider: str
    model: str
    text: str


class ProviderError(RuntimeError):
    pass


def _post(url: str, headers: dict[str, str], payload: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        # Never echo server bodies: they can contain request metadata.
        raise ProviderError(f"HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise ProviderError("network error") from exc


def _github(prompt: str) -> ProviderResponse:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ProviderError("not configured")
    model = os.getenv("GITHUB_MODELS_MODEL", "openai/gpt-4.1-mini")
    data = _post(
        "https://models.github.ai/inference/chat/completions",
        {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2026-03-10",
        },
        {"model": model, "messages": [{"role": "user", "content": prompt}]},
    )
    text = (((data.get("choices") or [{}])[0].get("message") or {}).get("content") or "")
    return ProviderResponse("github-models", model, text)


def _gemini(prompt: str) -> ProviderResponse:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ProviderError("not configured")
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    data = _post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        {"x-goog-api-key": key, "Content-Type": "application/json"},
        {"contents": [{"parts": [{"text": prompt}]}]},
    )
    candidates = data.get("candidates") or []
    parts = ((candidates[0].get("content") or {}).get("parts") or []) if candidates else []
    return ProviderResponse("gemini", model, " ".join(str(p.get("text", "")) for p in parts))


def _compatible(provider: str, env_name: str, url: str, model_env: str, default_model: str, prompt: str) -> ProviderResponse:
    key = os.getenv(env_name)
    if not key:
        raise ProviderError("not configured")
    model = os.getenv(model_env, default_model)
    data = _post(
        url,
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        {"model": model, "messages": [{"role": "user", "content": prompt}]},
    )
    text = (((data.get("choices") or [{}])[0].get("message") or {}).get("content") or "")
    return ProviderResponse(provider, model, text)


def generate(prompt: str, priority: tuple[str, ...] = ("github-models", "gemini", "groq", "mistral")) -> ProviderResponse:
    errors: list[str] = []
    for provider in priority:
        try:
            if provider == "github-models":
                return _github(prompt)
            if provider == "gemini":
                return _gemini(prompt)
            if provider == "groq":
                return _compatible("groq", "GROQ_API_KEY", "https://api.groq.com/openai/v1/chat/completions", "GROQ_MODEL", "llama-3.3-70b-versatile", prompt)
            if provider == "mistral":
                return _compatible("mistral", "MISTRAL_API_KEY", "https://api.mistral.ai/v1/chat/completions", "MISTRAL_MODEL", "mistral-small-latest", prompt)
            errors.append(f"{provider}: unknown provider")
        except ProviderError as exc:
            errors.append(f"{provider}: {exc}")
    raise ProviderError("all providers failed: " + "; ".join(errors))


if __name__ == "__main__":
    result = generate("Reply with exactly: VENTURA_OK")
    print(json.dumps({"provider": result.provider, "model": result.model, "ok": "VENTURA_OK" in result.text}))
