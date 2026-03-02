# Drama Nerd Designs — Shop Automation

> Automate Etsy listings, order notifications, and packing slips so all you have to do is pack and ship.

## What This Does

| Module | What It Does |
|--------|-------------|
| `etsy_client.py` | Connects to Etsy API v3 — handles auth, listings, and orders |
| `order_monitor.py` | Watches for new orders, sends you an email, generates a packing slip |
| `listing_manager.py` | Creates Etsy listings from pre-written copy (tote bags, Oracle, mug) |
| `packing_slip.py` | Generates printable HTML packing slips with order details |
| `notify.py` | Sends order notification emails via Gmail |

## Setup (One Time)

### 1. Install dependencies

```bash
cd automation
pip install -r requirements.txt
```

### 2. Configure credentials

Copy `.env.template` to `.env` and fill in your values:

```bash
cp .env.template .env
```

You need:
- **Etsy API Key + Shared Secret** — from etsy.com/developers
- **Gmail App Password** — from Google Account → Security → App Passwords
- **Your Etsy Shop ID** — the numeric ID (we can find this after authorization)

### 3. Authorize with Etsy

```bash
python -m automation.etsy_client
```

This opens your browser. Log in to Etsy and authorize the app. Tokens are saved locally and auto-refresh.

### 4. Test email notifications

```bash
python -m automation.notify
```

This sends a test email to john@musicaltheatrehistory.com.

## Daily Use

### Start the order monitor

```bash
python -m automation.order_monitor
```

Leave this running. When a new order comes in:
1. You get an email with order details and shipping address
2. A packing slip HTML file is generated in `output/`
3. Open the packing slip in your browser → Print (Cmd+P)
4. Pack the order
5. Buy the shipping label on Etsy
6. Ship it

### Create listings

See available listing templates:
```bash
python -m automation.listing_manager templates
```

Create a listing:
```bash
python -m automation.listing_manager create tote-regular
python -m automation.listing_manager create oracle
python -m automation.listing_manager create mug
```

View active listings:
```bash
python -m automation.listing_manager list
```

### Generate a packing slip manually

```bash
python -m automation.packing_slip <receipt_id>
```

## Available Listing Templates

| Key | Product | Price |
|-----|---------|-------|
| `tote-regular` | Broadway Tote Bag (Regular) | $36.00 |
| `tote-xl` | Broadway Tote Bag (XL, crossbody) | $36.00 |
| `tote-tiny` | Broadway Tote Bag (Tiny) | $36.00 |
| `oracle` | Broadway Oracle Cards (100 cards) | $25.00 |
| `mug` | Broadway Map Mug (15oz) | $20.00 |

> **Note**: After creating a listing, you still need to add product photos and set the shipping profile on Etsy.

## Still Need to Fill In

After setup, these blanks remain in your `.env`:

- [ ] `ETSY_SHOP_ID` — your numeric shop ID
- [ ] `GMAIL_ADDRESS` — your Gmail address for sending notifications
- [ ] `GMAIL_APP_PASSWORD` — 16-character app password from Google
- [ ] `SHIP_FROM_STREET` — your Palm Springs street address
- [ ] `SHIP_FROM_ZIP` — your zip code
