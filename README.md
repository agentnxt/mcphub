# MCPHub by AgentNxt

**Production-ready MCP servers for your entire stack. 58 servers, 1000+ tools.**

[![Build Status](https://img.shields.io/github/actions/workflow/status/agentnxt/mcp-registry/docker-push.yml?style=flat-square)](https://github.com/agentnxt/mcp-registry/actions)
[![Docker Hub](https://img.shields.io/docker/pulls/agentnxt/filesystem-mcp-server?style=flat-square)](https://hub.docker.com/u/agentnxt)
[![License](https://img.shields.io/github/license/agentnxt/mcp-registry?style=flat-square)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=flat-square)](https://www.typescriptlang.org/)

---

## Table of Contents

- [Quick Start (Docker)](#quick-start-docker)
- [Quick Start (Node.js)](#quick-start-nodejs)
- [Available Servers](#available-servers)
- [Development](#development)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

---

## Quick Start (Docker)

### Pull and Run Any Server

```bash
# Basic usage
docker run -d \
  -e SERVICE_URL="https://your-service.com" \
  -e SERVICE_API_KEY="your-api-key" \
  agentnxt/<server-name>

# Example: filesystem server
docker run -d \
  -e ALLOWED_DIRECTORIES="/data" \
  agentnxt/filesystem-mcp-server

# Example: GitHub server
docker run -d \
  -e GITHUB_TOKEN="your-github-token" \
  agentnxt/github-mcp-server

# Example: Slack server
docker run -d \
  -e SLACK_BOT_TOKEN="xoxb-your-token" \
  -e SLACK_TEAM_ID="your-team-id" \
  agentnxt/slack-mcp-server
```

### Docker Compose

```yaml
version: '3.8'

services:
  filesystem-mcp:
    image: agentnxt/filesystem-mcp-server
    environment:
      - ALLOWED_DIRECTORIES=/data
    volumes:
      - ./data:/data
    restart: unless-stopped

  github-mcp:
    image: agentnxt/github-mcp-server
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    restart: unless-stopped
```

### Environment Variables

Each server requires specific environment variables. See individual server README files for details.

All images are available on Docker Hub: https://hub.docker.com/u/agentnxt

---

## Quick Start (Node.js)

### Install and Run

```bash
# Clone the repo
git clone https://github.com/agentnxt/mcp-registry.git
cd mcp-registry

# Install all dependencies
npm install

# Build every server
npm run build

# Build a single server
cd filesystem-mcp-server && npm run build
```

### Add to Claude Desktop

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": ["/path/to/mcp-registry/filesystem-mcp-server/dist/index.js"],
      "env": {
        "ALLOWED_DIRECTORIES": "/data"
      }
    },
    "github": {
      "command": "node",
      "args": ["/path/to/mcp-registry/github-mcp-server/dist/index.js"],
      "env": {
        "GITHUB_TOKEN": "your-token"
      }
    }
  }
}
```

---

## Available Servers

This monorepo contains **58 MCP servers** covering various services:

| Category | Servers |
|----------|---------|
| **AI & ML** | litellm-mcp-server, txtai-mcp-server, ollama-mcp-server, mlflow-mcp-server |
| **Development** | github-mcp-server, gitlab-mcp-server, playwright-mcp-server |
| **Search** | brave-search-mcp-server, searxng-mcp-server, exa-mcp-server |
| **Productivity** | slack-mcp-server, calcom-mcp-server, n8n-mcp-server |
| **Storage** | filesystem-mcp-server, redis-mcp-server, qdrant-mcp-server, surrealdb-mcp-server |
| **Commerce** | woocommerce-mcp-server, lago-mcp-server, stripe-mcp-server |
| **Monitoring** | grafana-mcp-server, datadog-mcp-server, uptime-kuma-mcp-server |
| **Cloud** | aws-kb-retrieval-mcp-server, gdrive-mcp-server, nextcloud-mcp-server |

---

## Development

### Project Structure

```
mcp-registry/
├── packages/                    # Server packages
│   ├── filesystem-mcp-server/
│   │   ├── src/
│   │   │   ├── index.ts         # MCP server entry point
│   │   │   ├── lib.ts           # Core utilities
│   │   │   └── tools/           # Tool definitions
│   │   ├── Dockerfile           # Multi-stage Docker build
│   │   ├── package.json
│   │   └── tsconfig.json
│   └── ...
├── .github/
│   └── workflows/
│       └── docker-push.yml      # CI/CD pipeline
├── docker-compose.yml
└── package.json
```

### Adding a New Server

1. Create a new directory under the project root
2. Add `package.json`, `tsconfig.json`, `Dockerfile`, and source files
3. Update the matrix in `.github/workflows/docker-push.yml`
4. Add a section to this README

### Build Scripts

```bash
# Build all servers
npm run build

# Build only changed servers
npm run build:changed

# Build specific server
cd <server-name> && npm run build
```

---

## Architecture

### MCP Server Pattern

Each server follows a consistent pattern:

1. **Entry Point** (`index.ts`): Initializes the MCP server with stdio transport
2. **Tool Handlers**: Implement business logic for each tool
3. **Client Layer**: Handles API communication with external services
4. **Type Definitions**: TypeScript types for type safety

### Docker Build

- **Multi-stage builds** for minimal image size
- **Non-root user** execution for security
- **Build caching** via GitHub Actions
- **Vulnerability scanning** with Trivy

---

## Contributing

Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

### Code Style

- TypeScript strict mode enabled
- ESLint for linting
- Prettier for formatting
- Run `npm run lint` before committing

### Testing

```bash
cd <server-name>
npm test
```

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

Copyright 2026 AgentNxt. All rights reserved.

An Autonomyx Platform.

See individual server directories for specific license information.
