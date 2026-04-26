# AgentNxt MCP Registry Schema.org Profile

The AgentNxt MCP Registry uses Schema.org as a public semantic baseline, while AgentNxt controls the MCP registry profile, extension vocabulary, publishing workflow, deployment metadata, trust model, and identity-resolution rules.

This profile is intentionally permissive and incrementally enrichable. Registry entries may start with a small amount of metadata and gain additional Schema.org and `mcp.*` metadata over time.

## Design principles

- Use Schema.org fields when they fit the concept.
- Use AgentNxt `mcp.*` fields only for MCP-specific registry metadata.
- Do not make fields mandatory by default.
- Treat canonical identity, provenance, trust, and deployment metadata as separate concepts.
- Prefer publisher-controlled canonical URLs for MCP server identity.
- Use `isBasedOn` for forks, wrappers, clones, and derivative projects.
- Use `sameAs` only for equivalent identities that describe the same entity.

## Core Schema.org types

| Concept | Schema.org type | Purpose |
|---|---|---|
| MCP server artifact or hosted app | `WebApplication` | Describes the runnable MCP server or app artifact. |
| Hosted MCP API surface | `WebAPI` | Describes the API/service exposed over HTTP, SSE, or Streamable HTTP. |
| API docs or reference | `APIReference` | Describes documentation/reference material for the API. |
| Concrete API endpoint | `EntryPoint` | Describes a deployed endpoint such as `/mcp`. |
| Publisher, maintainer, or provider | `Organization` / `Person` | Describes who provides or publishes the server. |

## Schema.org validation workflow

Use Schema.org Markup Validator to validate the public Schema.org layer of a registry entry.

The validator can validate structured data by fetching a page URL or by accepting pasted markup. It extracts JSON-LD, RDFa, and Microdata; displays the extracted structured data graph; and identifies syntax mistakes. It is focused on Schema.org, so it should not be treated as the only validator for AgentNxt `mcp.*` extension fields.

### What to validate with Schema.org Markup Validator

Validate these fields and shapes:

- JSON-LD syntax
- `@context`
- `@type`
- `WebApplication`
- `WebAPI`
- `APIReference`
- `EntryPoint`
- `isBasedOn`
- `sameAs`
- `provider`
- `softwareRequirements`
- `runtimePlatform`
- `license`
- `documentation`
- `potentialAction`

### What not to expect from Schema.org Markup Validator

Do not expect the Schema.org validator to fully validate AgentNxt-specific fields such as:

- `mcp.canonicalId`
- `mcp.authority`
- `mcp.trust`
- `mcp.transports`
- `mcp.deployment`
- `mcp.auth`

Those are AgentNxt extension fields. Validate their shape with `registry/schema.json` and registry tooling.

### Manual validation steps

1. Copy a registry entry JSON object.
2. Wrap it in an HTML page as JSON-LD:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Schema.org validation fixture</title>
    <script type="application/ld+json">
    {
      "@context": {
        "@vocab": "https://schema.org/",
        "mcp": "https://agentnxt.dev/ns/mcp#"
      },
      "@type": "WebApplication",
      "name": "Example MCP Server",
      "mcp": {
        "canonicalId": "https://github.com/example/example-mcp-server"
      }
    }
    </script>
  </head>
  <body></body>
