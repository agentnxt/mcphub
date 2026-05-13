# Official Docker Hub MCP Registry Policy

Only official or human-verified Docker Hub sources may be added to this registry.

## Inclusion criteria

- The image is published by the upstream project, project owner, or verified organization.
- The image is referenced by official project documentation, an official repository, or a verified publisher profile.
- The image has a traceable source URL and clear ownership trail.

## Exclusion criteria

- Community images without an official upstream reference.
- Lookalike packages or unclear publisher ownership.
- Images with no source repository or verification notes.

## Proposed registry fields

Each Docker Hub MCP entry should include:

```json
{
  "name": "github-mcp-server",
  "title": "GitHub MCP Server",
  "docker_image": "agentnxt/github-mcp-server",
  "publisher": "agentnxt",
  "source_url": "https://github.com/AGenNext/mcp-registry",
  "dockerhub_url": "https://hub.docker.com/r/agentnxt/github-mcp-server",
  "verification_status": "official",
  "verification_notes": "Published under the verified upstream namespace.",
  "category": "development",
  "tags": ["github", "mcp", "development", "official"]
}
```

## Review requirement

Every imported Docker Hub MCP image must be reviewed before being marked `official`.
