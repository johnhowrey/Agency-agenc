# Drama Nerd Designs — AI Agent Toolkit

> Your personal team of AI agents for marketing, content, and strategy — built specifically for Drama Nerd Designs.

## What Is This?

This repository contains a set of specialized AI agents and playbooks tailored to **Drama Nerd Designs**, a Broadway/musical theatre-themed product brand. Instead of starting from scratch every time you need marketing help, these agents already know your brand, your products, your audience, and your voice.

Think of it as having a marketing team on call — a strategist, a social media manager, a copywriter, a calendar planner, and an email marketer — all of whom already understand that the choreographer of *Hamilton* also did *9 to 5*.

## Your Agents

| Agent | File | What It Does |
|-------|------|-------------|
| **Brand Strategist** | `agents/brand-strategist.md` | Big-picture strategy, positioning, pricing, relaunch planning, competitive analysis |
| **Social Media** | `agents/social-media.md` | Instagram captions, Reels concepts, hashtag strategy, content calendars, community engagement |
| **Product Copywriter** | `agents/product-copywriter.md` | Etsy listings, product descriptions, SEO optimization, website copy |
| **Marketing Calendar** | `agents/marketing-calendar.md` | Seasonal campaigns, content scheduling, event-driven marketing, weekly planning |
| **Email Marketing** | `agents/email-marketing.md` | Newsletters, launch sequences, subject lines, list building, customer retention |

## Your Playbooks

| Playbook | File | What It Covers |
|----------|------|---------------|
| **Etsy Relaunch** | `playbooks/etsy-relaunch.md` | Step-by-step guide to reopening the DramaNerdDesigns Etsy shop |
| **Instagram Growth** | `playbooks/instagram-growth.md` | Growing @dramanerddesigns from 57 to 2,000+ followers |
| **Product Launch** | `playbooks/product-launch.md` | Repeatable checklist for launching any new product |

## How to Use

### Quick Start

1. Open a conversation with Claude
2. Reference the agent file for what you need help with
3. Ask your question in plain English

### Example Conversations

**Need Instagram content for the week?**
> "Read `agents/social-media.md` and `brand/drama-nerd-designs.md`, then write me 5 Instagram captions for this week — mix of product and engagement posts."

**Relaunching the Etsy shop?**
> "Read `playbooks/etsy-relaunch.md` and help me plan my first week back on Etsy."

**Writing a product listing?**
> "Read `agents/product-copywriter.md` and write an Etsy listing for the Broadway Oracle cards."

**Planning for the Tony Awards?**
> "Read `agents/marketing-calendar.md` and create a 4-week content plan leading up to the Tony Awards."

**Sending a newsletter?**
> "Read `agents/email-marketing.md` and write this month's newsletter. Tony nominations just came out."

**Need strategic advice?**
> "Read `agents/brand-strategist.md` and help me decide whether to add a new product line of Broadway-themed greeting cards."

## The Brand Bible

All agents reference `brand/drama-nerd-designs.md` — the comprehensive brand document that contains:

- Brand identity, voice, and personality guidelines
- Complete product catalog with specs and pricing
- Target audience profiles
- Sales channel overview
- Competitive advantages
- Key marketing dates (Tony Awards, Sondheim's birthday, Broadway Week, etc.)

**If you update your products, pricing, or brand direction, update the brand bible first** — all agents pull from it.

## Products (Current Focus)

| Product | Price Range | Notes |
|---------|-------------|-------|
| Broadway Tote Bags (3 sizes) | ~$36 | Top seller, 300+ five-star reviews |
| The Broadway Oracle (100 cards) | TBD | Newest product |
| The Broadway Map Mug (15oz) | TBD | Great add-on / bundle item |

> **Note**: Shop goes on hiatus mid-April 2026. Other products (subway map poster, wrapping paper, Sondheim mug) are in the catalog but not the current focus.

## Shop Automation

The `automation/` directory contains Python scripts that automate Etsy shop operations:

```bash
# Start watching for new orders (sends email + generates packing slips)
python -m automation.order_monitor

# Create a listing from pre-written copy
python -m automation.listing_manager create tote-regular

# Generate a packing slip for a specific order
python -m automation.packing_slip <receipt_id>

# Test email notifications
python -m automation.notify
```

See [`automation/README.md`](automation/README.md) for full setup instructions.

## Channels

| Channel | URL | Status |
|---------|-----|--------|
| Website | [dramanerddesigns.com](https://www.dramanerddesigns.com) | Active |
| Etsy | [etsy.com/shop/DramaNerdDesigns](https://www.etsy.com/shop/DramaNerdDesigns) | Relaunch planned |
| Instagram | [@dramanerddesigns](https://www.instagram.com/dramanerddesigns/) | Active (growing) |
| Society6 | Puzzles | Active |
| BWAYX | Digital collectibles | Active |

---

*Built with love for musical theatre and the belief that every theatre nerd deserves a marketing team that gets it.*