</html>
```

3. Paste the HTML into Schema.org Markup Validator.
4. Confirm the Schema.org graph extracts cleanly.
5. Review any warnings or type/value mismatches.
6. Validate the same raw JSON file with `registry/schema.json` for AgentNxt profile checks.

### Recommended validation levels

| Level | Tool | Purpose |
|---|---|---|
| JSON syntax | `python -m json.tool` | Confirms registry entry is valid JSON. |
| AgentNxt profile | `registry/schema.json` | Confirms known AgentNxt and Schema.org-profile fields have expected shapes when present. |
| Schema.org graph | Schema.org Markup Validator | Confirms JSON-LD extracts as Schema.org structured data. |
| Registry semantics | human review / registry tooling | Confirms canonical ID, provenance, trust, and derivation semantics are correct. |

### Example validation fixture for WebApplication + WebAPI + APIReference

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Google Analytics MCP validation fixture</title>
    <script type="application/ld+json">
    {
      "@context": {
        "@vocab": "https://schema.org/",
        "mcp": "https://agentnxt.dev/ns/mcp#"
      },
      "@type": "WebApplication",
      "@id": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server",
      "name": "AgentNxt Google Analytics MCP Wrapper",
      "url": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server",
      "isBasedOn": "https://github.com/googleanalytics/google-analytics-mcp",
      "applicationCategory": "DeveloperApplication",
      "applicationSubCategory": "MCP Server",
      "runtimePlatform": ["Python 3.10+", "Docker", "Google Cloud Run"],
      "softwareRequirements": [
        "analytics-mcp",
        "mcp-proxy",
        "Google Analytics Admin API",
        "Google Analytics Data API"
      ],
      "subjectOf": {
        "@type": "WebAPI",
        "@id": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server#api",
        "name": "Google Analytics MCP API",
        "serviceType": "MCP Streamable HTTP API",
        "documentation": {
          "@type": "APIReference",
          "@id": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server#api-reference",
          "url": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server#readme"
        },
        "potentialAction": {
          "@type": "Action",
          "target": {
            "@type": "EntryPoint",
            "urlTemplate": "https://example.run.app/mcp",
            "httpMethod": "POST",
            "encodingType": "application/json",
            "contentType": "application/json"
          }
        }
      },
      "mcp": {
        "canonicalId": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server"
      }
    }
    </script>
  </head>
  <body></body>
</html>
```

## Identity model

The registry separates three identity layers:

| Field | Owner | Meaning |
|---|---|---|
| `mcp.canonicalId` | Software publisher or wrapper publisher | Stable identity for this exact MCP server artifact. Prefer a publisher-controlled URL. |
| `@id` | Metadata publisher | JSON-LD identifier for the described entity in this record. Usually same as `mcp.canonicalId`. |
| `mcp.id` | AgentNxt registry | Local registry slug or legacy ID. Not the canonical identity. |
| `mcp.aliases` | AgentNxt registry | Search aliases, old IDs, package names, or alternate names. |

Recommended identity pattern:

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "mcp": "https://agentnxt.dev/ns/mcp#"
  },
  "@type": "WebApplication",
  "@id": "https://github.com/example/example-mcp-server",
  "url": "https://github.com/example/example-mcp-server",
  "name": "Example MCP Server",
  "mcp": {
    "canonicalId": "https://github.com/example/example-mcp-server",
    "id": "example-mcp-server",
    "aliases": [
      "example-mcp",
      "example-server"
    ]
  }
}
```

## Publisher-controlled canonical URLs

A canonical ID should be globally unique, stable, and controlled by the publisher of the software artifact.

Good examples:

```text
https://github.com/googleanalytics/google-analytics-mcp
https://developers.google.com/analytics/mcp/google-analytics
did:web:example.com:mcp:servers:analytics
```

Avoid using a registry-local slug as the canonical ID:

```text
google-analytics-mcp-server
```

Use local slugs under `mcp.id` instead.

## Official upstream server

An official upstream server should use the upstream publisher-controlled URL as its canonical identity.

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "mcp": "https://agentnxt.dev/ns/mcp#"
  },
  "@type": "WebApplication",
  "@id": "https://github.com/googleanalytics/google-analytics-mcp",
  "name": "Google Analytics MCP Server",
  "url": "https://github.com/googleanalytics/google-analytics-mcp",
  "provider": {
    "@type": "Organization",
    "name": "Google Analytics"
  },
  "mcp": {
    "canonicalId": "https://github.com/googleanalytics/google-analytics-mcp",
    "id": "google-analytics-mcp-server",
    "publisherDomain": "github.com",
    "source": {
      "type": "upstream",
      "url": "https://github.com/googleanalytics/google-analytics-mcp",
      "package": "analytics-mcp"
    }
  }
}
```

## AgentNxt wrapper around upstream software

