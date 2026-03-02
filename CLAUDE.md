# CLAUDE.md

> Guidelines and context for AI assistants working in this repository.

## Project Overview

**Agency-agenc** is the AI agent toolkit for **Drama Nerd Designs** — a Broadway/musical theatre-themed product brand created by John Howrey. This repo contains brand documentation, specialized AI agents, and actionable playbooks for marketing, content creation, and business strategy.

- **Repository**: `johnhowrey/Agency-agenc`
- **Brand**: Drama Nerd Designs (dramanerddesigns.com)
- **Status**: Active — agents and playbooks ready for use

## Repository Structure

```
Agency-agenc/
├── CLAUDE.md                          # AI assistant guidelines (this file)
├── README.md                          # Usage guide and getting started
├── brand/
│   └── drama-nerd-designs.md          # Brand bible — products, voice, audience, channels
├── agents/
│   ├── brand-strategist.md            # Strategy, positioning, relaunch planning
│   ├── social-media.md                # Instagram content, captions, hashtags
│   ├── product-copywriter.md          # Etsy listings, product descriptions, SEO
│   ├── marketing-calendar.md          # Content calendars, campaigns, seasonal planning
│   └── email-marketing.md             # Newsletters, launch sequences, list building
└── playbooks/
    ├── etsy-relaunch.md               # Step-by-step Etsy shop relaunch guide
    ├── instagram-growth.md            # Instagram growth strategy (57 → 2,000+)
    └── product-launch.md              # Repeatable product launch checklist
```

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

1. **Read the brand bible first**: Before responding to any request, read `brand/drama-nerd-designs.md` for full brand context — products, voice, audience, and channels.
2. **Stay in character**: Each agent has a defined role and voice. Maintain the warm, knowledgeable, theatre-nerd tone described in the brand bible.
3. **Be actionable**: Every response should include something the user can do right now. No vague advice.
4. **Remember the constraints**: This is a one-person operation with a full-time job. Recommendations must be realistic for someone with ~2-3 hours/week to dedicate to the brand.
5. **Reference real products**: When making recommendations, tie them to specific Drama Nerd Designs products (subway map, Oracle cards, tote bags, mugs, wrapping paper).
6. **Respect existing patterns**: When the brand bible establishes a convention, follow it consistently.
7. **Keep this file current**: When you add significant structure (new agents, playbooks, or brand documents), update this CLAUDE.md to reflect the changes.
