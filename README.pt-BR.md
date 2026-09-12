<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: light)" srcset="./assets/profile-header-mobile-light.svg" />
  <source media="(max-width: 600px)" srcset="./assets/profile-header-mobile.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/profile-header-light.svg" />
  <img src="./assets/profile-header.svg" width="100%" alt="Marcus Boni — desenvolvedor de software. Produtos full-stack e IA aplicada. Retrato original em ASCII dentro de um terminal." />
</picture>

<p align="right"><a href="./README.md">English</a> · <strong>Português</strong></p>

Sou **Marcus**, desenvolvedor de software no Espírito Santo, Brasil. Construo **produtos full-stack e soluções de IA aplicada**, com foco em ferramentas para desenvolvedores, transcrição local e busca com citações.

[Portfólio](https://marcusboni.com.br/) · [LinkedIn](https://www.linkedin.com/in/marcus-boni-729a52243/) · [E-mail](mailto:mgalvaoboni@gmail.com)

## Projetos em destaque

### [OptTime](https://github.com/Marcus-Boni/OptTime) · Fluxos de desenvolvimento

Controle de horas conectado ao Azure DevOps: apontamentos, dashboards e automações em uma aplicação. Inclui uma extensão para o Azure DevOps e um servidor MCP para agentes trabalharem com os mesmos fluxos.

`TypeScript` `Next.js` `PostgreSQL` `Drizzle` `MCP` · [Servidor MCP ↗](https://github.com/Marcus-Boni/OptTime/blob/44a6c930d0725996a23b97cb003ec5df4b9aca57/packages/opt-time-mcp/src/server.ts)

### [ISPer](https://github.com/Marcus-Boni/ISPer) · Desktop e áudio

Transcrição local de voz com whisper.cpp, workspace Rust e aplicação desktop em Tauri. Componentes separados para áudio, modelos e LLMs, com builds Windows para CPU/CUDA e verificações de release.

`Rust` `Tauri` `whisper.cpp` `Windows` · [Workspace Rust ↗](https://github.com/Marcus-Boni/ISPer/blob/de736db67379d2bddbb11328f917788bc19577e5/Cargo.toml)

### [chatbot-template](https://github.com/Marcus-Boni/chatbot-template) · Busca e IA

Template RAG para consultar transcrições de reuniões do Teams. Combina busca com pgvector, citações das fontes e consultas restritas por workspace, com avaliação da qualidade de recuperação.

`TypeScript` `Next.js` `CopilotKit` `pgvector` · [Avaliação da busca ↗](https://github.com/Marcus-Boni/chatbot-template/blob/a9969fc6695030d20b109159a81ee40a0c4b5cc5/src/core/rag/eval.ts)

### [Portfólio](https://github.com/Marcus-Boni/Marcus-Boni-Portfolio) · Design e engenharia web

Portfólio bilíngue com um campo de tinta interativo em WebGL, blog Markdown e analytics próprios. API pública, contrato OpenAPI e páginas legíveis por agentes tornam o conteúdo acessível além da interface visual.

`React` `Vite` `TypeScript` `WebGL` `Firebase` · [Testes do contrato da API ↗](https://github.com/Marcus-Boni/Marcus-Boni-Portfolio/blob/d582da477ef60110f40652afc528a6d2f66fe77a/tests/openapi.test.ts)

<details>
<summary><strong>Mais projetos e como construo</strong></summary>

- **[Estimativa de horas](https://github.com/Marcus-Boni/Ferramenta-Estimativa-Horas)** — fluxo web por equipe para estimar tarefas, acompanhar dashboards e exportar para Excel.
- **[Jarvis](https://github.com/Marcus-Boni/Jarvis)** — experimento de assistente local-first com FastAPI, Ollama, memória vetorial e dashboard em Next.js.
- **[SignalR Meetup](https://github.com/Marcus-Boni/SignalR-Meetup-App)** — demonstração de tempo real com tracking, chat de múltiplas salas e status assíncrono de pagamentos.

### Como construo

- **Começar pelo fluxo de trabalho.** Transformar etapas operacionais repetitivas em ferramentas e integrações com um objetivo claro.
- **Explicitar os limites.** Separar processamento local, provedores externos e acesso aos dados.
- **Facilitar a inspeção.** Documentar decisões, testar comportamentos relevantes e manter builds reproduzíveis.

</details>

---

Interesse em ferramentas para desenvolvedores, IA aplicada ou boas experiências web? [Vamos conversar.](mailto:mgalvaoboni@gmail.com)
