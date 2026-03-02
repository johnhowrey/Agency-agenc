"""
Etsy API v3 client for Drama Nerd Designs.

Handles OAuth 2.0 authentication, shop management, listing CRUD,
and order retrieval. All other modules use this as their Etsy interface.
"""

import json
import os
import time
import hashlib
import base64
import secrets
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, urlparse, parse_qs

import requests
from dotenv import load_dotenv, set_key

load_dotenv()

ETSY_API_BASE = "https://openapi.etsy.com/v3"
ETSY_AUTH_URL = "https://www.etsy.com/oauth/connect"
ETSY_TOKEN_URL = "https://api.etsy.com/v3/public/oauth/token"
REDIRECT_URI = "http://localhost:3003/callback"
TOKENS_FILE = os.path.join(os.path.dirname(__file__), "tokens.json")


class EtsyClient:
    def __init__(self):
        self.api_key = os.getenv("ETSY_API_KEY")
        self.shared_secret = os.getenv("ETSY_SHARED_SECRET")
        self.shop_id = os.getenv("ETSY_SHOP_ID")
        self.access_token = None
        self.refresh_token = None
        self._load_tokens()

    # --- Authentication ---

    def _load_tokens(self):
        """Load tokens from file, then fall back to .env."""
        if os.path.exists(TOKENS_FILE):
            with open(TOKENS_FILE) as f:
                data = json.load(f)
                self.access_token = data.get("access_token")
                self.refresh_token = data.get("refresh_token")
        if not self.access_token:
            self.access_token = os.getenv("ETSY_ACCESS_TOKEN")
            self.refresh_token = os.getenv("ETSY_REFRESH_TOKEN")

    def _save_tokens(self):
        """Persist tokens to a local file (git-ignored)."""
        with open(TOKENS_FILE, "w") as f:
            json.dump({
                "access_token": self.access_token,
                "refresh_token": self.refresh_token,
            }, f)

    def authorize(self):
        """Run the one-time OAuth 2.0 PKCE flow in the browser."""
        code_verifier = secrets.token_urlsafe(32)
        code_challenge = (
            base64.urlsafe_b64encode(
                hashlib.sha256(code_verifier.encode()).digest()
            )
            .rstrip(b"=")
            .decode()
        )
        state = secrets.token_urlsafe(16)

        scopes = [
            "listings_r", "listings_w", "listings_d",
            "transactions_r", "transactions_w",
            "shops_r", "shops_w",
            "profile_r",
        ]

        params = {
            "response_type": "code",
            "client_id": self.api_key,
            "redirect_uri": REDIRECT_URI,
            "scope": " ".join(scopes),
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }

        auth_url = f"{ETSY_AUTH_URL}?{urlencode(params)}"
        print(f"\nOpening browser for Etsy authorization...")
        print(f"If it doesn't open, go to:\n{auth_url}\n")
        webbrowser.open(auth_url)

        # Tiny local server to catch the callback
        auth_code = None

        class CallbackHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                nonlocal auth_code
                query = parse_qs(urlparse(self.path).query)
                returned_state = query.get("state", [None])[0]
                if returned_state != state:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"State mismatch. Try again.")
                    return
                auth_code = query.get("code", [None])[0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(
                    b"<h1>Drama Nerd Designs connected!</h1>"
                    b"<p>You can close this tab.</p>"
                )

            def log_message(self, format, *args):
                pass  # Suppress server logs

        server = HTTPServer(("localhost", 3003), CallbackHandler)
        print("Waiting for authorization callback...")
        server.handle_request()

        if not auth_code:
            raise RuntimeError("Authorization failed — no code received.")

        # Exchange code for tokens
        resp = requests.post(ETSY_TOKEN_URL, json={
            "grant_type": "authorization_code",
            "client_id": self.api_key,
            "redirect_uri": REDIRECT_URI,
            "code": auth_code,
            "code_verifier": code_verifier,
        })
        resp.raise_for_status()
        data = resp.json()
        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]
        self._save_tokens()
        print("Authorization successful! Tokens saved.")

    def _refresh_access_token(self):
        """Refresh an expired access token."""
        resp = requests.post(ETSY_TOKEN_URL, json={
            "grant_type": "refresh_token",
            "client_id": self.api_key,
            "refresh_token": self.refresh_token,
        })
        resp.raise_for_status()
        data = resp.json()
        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]
        self._save_tokens()

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }

    def _request(self, method, path, **kwargs):
        """Make an authenticated request, refreshing tokens if needed."""
        if not self.access_token:
            raise RuntimeError(
                "Not authenticated. Run: python -m automation.etsy_client"
            )
        url = f"{ETSY_API_BASE}{path}"
        resp = requests.request(method, url, headers=self._headers(), **kwargs)
        if resp.status_code == 401:
            self._refresh_access_token()
            resp = requests.request(
                method, url, headers=self._headers(), **kwargs
            )
        resp.raise_for_status()
        return resp.json() if resp.content else None

    # --- Shop ---

    def get_shop(self):
        """Get shop details."""
        return self._request("GET", f"/application/shops/{self.shop_id}")

    # --- Listings ---

    def get_listings(self, state="active", limit=25):
        """Get shop listings."""
        return self._request(
            "GET",
            f"/application/shops/{self.shop_id}/listings",
            params={"state": state, "limit": limit},
        )

    def create_listing(self, title, description, price_cents, quantity=999,
                       tags=None, taxonomy_id=None, shipping_profile_id=None,
                       who_made="i_did", when_made="2020_2026",
                       is_supply=False):
        """Create a new listing in the shop."""
        payload = {
            "title": title,
            "description": description,
            "price": price_cents / 100,
            "quantity": quantity,
            "tags": tags or [],
            "who_made": who_made,
            "when_made": when_made,
            "is_supply": is_supply,
            "taxonomy_id": taxonomy_id,
            "shipping_profile_id": shipping_profile_id,
        }
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        return self._request(
            "POST",
            f"/application/shops/{self.shop_id}/listings",
            json=payload,
        )

    def update_listing(self, listing_id, **fields):
        """Update an existing listing."""
        return self._request(
            "PATCH",
            f"/application/listings/{listing_id}",
            json=fields,
        )

    # --- Orders / Receipts ---

    def get_receipts(self, min_created=None, limit=25):
        """Get shop receipts (orders). Optionally filter by creation time."""
        params = {"limit": limit}
        if min_created:
            params["min_created"] = int(min_created)
        return self._request(
            "GET",
            f"/application/shops/{self.shop_id}/receipts",
            params=params,
        )

    def get_receipt(self, receipt_id):
        """Get a single receipt by ID."""
        return self._request(
            "GET",
            f"/application/shops/{self.shop_id}/receipts/{receipt_id}",
        )

    def get_receipt_transactions(self, receipt_id):
        """Get the line items (transactions) for an order."""
        return self._request(
            "GET",
            f"/application/shops/{self.shop_id}/transactions",
            params={"receipt_id": receipt_id},
        )

    # --- Shipping ---

    def get_shipping_profiles(self):
        """Get all shipping profiles for the shop."""
        return self._request(
            "GET",
            f"/application/shops/{self.shop_id}/shipping-profiles",
        )


# --- CLI entry point: run authorization ---

if __name__ == "__main__":
    print("=== Drama Nerd Designs — Etsy Authorization ===\n")
    client = EtsyClient()
    if client.access_token:
        print("Already authorized. Testing connection...")
        try:
            shop = client.get_shop()
            print(f"Connected to shop: {shop.get('shop_name', 'unknown')}")
        except Exception as e:
            print(f"Token expired or invalid. Re-authorizing...\n{e}")
            client.authorize()
    else:
        client.authorize()
