---
name: skill-audit
description: Audit Agent Skills across Ventura repositories for overlap weak triggers unsupported references and format violations. Use when reviewing a repository skill catalog or preparing ecosystem-wide skill changes. Do not use when implementing the domain task described by an individual skill.
---

# Skill audit

- Enumerate `.github/skills/*/SKILL.md` in the target repository.
- Check folder and frontmatter names match and use kebab-case.
- Verify every description states both when to use and when not to use.
- Compare trigger scope pairwise and merge skills that compete for the same request.
- Confirm every referenced file module command and API exists or is explicitly conditional.
- Remove generic advice the agent already knows without repository context.
- Keep bodies imperative and under 200 lines.
- Run the shared Ventura Agent Skill validator before finishing.
