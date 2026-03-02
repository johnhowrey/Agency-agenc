"""
Order monitor for Drama Nerd Designs.

Polls Etsy for new orders and sends email notifications + generates
packing slips automatically. Run this in the background while the
shop is active.
"""

import os
import sys
import time
import json
from datetime import datetime

from dotenv import load_dotenv

from automation.etsy_client import EtsyClient
from automation.notify import send_order_notification
from automation.packing_slip import generate_packing_slip

load_dotenv()

SEEN_FILE = os.path.join(os.path.dirname(__file__), "seen_orders.json")


def load_seen_orders():
    """Load the set of already-processed receipt IDs."""
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    return set()


def save_seen_orders(seen):
    """Persist the set of processed receipt IDs."""
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def check_for_new_orders(client, seen):
    """Check for new orders and process any unseen ones."""
    receipts_resp = client.get_receipts(limit=25)
    results = receipts_resp.get("results", []) if receipts_resp else []
    new_count = 0

    for receipt in results:
        receipt_id = str(receipt.get("receipt_id", ""))
        if not receipt_id or receipt_id in seen:
            continue

        # New order found
        new_count += 1
        buyer_name = receipt.get("name", "Someone")
        print(f"\n{'='*50}")
        print(f"NEW ORDER: #{receipt_id} from {buyer_name}")
        print(f"{'='*50}")

        # Get transaction details for the notification
        try:
            txns = client.get_receipt_transactions(receipt_id)
            items = txns.get("results", []) if txns else []
        except Exception:
            items = []

        order_data = {
            "receipt_id": receipt_id,
            "name": buyer_name,
            "items": [
                {"title": t.get("title", "?"), "quantity": t.get("quantity", 1)}
                for t in items
            ],
            "grandtotal": receipt.get("grandtotal", {}),
            "shipping_address": receipt.get("shipping_address", {}),
            "message_from_buyer": receipt.get("message_from_buyer", ""),
            "is_gift": receipt.get("is_gift", False),
        }

        # Send notification
        try:
            send_order_notification(order_data)
        except Exception as e:
            print(f"  Warning: Could not send email — {e}")

        # Generate packing slip
        try:
            generate_packing_slip(receipt_id)
        except Exception as e:
            print(f"  Warning: Could not generate packing slip — {e}")

        seen.add(receipt_id)

    return new_count


def run_monitor():
    """Main loop: poll for orders on an interval."""
    poll_interval = int(os.getenv("POLL_INTERVAL", "300"))
    print("=" * 50)
    print("Drama Nerd Designs — Order Monitor")
    print("=" * 50)
    print(f"Checking every {poll_interval} seconds")
    print(f"Notifications → {os.getenv('NOTIFICATION_EMAIL')}")
    print(f"Press Ctrl+C to stop\n")

    client = EtsyClient()

    # Verify connection
    try:
        shop = client.get_shop()
        print(f"Connected to: {shop.get('shop_name', 'your shop')}")
    except Exception as e:
        print(f"Error connecting to Etsy: {e}")
        print("Run 'python -m automation.etsy_client' to authorize first.")
        sys.exit(1)

    seen = load_seen_orders()
    print(f"Tracking {len(seen)} previously seen orders")

    # On first run, mark all current orders as seen (don't re-notify)
    if not seen:
        print("First run — marking existing orders as seen...")
        check_result = client.get_receipts(limit=100)
        results = check_result.get("results", []) if check_result else []
        for r in results:
            seen.add(str(r.get("receipt_id", "")))
        save_seen_orders(seen)
        print(f"Marked {len(seen)} existing orders. Watching for new ones.\n")

    while True:
        try:
            now = datetime.now().strftime("%H:%M:%S")
            new = check_for_new_orders(client, seen)
            if new:
                save_seen_orders(seen)
                print(f"[{now}] Processed {new} new order(s)")
            else:
                print(f"[{now}] No new orders", end="\r")
            time.sleep(poll_interval)
        except KeyboardInterrupt:
            print("\n\nMonitor stopped. Break a leg!")
            save_seen_orders(seen)
            break
        except Exception as e:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
            print(f"Retrying in {poll_interval} seconds...")
            time.sleep(poll_interval)


if __name__ == "__main__":
    run_monitor()
