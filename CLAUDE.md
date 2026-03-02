# CLAUDE.md

> Guidelines and context for AI assistants working in this repository.

## Project Overview

**Agency-agenc** is a newly initialized repository. This document establishes foundational conventions and will be updated as the project evolves.

- **Repository**: `johnhowrey/Agency-agenc`
- **Status**: Initial setup

## Repository Structure

```
Agency-agenc/
├── CLAUDE.md          # AI assistant guidelines (this file)
└── .git/              # Git metadata
```

> **Note**: This project is in its initial phase. Update this section as source code, configuration, and documentation are added.

## Development Workflow

### Git Conventions

- **Default branch**: `main` (to be established with the first commit)
- **Feature branches**: Use descriptive names prefixed by category (e.g., `feature/`, `fix/`, `docs/`)
- **Commit messages**: Use clear, imperative-mood messages (e.g., "Add user authentication module")
- Keep commits focused and atomic — one logical change per commit

### Code Style

- Follow the conventions of whichever language(s) are adopted for this project
- Use consistent formatting; prefer automated formatters when available
- Write self-documenting code; add comments only where intent is non-obvious

### Testing

- Add tests alongside new functionality
- Run the full test suite before committing (update this section with the actual test command once established)

### Pull Requests

- Provide a clear title and description
- Reference related issues when applicable
- Ensure CI passes before requesting review

## Instructions for AI Assistants

1. **Read before writing**: Always read existing files before proposing edits. Understand the surrounding code and conventions first.
2. **Minimal changes**: Make only the changes that are requested or clearly necessary. Avoid unrelated refactors, extra comments, or speculative features.
3. **No over-engineering**: Prefer simple, direct solutions. Don't add abstractions, feature flags, or extensibility that isn't needed right now.
4. **Security first**: Never introduce credentials, secrets, or known vulnerabilities. Validate at system boundaries.
5. **Respect existing patterns**: When the codebase establishes a pattern, follow it consistently rather than introducing alternatives.
6. **Test your changes**: Run available linters and tests after making changes. Fix any issues you introduce.
7. **Keep this file current**: When you add significant structure (new directories, build tools, CI pipelines, dependencies), update this CLAUDE.md to reflect the changes.
