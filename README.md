# Agent-Tools

Agent-Tools is the canonical tool catalog for the AGenNext platform.

A tool is an invocable capability that can be discovered, governed, permissioned, reviewed, and used by agents, workflows, teams, and runtimes.

## Core model

```text
Tool Catalog
  contains Tool records

Tool Provider
  exposes one or more Tools

MCP Server
  is one type of Tool Provider

One MCP server
  can expose many tools
```

Therefore this repository is not only an MCP registry. MCP is an integration/provider protocol inside the broader tool catalog.

## Repository responsibilities

Agent-Tools owns:

```text
- tool catalog entries
- external tool definitions
- provider definitions
- MCP provider package metadata
- tool capability metadata
- tool invocation contracts
- tool security and approval metadata
```

Agent-Tools does not own:

```text
- runtime execution of agents
- skill definitions
- agent blueprints
- graph schema
- grammar rules
- seed-data ownership
```

## Current folders

### `catalog/`

Canonical catalog entries for tools and external tools.

Example:

```text
catalog/surrealkit.tool.yaml
```

### `packages/`

Existing folders under `packages/` are treated as **tool provider packages**.

Most current packages are MCP server providers. They should be migrated conceptually from:

```text
MCP server = catalog item
```

to:

```text
MCP server = provider package
provider package exposes one or more cataloged tools
```

Recommended package structure:

```text
packages/<provider-name>/
  provider.yaml          # provider metadata
  tools/                 # tool catalog entries exposed by this provider
    <tool-id>.tool.yaml
  src/                   # provider implementation
  package.json
  tsconfig.json
```

## MCP provider model

An MCP server package should declare:

```yaml
provider_id: filesystem-mcp-provider
provider_type: mcp_server
exposes_tools:
  - filesystem.read_file
  - filesystem.write_file
  - filesystem.list_directory
```

Each exposed tool should have a catalog entry with:

```yaml
id: filesystem.read_file
type: tool
provider: filesystem-mcp-provider
protocol: mcp
risk: medium
approval_required: false
```

## Build existing provider packages

Existing packages can still be built as Node.js workspaces:

```bash
npm install
npm run build
npm run build:changed
npm run build --workspace=packages/<provider-name>
```

Run a built MCP provider directly:

```bash
node packages/<provider-name>/dist/index.js
```

## Environment variables

Provider packages may require credentials or service URLs.

Common examples:

```bash
SERVICE_URL="https://your-service.com"
SERVICE_API_KEY="your-api-key"
ALLOWED_DIRECTORIES="/data"
```

Never commit secrets into this repository. Use environment variables, Docker secrets, or runtime secret stores.

## Migration rule for existing packages

Do not delete existing provider packages immediately.

Migrate them in place:

```text
1. Add provider.yaml to each package.
2. Identify tools exposed by that provider.
3. Add one .tool.yaml catalog entry per exposed tool.
4. Mark provider risk and auth requirements.
5. Keep implementation under src/.
6. Build and test provider package.
```

## Relationship to other repos

```text
Agent-Skills
  uses tools as executable capabilities

Agent-Graph
  maps tools, providers, permissions, and invocations

Agent-Grammar
  validates tool and provider records

Agent-Seed
  seeds default platform tool/provider records

Agent-Review
  reviews high-risk tools before publication/use
```

## Rule

A provider is not the same thing as a tool.

```text
MCP server/provider
  != Tool

MCP server/provider
  exposes Tools
```
