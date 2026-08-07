#!/usr/bin/env python3
"""Validate AI providers without printing credentials.

GitHub Models is discovered dynamically from the live catalog so retired model
IDs do not break validation. External providers are validated only when their
repository secrets are configured.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass

TIMEOUT = 25
PROMPT = "Reply with exactly: VENTURA_OK"


@dataclass
class Result:
    provider: str
    configured: bool
    ok: bool
    detail: str


def request_json(method: str, url: str, headers: dict[str, str], payload: dict | None = None) -> tuple[int, object]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        # Do not print response bodies: provider errors can include request metadata.
        return exc.code, {}
    except urllib.error.URLError:
        return 0, {}


def github_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2026-03-10",
    }


def _lightweight_score(model_id: str) -> tuple[int, int, str]:
    name = model_id.lower()
    lightweight = 0 if any(x in name for x in ("nano", "mini", "small", "flash", "lite")) else 1
    dated = 1 if any(c.isdigit() for c in name) else 0
    return lightweight, dated, model_id


def github_models() -> list[Result]:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return [Result("github-models", False, False, "GITHUB_TOKEN not configured")]

    headers = github_headers(token)
    status, catalog = request_json("GET", "https://models.github.ai/catalog/models", headers)
    if status != 200 or not isinstance(catalog, list):
        return [Result("github-models", True, False, f"catalog HTTP {status}")]

    # Validate distinct model publishers through the same protected GitHub Models
    # credential. Prefixes are intentionally broad; actual IDs come from catalog.
    prefixes = (
        ("github-models/openai", ("openai/",)),
        ("github-models/meta", ("meta/", "meta-llama/")),
        ("github-models/mistral", ("mistral-ai/", "mistral/")),
        ("github-models/deepseek", ("deepseek/",)),
    )
    available_ids = [str(item.get("id", "")) for item in catalog if isinstance(item, dict) and item.get("id")]
    results: list[Result] = []

    for label, allowed_prefixes in prefixes:
        candidates = [m for m in available_ids if m.lower().startswith(tuple(p.lower() for p in allowed_prefixes))]
        candidates.sort(key=_lightweight_score)
        if not candidates:
            continue

        success = False
        last_status = 0
        selected = ""
        for model in candidates[:4]:
            last_status, body = request_json(
                "POST",
                "https://models.github.ai/inference/chat/completions",
                headers,
                {
                    "model": model,
                    "messages": [{"role": "user", "content": PROMPT}],
                    "max_tokens": 20,
                    "temperature": 0,
                },
            )
            text = ""
            if isinstance(body, dict):
                choices = body.get("choices") or []
                if choices:
                    text = str(((choices[0].get("message") or {}).get("content")) or "")
            if last_status == 200 and "VENTURA_OK" in text:
                success = True
                selected = model
                break

        results.append(Result(label, True, success, f"HTTP {last_status}" + (f" model={selected}" if success else "")))

    if not results:
        results.append(Result("github-models", True, False, "catalog contained no supported vendor prefixes"))
    return results


def gemini() -> Result:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return Result("gemini", False, False, "secret not configured")
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    status, body = request_json(
        "POST",
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        {"x-goog-api-key": key, "Content-Type": "application/json"},
        {"contents": [{"parts": [{"text": PROMPT}]}], "generationConfig": {"temperature": 0, "maxOutputTokens": 20}},
    )
    text = ""
    if isinstance(body, dict):
        candidates = body.get("candidates") or []
        if candidates:
            parts = ((candidates[0].get("content") or {}).get("parts") or [])
            text = " ".join(str(p.get("text", "")) for p in parts)
    return Result("gemini", True, status == 200 and "VENTURA_OK" in text, f"HTTP {status}")


def openai_compatible(provider: str, key_env: str, url: str, model_env: str, default_model: str) -> Result:
    key = os.getenv(key_env)
    if not key:
        return Result(provider, False, False, "secret not configured")
    status, body = request_json(
        "POST",
        url,
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        {
            "model": os.getenv(model_env, default_model),
            "messages": [{"role": "user", "content": PROMPT}],
            "max_tokens": 20,
            "temperature": 0,
        },
    )
    text = ""
    if isinstance(body, dict):
        text = str((((body.get("choices") or [{}])[0].get("message") or {}).get("content")) or "")
    return Result(provider, True, status == 200 and "VENTURA_OK" in text, f"HTTP {status}")


def main() -> int:
    results = github_models()
    results += [
        gemini(),
        openai_compatible("groq", "GROQ_API_KEY", "https://api.groq.com/openai/v1/chat/completions", "GROQ_MODEL", "llama-3.3-70b-versatile"),
        openai_compatible("mistral", "MISTRAL_API_KEY", "https://api.mistral.ai/v1/chat/completions", "MISTRAL_MODEL", "mistral-small-latest"),
    ]

    print("Ventura AI Provider Validation")
    print("provider                    configured   valid   detail")
    print("--------------------------------------------------------------------------")
    for r in results:
        print(f"{r.provider:<27} {str(r.configured):<12} {str(r.ok):<7} {r.detail}")

    configured = [r for r in results if r.configured]
    valid = [r for r in configured if r.ok]
    github_valid = [r for r in valid if r.provider.startswith("github-models/")]
    external_configured = [r for r in configured if not r.provider.startswith("github-models/")]
    broken_external = [r.provider for r in external_configured if not r.ok]

    print(f"\nConfigured endpoints: {len(configured)} | Valid endpoints: {len(valid)} | GitHub vendor models valid: {len(github_valid)}")

    # Require at least one live GitHub marketplace vendor. Additional external
    # provider secrets are optional, but if configured they must validate.
    if not github_valid:
        print("ERROR: no live GitHub Models vendor validated", file=sys.stderr)
        return 1
    if broken_external:
        print("ERROR: configured external provider(s) failed: " + ", ".join(broken_external), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
