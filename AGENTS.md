# Repository Agent Instructions

Scope: entire repository.

This repository follows the shared OpenAutonomyX instruction layer in `openautonomyx/common-instructions` and is scoped to MCP registry documentation, metadata, and operational guidance.

## Documentation-only alignment rule

For documentation alignment tasks, update README files, docs, examples, registry metadata, and repo-level guidance only. Do not change implementation code unless a human maintainer explicitly requests it.

## Shared references

Use these shared references as the default baseline:

- `standards/engineering-execution-standard.md`
- `policies/context-and-guardrails-policy.md`
- `policies/test-and-process-improvement-policy.md`
- `policies/airgapped-operation-policy.md`

Do not duplicate shared policies here. Reference them and add only MCP-registry-specific guidance.

## In scope

- MCP server registry documentation
- Server metadata conventions
- Tool descriptions and usage examples
- Compatibility and deployment notes
- Review notes for substantial registry changes

## Out of scope

- Organization-level vision or strategy source documents
- Generic shared prompt packs
- Product implementation details owned by another repository
- Large private datasets or binary model artifacts unless explicitly approved

## Documentation rules

1. Keep server and tool entries clear, discoverable, and version-aware.
2. Document inputs, outputs, authentication, permissions, risks, and examples.
3. Include compatibility and review notes for production-facing servers.
4. Prefer small, composable docs over large monolithic files.
5. Record substantial registry changes in `reviews/` when applicable.
6. Require reviewer approval and HITL sign-off before production-facing MCP behavior changes.
