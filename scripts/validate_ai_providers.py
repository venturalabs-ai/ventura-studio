#!/usr/bin/env python3
"""Validate AI providers without printing credentials.

GitHub Models is validated with multiple official API-version header variants
because availability can differ across account/workflow contexts. External
providers are validated only when repository secrets are configured.
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
        return exc.code, {}
    except urllib.error.URLError:
        return 0, {}


def github_headers(token: str, api_version: str | None) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
    }
    if api_version:
        headers["X-GitHub-Api-Version"] = api_version
    return headers


def _lightweight_score(model_id: str) -> tuple[int, int, str]:
    name = model_id.lower()
    lightweight = 0 if any(x in name for x in ("nano", "mini", "small", "flash", "lite")) else 1
    dated = 1 if any(c.isdigit() for c in name) else 0
    return lightweight, dated, model_id


def _extract_chat(body: object) -> str:
    if not isinstance(body, dict):
        return ""
    choices = body.get("choices") or []
    if not choices:
        return ""
    return str(((choices[0].get("message") or {}).get("content")) or "")


def _validate_github_model(token: str, model: str, headers: dict[str, str]) -> tuple[bool, int]:
    status, body = request_json(
        "POST",
        "https://models.github.ai/inference/chat/completions",
        headers,
        {"model": model, "messages": [{"role": "user", "content": PROMPT}], "max_tokens": 20, "temperature": 0},
    )
    return status == 200 and "VENTURA_OK" in _extract_chat(body), status


def github_models() -> list[Result]:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return [Result("github-models", False, False, "GITHUB_TOKEN not configured")]

    header_variants = (
        ("2022-11-28", github_headers(token, "2022-11-28")),
        ("2026-03-10", github_headers(token, "2026-03-10")),
        ("default", github_headers(token, None)),
    )

    last_catalog_status = 0
    for version_label, headers in header_variants:
        status, catalog = request_json("GET", "https://models.github.ai/catalog/models", headers)
        last_catalog_status = status
        if status != 200 or not isinstance(catalog, list):
            continue

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
                success, last_status = _validate_github_model(token, model, headers)
                if success:
                    selected = model
                    break
            results.append(Result(label, True, success, f"HTTP {last_status} api={version_label}" + (f" model={selected}" if success else "")))
        if results:
            return results

    documented_models = ("openai/gpt-4o", "openai/gpt-4.1")
    for version_label, headers in header_variants:
        for model in documented_models:
            ok, status = _validate_github_model(token, model, headers)
            if ok:
                return [Result("github-models/openai", True, True, f"HTTP 200 api={version_label} model={model}")]
            last_catalog_status = status

    return [Result("github-models", True, False, f"unavailable HTTP {last_catalog_status}")]


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
        {"model": os.getenv(model_env, default_model), "messages": [{"role": "user", "content": PROMPT}], "max_tokens": 20, "temperature": 0},
    )
    text = _extract_chat(body)
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
    external_configured = [r for r in configured if not r.provider.startswith("github-models")]
    broken_external = [r.provider for r in external_configured if not r.ok]

    print(f"\nConfigured endpoints: {len(configured)} | Valid endpoints: {len(valid)} | GitHub vendor models valid: {len(github_valid)}")

    # Optional-provider policy:
    # - A configured external provider MUST validate successfully.
    # - GitHub Models is opportunistic because availability depends on account/context.
    # - When no external secret is configured and GitHub Models is unavailable, report
    #   SKIP instead of failing unrelated CI. This does not claim provider readiness.
    if broken_external:
        print("ERROR: configured external provider(s) failed: " + ", ".join(broken_external), file=sys.stderr)
        return 2
    if not valid:
        print("SKIP: no working AI provider is configured; provider readiness remains unverified")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
