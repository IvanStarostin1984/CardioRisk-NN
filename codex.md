<!-- markdownlint-disable -->
# OpenAI Codex 2025 — Consolidated Technical Specification

*v4 (16 Jun 2025 – lean, duplicate‑free, citation‑free)*

This document fuses every **unique** fact drawn from the seven markdown files you supplied, then adds the missing operational details you requested (file conventions, scripting patterns, exact container sequence, GitHub‑connector limits, etc.).
Use it verbatim as compact, high‑signal context for another LLM.

---

## 1  Milestones & Availability

| Event                                    | Date / Fact                                                    |
| ---------------------------------------- | -------------------------------------------------------------- |
| Public launch (Pro / Team / Enterprise)  | **16 May 2025**                                                |
| Plus tier enabled                        | **3 Jun 2025**                                                 |
| High‑compute variant `o3‑pro` (Pro plan) | **10 Jun 2025**                                                |
| Research‑preview status                  | Ongoing — Codex included in ChatGPT subscription; no extra fee |

---

## 2  Pricing & Quotas (ChatGPT subscription ⇒ Codex)

| Plan | Monthly fee                                         | Codex availability | Deep‑Research quota |
| ---- | --------------------------------------------------- | ------------------ | ------------------- |
| Pro  |  \$200 USD                                          | Day‑1              |  120 queries / mo   |
| Plus |  \$20 USD                                           |  3 Jun 2025        |  10 queries / mo    |
| Team |  \$25 user / mo (annual) · \$30 user / mo (monthly) | Day‑1              |  —                  |

Codex itself has **no separate surcharge** while in research preview.

---

## 3  Core Model & Reasoning

| Aspect             | Value                                                 |
| ------------------ | ----------------------------------------------------- |
| Underlying model   | **`codex‑1`** — fine‑tuned variant of OpenAI o3       |
| Max context window | **≈ 192 k tokens**                                    |
| Training extras    | RLHF + RLAIF on thousands of real engineering tickets |
| Reasoning style    | Hidden chain‑of‑thought → compressed public answer    |
| Public variants    | `codex‑mini‑latest` (CLI) · `o3‑pro` (ChatGPT Pro)    |

---

## 4  Security & Safety Snapshot

| Metric                       | codex‑1 | baseline o3 |
| ---------------------------- | ------- | ----------- |
| Malware refusal (synthetic)  | 0.97    | —           |
| Malware refusal (golden)     | 0.98    | —           |
| StrongReject jailbreak @ 0.1 | 0.98    |  0.97       |
| Harassment/threat not‑unsafe | 0.98    |  0.99       |

**Mitigations** — RL safety fine‑tuning, deny‑all network during agent phase, instruction‑hierarchy hardening, live policy monitoring.

---

## 5  End‑to‑End Lifecycle in ChatGPT Codex Cloud

```text
User prompt
└─→ Container boot   (Ubuntu 22.04 LTS, non‑privileged)
     ├─ ① Repo clone via ChatGPT Connector (token = contents+PR)
     ├─ ② Setup‑script phase  (network ALLOWED, time‑boxed, secrets injected)
     ├─ ③ Agent phase        (network BLOCKED ‑or‑ opt‑in allow‑list)
     └─ ④ Review phase       (diff & logs exposed; micro‑VM destroyed)
```

### 5.1 GitHub Connector

* Granted scopes: `contents:read,write`, `pull_requests:read,write` (no `actions:*` → Actions logs 403).
* Long‑lived installation tokens; repo cloned into `/workspace` at container start.

### 5.2 Setup‑script Phase

| Rule          | Detail                                                                                    |
| ------------- | ----------------------------------------------------------------------------------------- |
| Entry point   | UI‑uploaded shell script **or** `.codex/setup.sh` in repo root                            |
| Privilege     | Runs as **root**                                                                          |
| Network       | Outbound Internet **only while script runs**                                              |
| Time‑outs     | Free ≤ 5 min · Plus ≤ 10 min · Pro/Team/Business ≤ 20 min                                 |
| Secrets       | Env‑vars injected exclusively here                                                        |
| Best practice | Idempotent, non‑interactive; install all online dependencies (`apt`, `pip`, `npm ci`) now |

### 5.3 Agent Phase

| Characteristic | Value                                                                                        |
| -------------- | -------------------------------------------------------------------------------------------- |
| Network        | **Blocked** by default; opt‑in granular egress (domain & method allow‑list) since 3 Jun 2025 |
| Iterative loop | “plan → act → observe”; every shell command & test logged                                    |
| Diff cap       | **5 MiB** (raised 3 Jun 2025)                                                                |
| Model context  | System prompt + recursively merged `AGENTS.md` + user prompt                                 |
| Result         | Git commit / PR diff + full command transcript                                               |

### 5.4 Review Phase

Human reviews diff and logs, then pushes PR or discards; container is immediately destroyed.

---

## 6  Base Image & Runtime Matrix (`codex‑universal`)