A wrapper is a different software artifact, so it gets its own canonical ID. The upstream project is linked with `isBasedOn`, not `sameAs`.

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "mcp": "https://agentnxt.dev/ns/mcp#"
  },
  "@type": "WebApplication",
  "@id": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server",
  "name": "AgentNxt Google Analytics MCP Wrapper",
  "url": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server",
  "isBasedOn": "https://github.com/googleanalytics/google-analytics-mcp",
  "provider": {
    "@type": "Organization",
    "name": "AgentNxt",
    "url": "https://github.com/agentnxt"
  },
  "mcp": {
    "canonicalId": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server",
    "upstreamCanonicalId": "https://github.com/googleanalytics/google-analytics-mcp",
    "id": "google-analytics-mcp-server",
    "source": {
      "type": "container",
      "url": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server"
    }
  }
}
```

## Forks, clones, mirrors, and wrappers

Use `isBasedOn` for derivation relationships.

| Relationship | Canonical ID | Relationship field |
|---|---|---|
| Official upstream | Upstream publisher URL | none |
| Official mirror by same publisher | Publisher-controlled mirror URL | `sameAs` may be used if it is truly the same entity |
| Community fork | Fork maintainer URL | `isBasedOn` upstream |
| Clone or mirror | Clone/mirror maintainer URL | `isBasedOn` upstream |
| AgentNxt wrapper | AgentNxt wrapper URL | `isBasedOn` upstream |

Example fork:

```json
{
  "@type": "WebApplication",
  "@id": "https://github.com/community/google-analytics-mcp-fork",
  "name": "Community Google Analytics MCP Fork",
  "isBasedOn": "https://github.com/googleanalytics/google-analytics-mcp",
  "mcp": {
    "canonicalId": "https://github.com/community/google-analytics-mcp-fork",
    "upstreamCanonicalId": "https://github.com/googleanalytics/google-analytics-mcp",
    "id": "community-google-analytics-mcp-fork"
  }
}
```

## `sameAs` vs `isBasedOn`

Use `sameAs` only when two URLs describe the same entity.

Use `isBasedOn` when a project is derived from another project.

```json
{
  "sameAs": [
    "https://example.com/official-page-for-same-server"
  ],
  "isBasedOn": [
    "https://github.com/original/upstream-mcp-server"
  ]
}
```

Do not use `sameAs` for forks, wrappers, clones, or rewritten derivatives.

## API modeling

For hosted MCP deployments, model the server, API, documentation, and endpoint separately.

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "mcp": "https://agentnxt.dev/ns/mcp#"
  },
  "@type": "WebApplication",
  "@id": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server",
  "name": "AgentNxt Google Analytics MCP Wrapper",
  "subjectOf": {
    "@type": "WebAPI",
    "@id": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server#api",
    "name": "Google Analytics MCP API",
    "serviceType": "MCP Streamable HTTP API",
    "documentation": {
      "@type": "APIReference",
      "@id": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server#api-reference",
      "url": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server#readme"
    },
    "potentialAction": {
      "@type": "Action",
      "target": {
        "@type": "EntryPoint",
        "urlTemplate": "https://example.run.app/mcp",
        "httpMethod": "POST",
        "encodingType": "application/json",
        "contentType": "application/json"
      }
    }
  },
  "mcp": {
    "canonicalId": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server",
    "api": {
      "@type": "WebAPI",
      "@id": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server#api"
    },
    "apiReference": {
      "@type": "APIReference",
      "@id": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server#api-reference"
    },
    "endpoints": [
      {
        "@type": "EntryPoint",
        "urlTemplate": "https://example.run.app/mcp",
        "httpMethod": "POST",
        "contentType": "application/json"
      }
    ]
  }
}
```

## Runtime and dependency modeling

Use Schema.org fields first:

| Concept | Field |
|---|---|
| Runtime platform | `runtimePlatform` |
| Operating system | `operatingSystem` |
| Programming language | `programmingLanguage` |
| Required packages, SDKs, APIs, services | `softwareRequirements` |
| Deployment or installation page | `installUrl` |
| Downloadable package or image | `downloadUrl` |
| API docs | `APIReference` |

Example:

```json
{
  "@type": "WebApplication",
  "runtimePlatform": [
    "Python 3.10+",
    "Docker",
    "Google Cloud Run"
  ],
  "programmingLanguage": "Python",
  "softwareRequirements": [
    "analytics-mcp",
    "mcp-proxy",
    "Google Analytics Admin API",
    "Google Analytics Data API"
  ]
}
```

Avoid creating MCP-specific fields such as `mcp.frameworks`, `mcp.sdks`, or `mcp.toolkits` unless the AgentNxt vocabulary explicitly adopts them through the field proposal process.

## Domain authority and trust

The publisher-controlled domain is the authority anchor for identity. Trust is a registry evaluation layer, not an identity field.

