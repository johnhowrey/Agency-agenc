"""
Packing slip generator for Drama Nerd Designs.

Generates a printable HTML packing slip for each order.
Includes order details, shipping address, and gift message if applicable.
"""

import os
import sys
from datetime import datetime

from jinja2 import Template
from dotenv import load_dotenv

from automation.etsy_client import EtsyClient

load_dotenv()

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

PACKING_SLIP_TEMPLATE = Template("""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Packing Slip — Order #{{ receipt_id }}</title>
<style>
  @page { size: letter; margin: 0.75in; }
  body {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    color: #222;
    line-height: 1.5;
    max-width: 7in;
    margin: 0 auto;
    padding: 20px;
  }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 3px solid #222;
    padding-bottom: 12px;
    margin-bottom: 24px;
  }
  .brand-name {
    font-size: 24px;
    font-weight: bold;
    letter-spacing: 0.5px;
  }
  .brand-tagline {
    font-size: 11px;
    color: #666;
    margin-top: 4px;
  }
  .order-info {
    text-align: right;
    font-size: 13px;
    color: #555;
  }
  .order-number {
    font-size: 16px;
    font-weight: bold;
    color: #222;
  }
  .addresses {
    display: flex;
    gap: 40px;
    margin-bottom: 24px;
  }
  .address-block { flex: 1; }
  .address-label {
    font-size: 11px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #888;
    margin-bottom: 6px;
  }
  .address-text { font-size: 14px; }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 24px;
  }
  th {
    text-align: left;
    font-size: 11px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #888;
    border-bottom: 1px solid #ddd;
    padding: 8px 0;
  }
  th:last-child { text-align: right; }
  td {
    padding: 10px 0;
    font-size: 14px;
    border-bottom: 1px solid #eee;
  }
  td:last-child { text-align: right; }
  .gift-message {
    background: #f9f6f1;
    border-left: 4px solid #c9a96e;
    padding: 16px 20px;
    margin-bottom: 24px;
    font-style: italic;
  }
  .gift-label {
    font-size: 11px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #c9a96e;
    margin-bottom: 6px;
    font-style: normal;
  }
  .footer {
    text-align: center;
    font-size: 12px;
    color: #888;
    border-top: 1px solid #ddd;
    padding-top: 16px;
    margin-top: 32px;
  }
  .thank-you {
    font-size: 16px;
    text-align: center;
    margin: 24px 0;
    color: #444;
  }
</style>
</head>
<body>
  <div class="header">
    <div>
      <div class="brand-name">Drama Nerd Designs</div>
      <div class="brand-tagline">dramanerddesigns.com</div>
    </div>
    <div class="order-info">
      <div class="order-number">Order #{{ receipt_id }}</div>
      <div>{{ order_date }}</div>
    </div>
  </div>

  <div class="addresses">
    <div class="address-block">
      <div class="address-label">Ship From</div>
      <div class="address-text">
        {{ ship_from_name }}<br>
        {{ ship_from_city }}, {{ ship_from_state }} {{ ship_from_zip }}
      </div>
    </div>
    <div class="address-block">
      <div class="address-label">Ship To</div>
      <div class="address-text">
        {{ ship_to_name }}<br>
        {{ ship_to_line1 }}<br>
        {% if ship_to_line2 %}{{ ship_to_line2 }}<br>{% endif %}
        {{ ship_to_city }}, {{ ship_to_state }} {{ ship_to_zip }}<br>
        {{ ship_to_country }}
      </div>
    </div>
  </div>

  <table>
    <thead>
      <tr>
        <th>Item</th>
        <th>Qty</th>
      </tr>
    </thead>
    <tbody>
      {% for item in items %}
      <tr>
        <td>{{ item.title }}{% if item.variation %} — {{ item.variation }}{% endif %}</td>
        <td>{{ item.quantity }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>

  {% if gift_message %}
  <div class="gift-message">
    <div class="gift-label">Gift Message</div>
    {{ gift_message }}
  </div>
  {% endif %}

  <div class="thank-you">
    Thank you for supporting Drama Nerd Designs!<br>
    <small>We hope this brings a little Broadway magic to your day.</small>
  </div>

  <div class="footer">
    Drama Nerd Designs &middot; Palm Springs, CA &middot; dramanerddesigns.com
  </div>
</body>
</html>
""")


def generate_packing_slip(receipt_id):
    """Fetch order from Etsy and generate a packing slip HTML file."""
    client = EtsyClient()
    receipt = client.get_receipt(receipt_id)
    transactions = client.get_receipt_transactions(receipt_id)

    addr = receipt.get("shipping_address", {}) if receipt else {}
    items_data = transactions.get("results", []) if transactions else []

    items = []
    for txn in items_data:
        variations = txn.get("variations", [])
        variation_str = ", ".join(
            f"{v.get('formatted_name', '')}: {v.get('formatted_value', '')}"
            for v in variations
        ) if variations else ""
        items.append({
            "title": txn.get("title", "Unknown item"),
            "quantity": txn.get("quantity", 1),
            "variation": variation_str,
        })

    created_ts = receipt.get("create_timestamp", 0) if receipt else 0
    order_date = datetime.fromtimestamp(created_ts).strftime("%B %d, %Y") if created_ts else "Unknown"

    buyer_message = ""
    if receipt:
        buyer_message = receipt.get("message_from_buyer", "") or ""

    html = PACKING_SLIP_TEMPLATE.render(
        receipt_id=receipt_id,
        order_date=order_date,
        ship_from_name=os.getenv("SHIP_FROM_NAME", "John Howrey"),
        ship_from_city=os.getenv("SHIP_FROM_CITY", "Palm Springs"),
        ship_from_state=os.getenv("SHIP_FROM_STATE", "CA"),
        ship_from_zip=os.getenv("SHIP_FROM_ZIP", ""),
        ship_to_name=addr.get("name", ""),
        ship_to_line1=addr.get("first_line", ""),
        ship_to_line2=addr.get("second_line", ""),
        ship_to_city=addr.get("city", ""),
        ship_to_state=addr.get("state", ""),
        ship_to_zip=addr.get("zip", ""),
        ship_to_country=addr.get("country_iso", ""),
        items=items,
        gift_message=buyer_message if buyer_message else None,
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"packing-slip-{receipt_id}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w") as f:
        f.write(html)

    print(f"Packing slip saved: {filepath}")
    print(f"Open in your browser and print (Cmd+P / Ctrl+P)")
    return filepath


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m automation.packing_slip <receipt_id>")
        sys.exit(1)
    generate_packing_slip(sys.argv[1])
