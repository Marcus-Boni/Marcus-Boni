<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: light)" srcset="./assets/hero-terminal-v3-mobile-light.svg" />
  <source media="(max-width: 600px)" srcset="./assets/hero-terminal-v3-mobile.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/hero-terminal-v3-light.svg" />
  <img src="./assets/hero-terminal-v3.svg" width="100%" alt="Marcus Boni, software engineer. Monochrome silver ASCII bust portrait and systems terminal." />
</picture>

<p align="right"><strong>English</strong> · <a href="./README.pt-BR.md">Português</a></p>

I’m **Marcus Boni**, a software engineer based in Espírito Santo, Brazil. I build **full-stack products, native desktop systems, and applied AI workflows** — combining solid engineering fundamentals with AI-assisted development and sharing technical notes on [my blog](https://marcusboni.com.br/blog).

[Portfolio ↗](https://marcusboni.com.br/) · [Blog ↗](https://marcusboni.com.br/blog) · [LinkedIn ↗](https://www.linkedin.com/in/marcus-boni-729a52243/) · [Email ↗](mailto:mgalvaoboni@gmail.com)

---

## Selected work

### 01 · [ISPer](https://github.com/Marcus-Boni/ISPer) · Local-first voice engine

Offline Windows dictation and Teams meeting transcription built on a **12-crate Rust workspace**, Tauri 2, and `whisper.cpp` (CPU/CUDA). Audio stays on-device; production crates enforce strict zero-`unwrap` Clippy rules across **25 releases (`v0.30.0`)**.

`Rust` `Tauri 2` `whisper.cpp` `CUDA` `MCP` · [Site ↗](https://isper.pages.dev) · [Releases ↗](https://github.com/Marcus-Boni/ISPer/releases/latest) · [Workspace ↗](https://github.com/Marcus-Boni/ISPer/blob/72ea1174c881e860a32b3aed58f75edbdb5a2f86/Cargo.toml)

### 02 · [OptTime](https://github.com/Marcus-Boni/OptTime) · Developer workflows & MCP

Full-stack time tracking synced bi-directionally with **Azure DevOps**, featuring approval workflows, dashboards, Entra ID auth, and an Azure DevOps extension. Ships with a dual-transport (`stdio`/HTTP) **MCP server** (16 tools, 4 resources, 3 prompts) for AI agents.

`TypeScript` `Next.js 16` `PostgreSQL` `Drizzle` `MCP` · [Live ↗](https://opt-time.optsolv.com.br) · [MCP server ↗](https://github.com/Marcus-Boni/OptTime/blob/1e492d2e74dad1024c22c2230f0e07cc58796ceb/packages/opt-time-mcp/src/server.ts)

### 03 · [chatbot-template](https://github.com/Marcus-Boni/chatbot-template) · Grounded RAG & evals

Config-driven RAG template for Microsoft Teams transcripts over `pgvector` on Neon Postgres. Enforces mandatory source citations, workspace isolation, and a dedicated **retrieval evaluation harness** to measure search quality.

`TypeScript` `Next.js 16` `CopilotKit` `pgvector` `Vitest` · [Retrieval eval ↗](https://github.com/Marcus-Boni/chatbot-template/blob/a9969fc6695030d20b109159a81ee40a0c4b5cc5/src/core/rag/eval.ts)

### 04 · [Portfolio & Blog](https://github.com/Marcus-Boni/Marcus-Boni-Portfolio) · Web engineering & OpenAPI

Bilingual portfolio and technical journal with a custom **WebGL/GLSL ink field**, procedural code portrait, Markdown publishing, and first-party analytics. Exposes a public REST API with **OpenAPI contract tests** and agent-readable pages.

`React` `TypeScript` `WebGL` `Firebase` `OpenAPI` · [Site ↗](https://marcusboni.com.br/) · [Blog ↗](https://marcusboni.com.br/blog) · [OpenAPI tests ↗](https://github.com/Marcus-Boni/Marcus-Boni-Portfolio/blob/6d9e9b381e04c2a3689f5a1441089a8515d7b6ec/tests/openapi.test.ts)

---

## Architecture & stack

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: light)" srcset="./assets/systems-blueprint-v2-mobile-light.svg" />
  <source media="(max-width: 600px)" srcset="./assets/systems-blueprint-v2-mobile.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/systems-blueprint-v2-light.svg" />
  <img src="./assets/systems-blueprint-v2.svg" width="100%" alt="Monochrome animated ASCII architecture diagram covering four layers: Interfaces, Applied AI, Systems and Data, and Cloud and Ship." />
</picture>

- **Interfaces** — TypeScript, React, Next.js, WebGL/GLSL, Tailwind CSS, Flutter, React Native
- **Applied AI** — MCP Servers, pgvector RAG, Retrieval Evals, whisper.cpp, CopilotKit, Ollama
- **Systems & Data** — Rust, Tauri 2, UniFFI, Node.js, Python, C#/.NET, Java/Spring, PostgreSQL, Drizzle
- **Cloud & Delivery** — Azure, Azure DevOps, Docker, GitHub Actions, Firebase, CPU/CUDA Releases

## Writing

I publish regular technical articles on software architecture, applied AI workflows, and engineering decisions behind real projects at **[marcusboni.com.br/blog ↗](https://marcusboni.com.br/blog)**.

<details>
<summary><strong>More work</strong></summary>

- **[Auto Daily](https://github.com/Marcus-Boni/Auto-Daily-App)** — AI-assisted standup drafts synthesized from Azure DevOps commits and OptTime logs · [Live ↗](https://auto-daily-app.vercel.app)
- **[Hour Estimation](https://github.com/Marcus-Boni/Ferramenta-Estimativa-Horas)** — team-based estimation workflow wired to Azure DevOps with dashboards and Excel export · [Live ↗](https://ferramenta-estimativa-horas.vercel.app)
- **[Jarvis](https://github.com/Marcus-Boni/Jarvis)** — local-first developer assistant with FastAPI, Ollama, vector memory, and a Next.js dashboard
- **[SignalR Meetup](https://github.com/Marcus-Boni/SignalR-Meetup-App)** — real-time .NET SignalR demo with live tracking, multi-room chat, and async payment state

</details>

## How I build

- **AI-assisted engineering, grounded in fundamentals.** I use AI deliberately to explore architectures, understand complex domains, and accelerate delivery — always anchored in clean design, code review, and modern industry standards.
- **Start with the real workflow.** Turn repetitive operational friction into focused software wired directly into the team’s daily ecosystem.
- **Explicit boundaries & verifiable behavior.** Separate local compute, inference, and data access; verify with retrieval evals, OpenAPI contract tests, strict lints, and reproducible CI.
- **Continuous learning in public.** Stay current with evolving systems, applied AI, and web craft — documenting real trade-offs and lessons learned on [the blog](https://marcusboni.com.br/blog).

---

Interested in developer tools, applied AI, or clean software engineering? **[Let’s talk ↗](mailto:mgalvaoboni@gmail.com)** · [Portfolio](https://marcusboni.com.br/) · [Blog](https://marcusboni.com.br/blog) · [LinkedIn](https://www.linkedin.com/in/marcus-boni-729a52243/)
