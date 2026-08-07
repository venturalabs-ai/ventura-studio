#!/usr/bin/env python3
"""Validate configured AI providers without printing credentials.

Providers:
- GitHub Models (uses GITHUB_TOKEN in Actions)
- Google Gemini
- Groq
- Mistral

Only provider name, HTTP status category and a short sanitized result are printed.
No API key/token value is ever logged.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass

TIMEOUT = 20
PROMPT = "Reply with exactly: VENTURA_OK"


@dataclass
class Result:
    provider: str
    configured: bool
    ok: bool
    detail: str


def post_json(url: str, headers: dict[str, str], payload: dict) -> tuple[int, dict]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"error": "HTTP error"}
        return exc.code, parsed


def github_models() -> Result:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return Result("github-models", False, False, "GITHUB_TOKEN not configured")
    status, body = post_json(
        "https://models.github.ai/inference/chat/completions",
        {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2026-03-10",
        },
        {
            "model": os.getenv("GITHUB_MODELS_MODEL", "openai/gpt-4.1-mini"),
            "messages": [{"role": "user", "content": PROMPT}],
            "max_tokens": 20,
            "temperature": 0,
        },
    )
    text = (((body.get("choices") or [{}])[0].get("message") or {}).get("content") or "")
    return Result("github-models", True, status == 200 and "VENTURA_OK" in text, f"HTTP {status}")


def gemini() -> Result:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return Result("gemini", False, False, "secret not configured")
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    status, body = post_json(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        {"x-goog-api-key": key, "Content-Type": "application/json"},
        {"contents": [{"parts": [{"text": PROMPT}]}], "generationConfig": {"temperature": 0, "maxOutputTokens": 20}},
    )
    candidates = body.get("candidates") or []
    text = ""
    if candidates:
        parts = ((candidates[0].get("content") or {}).get("parts") or [])
        text = " ".join(str(p.get("text", "")) for p in parts)
    return Result("gemini", True, status == 200 and "VENTURA_OK" in text, f"HTTP {status}")


def openai_compatible(provider: str, key_env: str, url: str, model_env: str, default_model: str) -> Result:
    key = os.getenv(key_env)
    if not key:
        return Result(provider, False, False, "secret not configured")
    status, body = post_json(
        url,
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        {
            "model": os.getenv(model_env, default_model),
            "messages": [{"role": "user", "content": PROMPT}],
            "max_tokens": 20,
            "temperature": 0,
        },
    )
    text = (((body.get("choices") or [{}])[0].get("message") or {}).get("content") or "")
    return Result(provider, True, status == 200 and "VENTURA_OK" in text, f"HTTP {status}")


def main() -> int:
    results = [
        github_models(),
        gemini(),
        openai_compatible(
            "groq",
            "GROQ_API_KEY",
            "https://api.groq.com/openai/v1/chat/completions",
            "GROQ_MODEL",
            "llama-3.3-70b-versatile",
        ),
        openai_compatible(
            "mistral",
            "MISTRAL_API_KEY",
            "https://api.mistral.ai/v1/chat/completions",
            "MISTRAL_MODEL",
            "mistral-small-latest",
        ),
    ]

    print("Ventura AI Provider Validation")
    print("provider          configured   valid   detail")
    print("------------------------------------------------")
    for r in results:
        print(f"{r.provider:<17} {str(r.configured):<12} {str(r.ok):<7} {r.detail}")

    configured = [r for r in results if r.configured]
    valid = [r for r in configured if r.ok]
    print(f"\nConfigured: {len(configured)} | Valid: {len(valid)}")

    # At least one working provider is mandatory. Optional configured providers
    # must also validate; a broken configured key must not be silently ignored.
    if not valid:
        print("ERROR: no working AI provider", file=sys.stderr)
        return 1
    broken = [r.provider for r in configured if not r.ok]
    if broken:
        print("ERROR: configured provider(s) failed validation: " + ", ".join(broken), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
