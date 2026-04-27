# Contributing to MCPHub

Thank you for your interest in contributing to MCPHub by AgentNxt! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Creating a New MCP Server](#creating-a-new-mcp-server)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Docker Deployment](#docker-deployment)

---

## Code of Conduct

We are committed to providing a welcoming and respectful environment. Please:

- Be kind and considerate in your communications
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show courtesy towards differing viewpoints

---

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mcp-registry.git
   cd mcp-registry
   ```
3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/agentnxt/mcp-registry.git
   ```

---

## Development Setup

### Prerequisites

- Node.js 18+ (LTS recommended)
- npm 9+
- Docker (for containerization)
- Git

### Install Dependencies

```bash
# Install all dependencies for all servers
npm install

# Or install for a single server
cd <server-name>
npm install
```

### Build Servers

```bash
# Build all servers
npm run build

# Build a specific server
cd <server-name>
npm run build
```

---

## Creating a New MCP Server

### 1. Create Directory Structure

Create a new directory with the following structure:

```
<service-name>-mcp-server/
├── src/
│   ├── index.ts           # Main entry point
│   ├── client.ts          # API client (if needed)
│   ├── types.ts           # Type definitions
│   └── tools/
│       ├── index.ts       # Tool exports
│       └── *.ts           # Individual tool files
├── Dockerfile             # Multi-stage Docker build
├── package.json
├── tsconfig.json
├── README.md
└── LICENSE (if applicable)
```

### 2. Required Files

#### package.json

```json
{
  "name": "@agentnxt/<service-name>-mcp-server",
  "version": "1.0.0",
  "description": "MCP server for <service-name>",
  "type": "module",
  "bin": {
    "mcp-server-<service>": "dist/index.js"
  },
  "scripts": {
    "build": "tsc && chmod +x dist/*.js",
    "watch": "tsc --watch",
    "test": "vitest run"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@types/node": "^22",
    "typescript": "^5.0.0"
  }
}
```

#### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

#### Dockerfile

```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install --ignore-scripts

COPY tsconfig.json ./
COPY src ./src

RUN npm run build

# Production stage
FROM node:20-alpine AS runner

WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules

# Run as non-root user
RUN addgroup -S mcp && adduser -S mcp -G mcp
USER mcp

ENTRYPOINT ["node", "dist/index.js"]
```

### 3. Server Implementation

Follow the MCP SDK pattern:

```typescript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  { name: "my-mcp-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "my_tool",
      description: "Description of what the tool does",
      inputSchema: {
        type: "object",
        properties: {
          param: { type: "string", description: "Parameter description" }
        },
        required: ["param"]
      }
    }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  // Handle tool calls here
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("My MCP Server running on stdio");
}

main().catch(console.error);
```

### 4. Update CI/CD

Add your server to the matrix in `.github/workflows/docker-push.yml`:

```yaml
jobs:
  build-matrix:
    strategy:
      matrix:
        server:
          # ... existing servers ...
          - my-new-mcp-server  # Add this line
```

---

## Code Style

### TypeScript Guidelines

- Use TypeScript strict mode
- Avoid `any` type - use `unknown` when type is truly unknown
- Use explicit return types for exported functions
- Prefer `const` over `let`
- Use async/await over raw promises
- Handle errors with proper error types

### Naming Conventions

- **Files**: kebab-case (`my-file.ts`)
- **Classes**: PascalCase (`MyClass`)
- **Functions**: camelCase (`myFunction`)
- **Constants**: UPPER_SNAKE_CASE (`MY_CONSTANT`)
- **Types/Interfaces**: PascalCase (`MyType`)

### Import Order

1. Built-in Node.js modules
2. External packages (npm)
3. Internal modules (local)
4. Type imports

---

## Testing

### Writing Tests

```typescript
import { describe, it, expect } from 'vitest';

describe('MyService', () => {
  it('should do something', () => {
    expect(true).toBe(true);
  });
});
```

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run with coverage
npm run test:coverage
```

---

## Documentation

### README Requirements

Each server should have a README.md with:

1. **Description**: What the server does
2. **Installation**: How to install/setup
3. **Configuration**: Environment variables required
4. **Usage**: Examples of how to use the tools
5. **Tools**: List of all available tools with descriptions

### Example README Structure

```markdown
# Service Name MCP Server

Brief description of what this MCP server provides.

## Installation

### Docker

```bash
docker run agentnxt/service-mcp-server
```

### Manual

```bash
npm install
npm run build
```

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `API_KEY` | Yes | Your API key |
| `API_URL` | No | Custom API URL |

## Tools

### `tool_name`

Description of what this tool does.

**Parameters:**
- `param1` (string, required): Description
- `param2` (number, optional): Description

**Example:**
```json
{
  "param1": "value"
}
```
```

---

## Submitting Changes

### Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and commit:
   ```bash
   git add .
   git commit -m "Add: description of changes"
   ```

3. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Open a Pull Request** with:
   - Clear title and description
   - Link to related issues
   - Screenshots/examples if applicable

### Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `Add` - New feature
- `Fix` - Bug fix
- `Update` - Update existing feature
- `Refactor` - Code refactoring
- `Docs` - Documentation changes
- `Chore` - Maintenance tasks

### Review Process

1. Maintainers will review your PR
2. Address any feedback/comments
3. Once approved, your PR will be merged

---

## Docker Deployment

### Building Locally

```bash
# Build the image
docker build -t agentnxt/my-server ./my-server

# Run with environment variables
docker run -d \
  -e API_KEY="your-key" \
  agentnxt/my-server
```

### Using Docker Compose

```yaml
services:
  my-server:
    image: agentnxt/my-server
    environment:
      - API_KEY=${API_KEY}
    restart: unless-stopped
```

### Image Registry

All images are automatically built and pushed to Docker Hub via GitHub Actions on merge to main.

---

## Questions?

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Be descriptive in your issue reports

---

Thank you for contributing to MCPHub! 🚀