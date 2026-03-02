"""
Email notification sender for Drama Nerd Designs.

Sends order notifications to john@musicaltheatrehistory.com via Gmail SMTP.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

load_dotenv()


def send_order_notification(order):
    """Send an email notification for a new Etsy order."""
    gmail_address = os.getenv("GMAIL_ADDRESS")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    to_email = os.getenv("NOTIFICATION_EMAIL", "john@musicaltheatrehistory.com")

    buyer_name = order.get("name", "A customer")
    receipt_id = order.get("receipt_id", "unknown")
    items = order.get("items", [])
    total = order.get("grandtotal", {})
    total_str = f"${total.get('amount', 0) / 100:.2f}" if total else "unknown"

    # Build the item list
    item_lines = []
    for item in items:
        title = item.get("title", "Unknown item")
        qty = item.get("quantity", 1)
        item_lines.append(f"  - {title} (x{qty})")
    item_text = "\n".join(item_lines) if item_lines else "  (see Etsy for details)"

    # Shipping address
    addr = order.get("shipping_address", {})
    ship_to = "\n".join(filter(None, [
        addr.get("name", ""),
        addr.get("first_line", ""),
        addr.get("second_line", ""),
        f"{addr.get('city', '')}, {addr.get('state', '')} {addr.get('zip', '')}",
        addr.get("country_iso", ""),
    ]))

    gift_message = order.get("message_from_buyer", "")
    is_gift = order.get("is_gift", False)

    subject = f"New Order #{receipt_id} from {buyer_name}"

    body = f"""New order from {buyer_name}!

Order #{receipt_id}
Total: {total_str}

ITEMS:
{item_text}

SHIP TO:
{ship_to}
"""

    if is_gift and gift_message:
        body += f"\nGIFT MESSAGE:\n{gift_message}\n"
    elif gift_message:
        body += f"\nBUYER MESSAGE:\n{gift_message}\n"

    body += f"""
NEXT STEPS:
1. Print the packing slip:  python -m automation.packing_slip {receipt_id}
2. Pack the order
3. Buy shipping label on Etsy
4. Ship it!

---
View on Etsy: https://www.etsy.com/your/orders/sold?order_id={receipt_id}
"""

    msg = MIMEMultipart()
    msg["From"] = gmail_address
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_address, gmail_password)
        server.send_message(msg)

    print(f"Notification sent for order #{receipt_id}")


def send_test_email():
    """Send a test email to verify the configuration works."""
    gmail_address = os.getenv("GMAIL_ADDRESS")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    to_email = os.getenv("NOTIFICATION_EMAIL", "john@musicaltheatrehistory.com")

    msg = MIMEMultipart()
    msg["From"] = gmail_address
    msg["To"] = to_email
    msg["Subject"] = "Drama Nerd Designs Automation — Test"
    msg.attach(MIMEText(
        "This is a test email from your Drama Nerd Designs automation.\n\n"
        "If you're reading this, notifications are working!\n\n"
        "Break a leg,\nYour automation system",
        "plain",
    ))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_address, gmail_password)
        server.send_message(msg)

    print(f"Test email sent to {to_email}")


if __name__ == "__main__":
    send_test_email()
