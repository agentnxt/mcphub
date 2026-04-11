# Cloud/Hosted MCP Servers

Remote MCP servers hosted by SaaS providers. These can be registered in MetaMCP as SSE/Streamable HTTP endpoints — no local process needed. Customers connect via OAuth and get instant access to the provider's tools.

## Available Cloud MCP Servers

| Provider | Endpoint URL | Auth | Transport | Notes |
|----------|-------------|------|-----------|-------|
| **Notion** | `https://mcp.notion.com/sse` | OAuth 2.1 | SSE + Streamable HTTP | Workspaces, pages, databases, search, comments |
| **Cloudflare** | `https://mcp.cloudflare.com/sse` | OAuth | Streamable HTTP + SSE | Workers, KV, R2, D1, DNS, analytics. Also has product-specific endpoints: `observability.mcp.cloudflare.com`, `bindings.mcp.cloudflare.com` |
| **Sentry** | `https://mcp.sentry.dev/sse` | OAuth | Streamable HTTP (SSE fallback) | Error tracking, issues, events, releases, performance |
| **Linear** | `https://mcp.linear.app/sse` | OAuth / API Key | Streamable HTTP | Issues, projects, cycles, teams. Only one that accepts plain API key as Bearer token |
| **Stripe** | `https://mcp.stripe.com/sse` | OAuth | Streamable HTTP + SSE | Payments, customers, subscriptions, invoices, products |
| **Figma** | `https://mcp.figma.com/sse` | OAuth | Streamable HTTP | Design files, components, styles, variables. Requires Dev Mode seat for full access |
| **Netlify** | `https://netlify-mcp.netlify.app/sse` | OAuth 2.1 | Streamable HTTP (stateless) | Sites, deploys, builds, DNS, forms, serverless functions |
| **Slack** | `https://mcp.slack.com/sse` | OAuth | Streamable HTTP only | Channels, messages, users, reactions. No SSE support, no Dynamic Client Registration |

## Not Available as Remote Endpoints

| Provider | Status | Alternative |
|----------|--------|-------------|
| **Perplexity** | Local stdio only (`npx @perplexity-ai/mcp-server`) | Self-host via Docker, expose as SSE |
| **Shopify** | Per-store only (`https://{store}.myshopify.com/api/mcp`) | Register individual store endpoints |

## How to Register in MetaMCP

1. Go to MetaMCP UI at `https://mcp.agnxxt.com`
2. Add Server → Type: **SSE**
3. Enter the endpoint URL from the table above
4. Complete the OAuth flow when prompted
5. Enable/disable individual tools per customer namespace

## Auth Notes

- All cloud MCP servers use **OAuth 2.1** flows
- MetaMCP handles OAuth token acquisition and refresh
- **Linear** is the most flexible — also accepts a static API key as `Authorization: Bearer {key}`
- **Slack** requires a registered Slack app with client ID (not just a bot token)
- **Figma** requires a Figma account with Dev Mode seat for full design access
- **Cloudflare** has multiple product-specific endpoints that can be registered separately

## Endpoint URL Patterns

Most providers follow the convention:
- `https://mcp.{provider}.com/sse` — SSE transport
- `https://mcp.{provider}.com/mcp` — Streamable HTTP transport

MetaMCP's SSE server type handles both. Use the `/sse` URLs listed above.
