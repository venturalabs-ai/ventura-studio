# AI Provider & Branch Protection Bootstrap

This document records the required secret names and security boundaries. **Never commit secret values.** `.env` and `.env.*` are already ignored by Git.

## AI providers

The repository supports these providers:

| Provider | Secret | Notes |
|---|---|---|
| GitHub Models | `GITHUB_TOKEN` | Supplied automatically by GitHub Actions when Models access is available. Current validation may report HTTP 410 if Models is unavailable for the account/workflow context. |
| Google Gemini | `GEMINI_API_KEY` | Optional repository Secret. Free-tier/rate-limited availability depends on Google AI Studio account eligibility. |
| Groq | `GROQ_API_KEY` | Optional repository Secret. Free developer usage is rate-limited. |
| Mistral | `MISTRAL_API_KEY` | Optional repository Secret. Mistral Free mode is rate-limited. |

Optional model overrides:

- `GEMINI_MODEL`
- `GROQ_MODEL`
- `MISTRAL_MODEL`
- `GITHUB_MODELS_MODEL`

The validation workflow prints only provider/model identifiers and sanitized HTTP status. It does not print keys or provider error bodies.

## Adding a repository Secret

GitHub UI path:

`Repository → Settings → Secrets and variables → Actions → New repository secret`

Use exactly the names above. Do not place values in source files, workflow YAML, issues, PR descriptions, README files or commit messages.

## Branch protection

The workflow `Enforce Branch Protection` requires:

`VENTURA_GITHUB_ADMIN_TOKEN`

Use a fine-grained GitHub personal access token or GitHub App token with the smallest practical scope. It must have **Administration: read/write** for the six flagship repositories and enough read access to inspect repository metadata and check runs.

The token is stored only as a GitHub Actions Secret and is passed to `scripts/enforce_branch_protection.py` at runtime.

The script protects:

1. `Ventura.SEG`
2. `ventura-pro-agro`
3. `ventura-chat`
4. `autor-ventura`
5. `ventura-agents`
6. `ventura-studio`

For every default branch it:

- resolves the current HEAD;
- discovers successful check-runs on that HEAD;
- refuses to configure an empty required-check set;
- requires those successful checks;
- requires the branch to be up to date before merge;
- requires changes to go through a pull request;
- applies the rules to administrators too;
- blocks force pushes;
- blocks branch deletion;
- requires conversation resolution;
- keeps zero mandatory external reviewers while the project is maintained by a single primary maintainer.

If a team with independent reviewers is added later, raise `required_approving_review_count` and enable `require_last_push_approval`.

## Verification rule

Do not publish `CI protected`, `production-grade`, `0 critical vulnerabilities`, or provider-availability claims solely because these files exist. Promotion requires successful workflow execution plus an API readback confirming protection is active.