```json
{
  "mcp": {
    "canonicalId": "https://developers.google.com/analytics/mcp/google-analytics",
    "publisherDomain": "developers.google.com",
    "authority": {
      "domain": "developers.google.com",
      "canonicalUrl": "https://developers.google.com/analytics/mcp/google-analytics",
      "verificationMethod": "publisher-controlled-canonical-url",
      "evidence": [
        "https://developers.google.com/analytics/mcp/google-analytics"
      ]
    },
    "trust": {
      "score": 0.98,
      "level": "official",
      "publisherDomain": "developers.google.com",
      "domainRelationship": "official"
    }
  }
}
```

Suggested trust levels:

| Level | Meaning |
|---|---|
| `official` | Canonical ID is controlled by the upstream publisher. |
| `verified` | Evidence supports the publisher relationship, but the canonical URL may be on a delegated platform such as GitHub. |
| `community` | Maintained by a community or third party. |
| `mirror` | Mirrors upstream but is not the authoritative source. |
| `unverified` | Insufficient evidence. |
| `disputed` | Conflicting evidence or ownership concerns. |

## Provenance

Provenance means origin, ownership, and evidence chain.

```json
{
  "mcp": {
    "canonicalId": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server",
    "upstreamCanonicalId": "https://github.com/googleanalytics/google-analytics-mcp",
    "provenance": {
      "sourceType": "wrapper",
      "relationship": "agentnxt-packaged-wrapper",
      "publisher": "AgentNxt",
      "upstreamPublisher": "Google Analytics",
      "evidence": [
        "Dockerfile installs analytics-mcp",
        "README links to upstream Google Analytics MCP repo"
      ]
    }
  }
}
```

Provenance can inform trust scoring, but provenance fields should not automatically imply endorsement.

## Field governance

AgentNxt controls the registry profile. Schema.org is inherited as a semantic baseline, not a dependency that blocks registry evolution.

When proposing new fields:

1. Check if Schema.org already has a suitable field.
2. Use the Schema.org field if the semantics match.
3. If the concept is MCP-specific, propose an AgentNxt extension under `mcp.*`.
4. Keep fields optional unless a separate migration plan exists.
5. Document examples and relationships to existing fields.
6. Avoid changing the meaning of adopted fields.

## Minimal valid partial record

Because the schema is permissive, even a partial record can be valid and enriched later.

```json
{
  "@type": "WebApplication",
  "name": "Example MCP Server",
  "mcp": {
    "canonicalId": "https://github.com/example/example-mcp-server"
  }
}
```

## Recommended complete record

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "mcp": "https://agentnxt.dev/ns/mcp#"
  },
  "@type": "WebApplication",
  "@id": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server",
  "name": "AgentNxt Google Analytics MCP Wrapper",
  "description": "Remote-ready wrapper for the Google Analytics MCP server.",
  "url": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server",
  "sameAs": [
    "https://github.com/googleanalytics/google-analytics-mcp"
  ],
  "isBasedOn": [
    "https://github.com/googleanalytics/google-analytics-mcp"
  ],
  "applicationCategory": "DeveloperApplication",
  "applicationSubCategory": "MCP Server",
  "runtimePlatform": [
    "Python 3.10+",
    "Docker",
    "Google Cloud Run"
  ],
  "programmingLanguage": "Python",
  "softwareRequirements": [
    "analytics-mcp",
    "mcp-proxy",
    "Google Analytics Admin API",
    "Google Analytics Data API"
  ],
  "featureList": [
    "Account summaries",
    "Property details",
    "GA4 reports",
    "Realtime reports"
  ],
  "installUrl": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server#readme",
  "license": "Apache-2.0",
  "provider": {
    "@type": "Organization",
    "name": "AgentNxt",
    "url": "https://github.com/agentnxt"
  },
  "mcp": {
    "canonicalId": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server",
    "upstreamCanonicalId": "https://github.com/googleanalytics/google-analytics-mcp",
    "id": "google-analytics-mcp-server",
    "aliases": [
      "analytics-mcp",
      "google-analytics-mcp"
    ],
    "publisherDomain": "github.com",
    "transports": [
      "stdio",
      "streamable-http"
    ],
    "source": {
      "type": "container",
      "url": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server"
    },
    "authority": {
      "domain": "github.com",
      "canonicalUrl": "https://github.com/agentnxt/mcp-registry/tree/main/google-analytics-mcp-server",
      "verificationMethod": "registry-maintained-wrapper"
    },
    "trust": {
      "score": 0.8,
      "level": "verified",
      "publisherDomain": "github.com",
      "domainRelationship": "registry-maintained-wrapper"
    }
  }
}
```
