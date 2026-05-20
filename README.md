# Agent-Tools

Agent-Tools is the canonical tool catalog for the AGenNext platform.

This is a cloud marketplace-style catalog problem.

A tool is an invocable product/capability package that can be discovered, governed, versioned, permissioned, reviewed, priced, installed, and used by agents, workflows, teams, and runtimes.

## Core model

```text
Capability
  = standardized semantic ability
  = what can be done

Tool
  = catalog product implementing one or more capabilities

Tool Version
  = versioned contract for a tool

Provider Offer
  = one way to access a specific tool version

Provider
  = organization, package, service, MCP server, CLI, SDK, HTTP API, or runtime endpoint offering the tool version
```

The primary catalog object is the **Tool**.

Capabilities standardize meaning. Versions standardize compatibility. Providers describe how a specific version is obtained or invoked.

## Marketplace rule

```text
One Capability
  can be implemented by many Tools

One Tool
  can implement many Capabilities

One Tool
  can have many Versions

One Tool Version
  can have many Provider Offers

One Provider
  can offer many Tools

One MCP Server
  is a Provider type

One MCP Server
  can expose many Tool Versions
```

## Example: capability, tool, version, providers

```yaml
id: filesystem.read_file
type: tool
name: Read File
capabilities:
  - file.read

versions:
  - version: 1.0.0
    contract:
      inputs:
        path: string
      outputs:
        content: string
    providers:
      - provider_id: filesystem-mcp-server
        provider_type: mcp_server
        protocol: mcp
        package_path: packages/filesystem-mcp-server
        offer_status: active

      - provider_id: internal-filesystem-http
        provider_type: http_api
        protocol: https
        offer_status: active
```

## Example: open-source tool with multiple providers

```yaml
id: surrealkit
type: tool
name: SurrealKit
capabilities:
  - database.schema.generate
  - database.migration.run
  - database.seed.load

versions:
  - version: 2.2.1
    providers:
      - provider_id: surrealkit-github-release
        provider_type: github_release
        install_strategy: pinned_binary
        version_policy: pinned

      - provider_id: surrealkit-npm
        provider_type: npm_package
        install_strategy: package_manager
        version_policy: pinned

      - provider_id: agennext-ci-wrapper
        provider_type: ci_wrapper
        install_strategy: workflow_script
        version_policy: pinned
```

## Repository responsibilities

Agent-Tools owns:

```text
- tool catalog entries
- capability references used by tools
- version contracts
- provider offer metadata
- external tool definitions
- MCP provider/package metadata where needed
- tool invocation contracts
- tool security, approval, and governance metadata
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

Each file should describe a tool first.

Provider details belong under the specific tool version they support.

### `packages/`

Existing folders under `packages/` are provider implementation packages.

Most current packages are MCP server implementations. They should be migrated conceptually from:

```text
MCP server = catalog item
```

to:

```text
Tool = catalog item
Tool Version = versioned contract
MCP server = provider offer for one or more tool versions
```

Recommended package structure:

```text
packages/<provider-name>/
  provider.yaml          # provider/package metadata
  tools/                 # tool catalog entries exposed through this provider
    <tool-id>.tool.yaml
  src/                   # provider implementation
  package.json
  tsconfig.json
```

## MCP provider model

An MCP server package should declare which tool versions it provides:

```yaml
provider_id: filesystem-mcp-server
provider_type: mcp_server
provides:
  - tool_id: filesystem.read_file
    version: 1.0.0
  - tool_id: filesystem.write_file
    version: 1.0.0
  - tool_id: filesystem.list_directory
    version: 1.0.0
```

Each exposed tool should have a catalog entry with provider offer metadata:

```yaml
id: filesystem.read_file
type: tool
capabilities:
  - file.read
versions:
  - version: 1.0.0
    providers:
      - provider_id: filesystem-mcp-server
        provider_type: mcp_server
        protocol: mcp
risk: medium
approval_required: false
```

## Capability standardization

Capabilities should be stable semantic identifiers.

Examples:

```text
file.read
file.write
filesystem.list
database.query
database.schema.generate
database.migration.run
database.seed.load
cloud.compute.create
cloud.storage.object.read
```

Capabilities allow the platform to compare tools, substitute providers, reason about risk, and match skills to tools.

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
1. Identify the tools exposed by each provider package.
2. Identify capabilities implemented by each tool.
3. Add one .tool.yaml catalog entry per tool.
4. Add versions under each tool.
5. Add provider offers under each version.
6. Add provider.yaml only for package/build/runtime metadata.
7. Mark tool risk, approval requirements, auth, pricing, license, and support metadata where known.
8. Keep implementation under src/.
9. Build and test provider package.
```

## Relationship to other repos

```text
Agent-Skills
  uses tools as executable capabilities

Agent-Graph
  maps tools, capabilities, providers, versions, permissions, and invocations

Agent-Grammar
  validates tool, capability, version, and provider metadata

Agent-Seed
  seeds default platform tool/capability records

Agent-Review
  reviews high-risk tools before publication/use
```

## Rule

```text
Capability
  = semantic ability

Tool
  = catalog product implementing capabilities

Tool Version
  = versioned contract

Provider Offer
  = access path for a specific tool version

MCP Server
  = provider type, not the tool itself
```
