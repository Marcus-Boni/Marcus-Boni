<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: light)" srcset="./assets/profile-header-mobile-light.svg?v=portrait-motion-2" />
  <source media="(max-width: 600px)" srcset="./assets/profile-header-mobile.svg?v=portrait-motion-2" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/profile-header-light.svg?v=portrait-motion-2" />
  <img src="./assets/profile-header.svg?v=portrait-motion-2" width="100%" alt="Marcus Boni — software developer. Full-stack products and applied AI. An original ASCII portrait in a terminal." />
</picture>

<p align="right"><strong>English</strong> · <a href="./README.pt-BR.md">Português</a></p>

I’m **Marcus**, a software developer based in Espírito Santo, Brazil. I turn complex workflows into **full-stack products and applied AI**: developer tools, local transcription and retrieval systems that show their sources.

[Portfolio](https://marcusboni.com.br/) · [LinkedIn](https://www.linkedin.com/in/marcus-boni-729a52243/) · [Email](mailto:mgalvaoboni@gmail.com)

## Selected work

### [OptTime](https://github.com/Marcus-Boni/OptTime) · Developer workflows

Time tracking connected to Azure DevOps: timesheets, dashboards and automations in one application. Includes an Azure DevOps extension and an MCP server so agents can work with the same workflows.

`TypeScript` `Next.js` `PostgreSQL` `Drizzle` `MCP` · [MCP server ↗](https://github.com/Marcus-Boni/OptTime/blob/44a6c930d0725996a23b97cb003ec5df4b9aca57/packages/opt-time-mcp/src/server.ts)

### [ISPer](https://github.com/Marcus-Boni/ISPer) · Desktop & audio

Local speech transcription with whisper.cpp, a Rust workspace and a Tauri desktop app. Separate audio, model and LLM components, with Windows CPU/CUDA build paths and release checks.

`Rust` `Tauri` `whisper.cpp` `Windows` · [Rust workspace ↗](https://github.com/Marcus-Boni/ISPer/blob/de736db67379d2bddbb11328f917788bc19577e5/Cargo.toml)

### [chatbot-template](https://github.com/Marcus-Boni/chatbot-template) · Retrieval & AI

A RAG template for searching Teams meeting transcripts. Combines pgvector retrieval, source citations and workspace-scoped search, with an evaluation harness for retrieval quality.

`TypeScript` `Next.js` `CopilotKit` `pgvector` · [Retrieval evaluation ↗](https://github.com/Marcus-Boni/chatbot-template/blob/a9969fc6695030d20b109159a81ee40a0c4b5cc5/src/core/rag/eval.ts)

### [Portfolio](https://github.com/Marcus-Boni/Marcus-Boni-Portfolio) · Design & web engineering

A bilingual portfolio with an interactive WebGL ink field, a Markdown blog and first-party analytics. A public API, OpenAPI contract and agent-readable pages make the content available beyond the visual interface.

`React` `Vite` `TypeScript` `WebGL` `Firebase` · [API contract tests ↗](https://github.com/Marcus-Boni/Marcus-Boni-Portfolio/blob/d582da477ef60110f40652afc528a6d2f66fe77a/tests/openapi.test.ts)

<details>
<summary><strong>More work</strong></summary>

- **[Hour estimation](https://github.com/Marcus-Boni/Ferramenta-Estimativa-Horas)** — a team-based web workflow for task estimates, dashboards and Excel export.
- **[Jarvis](https://github.com/Marcus-Boni/Jarvis)** — a local-first assistant experiment with FastAPI, Ollama, vector memory and a Next.js dashboard.
- **[SignalR Meetup](https://github.com/Marcus-Boni/SignalR-Meetup-App)** — a real-time demo covering tracking, multi-room chat and asynchronous payment status.

</details>

## How I build

- **Start with the workflow.** Turn repetitive operational steps into focused tools and integrations.
- **Make boundaries explicit.** Separate local processing, external providers and data access.
- **Make the work inspectable.** Document decisions, test meaningful behavior and keep builds reproducible.

---

Interested in developer tools, practical AI or thoughtful web experiences? [Let’s talk.](mailto:mgalvaoboni@gmail.com)
