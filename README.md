# MCP Registry

**The Tool Catalog for MCP-compatible AI agents.**

MCP Registry is an open catalog of reusable MCP tools that agents can discover, deploy, and compose through the Model Context Protocol. Each tool package includes focused capabilities, MCP tool definitions, deployment metadata, and runtime instructions.

---

## Why Tool Catalog?

Traditional MCP projects describe integrations as servers. MCP Registry organizes them as a discoverable **tool catalog**:

| Traditional MCP View | Tool Catalog View |
| --- | --- |
| MCP server | Tool package |
| Tool endpoint | Tool action |
| Server metadata | Tool manifest |
| Docker image | Tool runtime |
| Server list | Discoverable tool catalog |

---

## What is included

- 58+ MCP-compatible tool packages
- 1000+ tools across SaaS, developer tools, infrastructure, data, automation, and monitoring
- Docker-ready runtimes
- Workspace-based package structure
- Tool manifest schema and validation workflow

---

## Quick Start

```bash
git clone https://github.com/AGenNext/mcp-registry.git
cd mcp-registry
npm install
npm run check
```

Build every workspace:

```bash
npm run build
```

Build one tool package:

```bash
npm run build --workspace=packages/<tool-package-name>
```

Run a built MCP tool package:

```bash
node packages/<tool-package-name>/dist/index.js
```

---

## Docker

```bash
docker run -d \
  -e SERVICE_URL="https://your-service.com" \
  -e SERVICE_API_KEY="your-api-key" \
  agentnxt/<tool-package-name>
```

Published images are available on Docker Hub:

https://hub.docker.com/u/agentnxt

---

## Tool Manifest

Each tool package should include a `tool.json` or equivalent manifest:

```json
{
  "name": "github-repo-search",
  "title": "GitHub Repository Search",
  "description": "Search repositories, issues, and pull requests.",
  "category": "development",
  "docker_image": "agentnxt/github-mcp-server",
  "tools": ["search_repositories", "list_issues"],
  "auth": ["github_token"],
  "tags": ["github", "code", "search"]
}
```

---

## Recommended Tool Package Layout

```text
packages/<tool-package-name>/
  tool.json
  README.md
  Dockerfile
  src/
    index.ts
    tools/
    api/
  package.json
  tsconfig.json
```

---

## Validate the Registry

```bash
npm run validate
```

The validator checks for required tool packaging files where applicable.

---

## Claude Desktop Configuration

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": ["/absolute/path/to/mcp-registry/packages/filesystem-mcp-server/dist/index.js"],
      "env": {
        "ALLOWED_DIRECTORIES": "/data"
      }
    }
  }
}
```

Use absolute paths so your MCP client can find the runtime reliably.

---

## Contributing

Contributions are welcome. Please read `CONTRIBUTING.md` before opening a pull request.

---

## Security

Please report vulnerabilities privately using the instructions in `SECURITY.md`.

---

## Website

The marketing site can be deployed with GitHub Pages.

---

Copyright 2026 AgentNxt. An Autonomyx Platform.