| Runtime      | Default version                                         | Override via env           |
| ------------ | ------------------------------------------------------- | -------------------------- |
| Python       | 3.11.12 (+ pyenv, poetry, uv, ruff, black, mypy, isort) | `CODEX_ENV_PYTHON_VERSION` |
| Node.js      | 20 (+ corepack, yarn, pnpm)                             | `CODEX_ENV_NODE_VERSION`   |
| Rust         | 1.87.0                                                  | `CODEX_ENV_RUST_VERSION`   |
| Go           | 1.23.8                                                  | `CODEX_ENV_GO_VERSION`     |
| Swift        | 6.1                                                     | `CODEX_ENV_SWIFT_VERSION`  |
| Also present | Ruby 3.2 · Java 21 · Bazelisk/Bazel                     | —                          |

---

## 7  Guidance & File Conventions

### 7.1 `AGENTS.md` — Soft Prompt for Agents

| Rule              | Explanation                                                         |
| ----------------- | ------------------------------------------------------------------- |
| Recursive scan    | All `AGENTS.md` files are merged; the **deepest‑path file wins**.   |
| Prompt precedence | The user’s live prompt overrides any file guidance.                 |
| Typical content   | `shell:` blocks (commands/tests), env vars, lint/style rules.       |
| Execution         | Codex runs each `shell:` block at the **start of every iteration**. |

**Example**

```markdown
## How to run tests
shell: |
  pip install -e .
  pytest -q
```

**Authoring best practices**

1. Declare an explicit test command; never rely on heuristic detection.
2. Keep the file short—Codex reparses it in every loop.
3. Store it beside the code it governs (monorepo friendly).
4. Document produced artifacts (coverage XML path, build dir).

### 7.2 Other Special Files

| File              | Purpose                                             |
| ----------------- | --------------------------------------------------- |
| `.codex/setup.sh` | Repo‑level setup script (alternative to UI upload). |
| `README_CI.md`    | Explain CI matrix so Codex matches test shards.     |
| `CODEREVIEW.md`   | House style & PR checklist Codex should follow.     |

---

## 8  Scripting & Secrets — Proven Patterns

* **Install everything** online inside the setup script; agent runs offline.
* Make the script executable (`chmod +x .codex/setup.sh`) and ensure it **exits 0**.
* Inject secrets via *Environment → Secrets*; reference with `$VAR` in the script.
* Cache heavy toolchains (`npx playwright install-deps`) during setup.
* Use idempotent commands (`apt-get update && apt-get install -y …`) for safe retries.

---

## 9  Accessing GitHub Actions Logs (Connector lacks `actions:*`)

| Pattern                  | How it works                                                                                                      |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| **Fine‑grained PAT**     | Create token with `actions:read`; mount as `GH_ACTIONS_PAT` secret; download with `gh run download` during setup. |
| **Secondary GitHub App** | Mint installation token inside setup; call REST v3 `.../runs/{id}/logs`.                                          |

Never overwrite the default `GITHUB_TOKEN`; mount extra creds under fresh env vars and restrict their use to the setup script (unless outbound net is enabled).

---

## 10  Local Workflow (`@openai/codex` CLI)

* Install: `npm install -g @openai/codex`
* Sandboxing: `sandbox-exec` (macOS) · Docker + iptables (Linux) · WSL 2 (Windows)
* Modes: `suggest` → `auto‑edit` → `full‑auto` (only *full‑auto* runs shell commands)
* Works directly in the current Git worktree (no extra clone step)
* Network is blocked by default; allow host egress with `--allow-net`

---

## 11  Benchmark & Performance

| Benchmark                   | Result                                                                      |
| --------------------------- | --------------------------------------------------------------------------- |
| SWE‑Bench (runnable subset) | 23 / 23 issues solved                                                       |
| Internal repo suites        | Higher patch cleanliness vs raw o3 (AstroPy, Matplotlib, Django, Expensify) |

Typical task wall‑clock: **1 – 30 min**.

---

## 12  Quantitative Reference

| Metric                  | Value                                           |
| ----------------------- | ----------------------------------------------- |
| Context window          | ≈ 192 k tokens                                  |
| Max diff size           | 5 MiB (raised 3 Jun 2025)                       |
| Setup‑script time‑limit | Up to 20 min (Pro/Team/Business)                |
| Parallel tasks          | “Many” (OpenAI has not published a numeric cap) |

---

## 13  Known Limitations & Roadmap

* Latency — remote container adds seconds‑to‑minutes vs inline completions.
* Modal gaps — no image input or mid‑task interactive steering (planned).
* Mandatory human review — every diff must be approved or discarded; no warranty.
* Roadmap — mid‑task guidance, richer IDE integrations, expanded connector APIs.

---

## 14  Field‑Tested Checklist (Quick Reminders)

1. **Write** a setup script that finishes within your tier’s timeout.
2. **Pin** exact test commands in `AGENTS.md`.
3. **Scope** tasks narrowly—think “single PR”.
4. **Store** secrets in the UI, *never* inline.
5. **Dry‑run** locally with the CLI before using cloud agents.
6. **Review** every diff and log—Codex is powerful but not infallible.

---

*End of specification — ready for ingestion by any LLM assistant.*
