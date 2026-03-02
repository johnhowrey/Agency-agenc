"""
Listing manager for Drama Nerd Designs.

Creates and updates Etsy listings using the product copy from the agents.
Provides ready-to-use listing data for the three focus products.
"""

import sys

from automation.etsy_client import EtsyClient


# --- Focus Product Listing Data ---
# These match the copy from agents/product-copywriter.md

LISTINGS = {
    "tote-regular": {
        "title": (
            "Broadway Tote Bag - Musical Theatre Map Design"
            " - Gift for Theatre Nerd - Reusable Grocery Bag"
        ),
        "description": (
            "The same choreographer did both Hamilton and 9 to 5. (Yes, really.)\n\n"
            "That's the kind of connection you'll find on our Broadway Musical "
            "History tote bags. Each \"subway line\" is a different creative — "
            "directors, choreographers, composers, lyricists — and they meet at "
            "the shows they worked on together.\n\n"
            "WHAT YOU GET:\n"
            "- Sturdy canvas tote bag\n"
            "- Full Broadway Musical History Subway Map design\n"
            "- Regular size — perfect for groceries, books, and sheet music\n\n"
            "It's been stumping theatre nerds since 2008. Now you can carry it "
            "everywhere.\n\n"
            "Also available in Tiny and XL (with a crossbody strap).\n\n"
            "PERFECT FOR:\n"
            "- Theatre lovers and Broadway fans\n"
            "- Drama teachers\n"
            "- Cast and crew gifts\n"
            "- Yourself (you deserve it)\n\n"
            "SHIPPING:\n"
            "Ships free from Palm Springs, CA within 1-2 weeks."
        ),
        "price_cents": 3600,
        "tags": [
            "broadway tote bag",
            "musical theatre gift",
            "theatre map bag",
            "broadway gift",
            "theatre nerd tote",
            "reusable grocery bag",
            "drama teacher gift",
            "broadway fan gift",
            "theatre lover bag",
            "musical theatre tote",
            "cast gift idea",
            "broadway map bag",
            "theatre tote bag",
        ],
    },
    "tote-xl": {
        "title": (
            "XL Broadway Crossbody Tote Bag - Musical Theatre Map"
            " - Extra Large Theatre Gift - Broadway Lover Bag"
        ),
        "description": (
            "The same choreographer did both Hamilton and 9 to 5. (Yes, really.)\n\n"
            "That's the kind of connection you'll find on our XL Broadway Musical "
            "History tote. Each \"subway line\" is a different creative — "
            "directors, choreographers, composers, lyricists — and they meet at "
            "the shows they worked on together.\n\n"
            "WHAT YOU GET:\n"
            "- Extra-large canvas tote bag\n"
            "- Full Broadway Musical History Subway Map design\n"
            "- Extra-long handle for crossbody use\n"
            "- Room for everything — groceries, books, rehearsal gear\n\n"
            "Also available in Regular and Tiny sizes.\n\n"
            "SHIPPING:\n"
            "Ships free from Palm Springs, CA within 1-2 weeks."
        ),
        "price_cents": 3600,
        "tags": [
            "xl tote bag",
            "crossbody tote bag",
            "broadway tote bag",
            "musical theatre gift",
            "large tote bag",
            "broadway gift",
            "theatre nerd bag",
            "drama teacher gift",
            "broadway fan tote",
            "theatre map bag",
            "cast crew gift",
            "extra large tote",
            "musical theatre bag",
        ],
    },
    "tote-tiny": {
        "title": (
            "Tiny Broadway Tote Bag - Mini Musical Theatre Map Bag"
            " - Small Theatre Gift - Broadway Lunch Bag"
        ),
        "description": (
            "All the Broadway history, in a perfectly tiny package.\n\n"
            "Our Tiny tote features the full Broadway Musical History Subway "
            "Map — the same design that's been delighting theatre nerds since "
            "2008 — in a compact size perfect for lunch, toiletries, or a "
            "quick errand.\n\n"
            "WHAT YOU GET:\n"
            "- Tiny canvas tote bag\n"
            "- Full Broadway Musical History Subway Map design\n"
            "- Perfect for lunch, small items, toiletries\n\n"
            "Also available in Regular and XL (with crossbody strap).\n\n"
            "SHIPPING:\n"
            "Ships free from Palm Springs, CA within 1-2 weeks."
        ),
        "price_cents": 3600,
        "tags": [
            "tiny tote bag",
            "mini tote bag",
            "broadway tote bag",
            "musical theatre gift",
            "small tote bag",
            "broadway gift",
            "theatre lunch bag",
            "drama teacher gift",
            "broadway fan gift",
            "theatre nerd bag",
            "mini broadway bag",
            "theatre map bag",
            "small theatre gift",
        ],
    },
    "oracle": {
        "title": (
            "Broadway Lyric Oracle Cards - 100 Card Musical Theatre Deck"
            " - Broadway Gift - Theatre Lover Gift Idea"
        ),
        "description": (
            "Stuck on a tough decision? Let Broadway decide.\n\n"
            "The Broadway Oracle is a deck of 100 lyric cards drawn from the "
            "greatest musicals ever written. Pull a card, read the lyric, and "
            "let the wisdom of the stage guide your way.\n\n"
            "WHAT YOU GET:\n"
            "- 100 unique oracle cards\n"
            "- Card size: 2.75 x 4.75 inches (standard tarot card size)\n"
            "- Lyrics from Hamilton, Rent, Phantom, Wicked, Les Mis, Dear Evan "
            "Hansen, West Side Story, A Chorus Line, and many more\n"
            "- Beautifully designed by a professional graphic designer\n\n"
            "HOW TO USE:\n"
            "There's no wrong way to use The Oracle. Shuffle the deck, pull a "
            "card, and see what Broadway has to say. Use it for:\n"
            "- Daily inspiration\n"
            "- Making tough decisions\n"
            "- Pre-show rituals\n"
            "- Party games with theatre friends\n"
            "- A little dramatic flair in your morning routine\n\n"
            "\"Keep a song in your heart and the meaning will come to you.\"\n\n"
            "PERFECT FOR:\n"
            "- Theatre lovers and Broadway fans\n"
            "- Birthday and holiday gifts\n"
            "- Opening night gifts for cast and crew\n"
            "- Drama club and theatre class activities\n"
            "- Anyone who could use a little theatrical wisdom\n\n"
            "SHIPPING:\n"
            "Ships from Palm Springs, CA within 1-2 weeks."
        ),
        "price_cents": 2500,
        "tags": [
            "broadway oracle cards",
            "musical theatre gift",
            "broadway card deck",
            "theatre lover gift",
            "oracle cards",
            "broadway fan gift",
            "theatre nerd",
            "musical theatre cards",
            "cast gift idea",
            "drama teacher gift",
            "broadway game",
            "theatre party",
            "opening night gift",
        ],
    },
    "mug": {
        "title": (
            "Broadway Musical History Mug - 15oz Theatre Coffee Mug"
            " - Musical Theatre Gift - Broadway Lover Mug"
        ),
        "description": (
            "Start your morning with the entire history of Broadway in your "
            "hands.\n\n"
            "This 15oz mug features the Broadway Musical History Subway Map — "
            "the same beloved design that's been delighting theatre nerds since "
            "2008. Each \"subway line\" is a different director, choreographer, "
            "composer, or lyricist, and they meet at the shows they worked on "
            "together.\n\n"
            "WHAT YOU GET:\n"
            "- 15oz ceramic mug (slightly bigger than standard — you'll love it)\n"
            "- Full Broadway Musical History Subway Map design\n"
            "- Vibrant, dishwasher-safe print\n"
            "- Packaged securely for safe shipping\n\n"
            "WHY YOU NEED IT:\n"
            "Your morning coffee just got a lot more interesting. Trace Bob "
            "Fosse's career while you sip. Find the surprising connections "
            "between Golden Age classics and modern hits. Every morning is "
            "a new discovery.\n\n"
            "Pairs perfectly with a tote bag for the complete Broadway nerd kit.\n\n"
            "PERFECT FOR:\n"
            "- The theatre lover who starts every day with a cast recording\n"
            "- Birthday and holiday gifts\n"
            "- Drama teacher appreciation gifts\n"
            "- Treating yourself (you deserve it)\n\n"
            "SHIPPING:\n"
            "Ships from Palm Springs, CA within 1-2 weeks. Packaged securely."
        ),
        "price_cents": 2000,
        "tags": [
            "broadway mug",
            "musical theatre gift",
            "theatre coffee mug",
            "broadway gift",
            "theatre lover mug",
            "musical theatre mug",
            "drama teacher gift",
            "broadway coffee cup",
            "theatre nerd gift",
            "broadway lover gift",
            "cast gift idea",
            "theatre mug",
            "broadway fan mug",
        ],
    },
}


def list_available():
    """Show available listing templates."""
    print("Available listing templates:\n")
    for key, data in LISTINGS.items():
        title = data["title"][:60]
        price = f"${data['price_cents'] / 100:.2f}"
        print(f"  {key:15s}  {price:>8s}  {title}...")
    print(f"\nUsage: python -m automation.listing_manager create <key>")
    print(f"       python -m automation.listing_manager list")


def show_listings():
    """Show current active listings from Etsy."""
    client = EtsyClient()
    result = client.get_listings(state="active")
    listings = result.get("results", []) if result else []
    if not listings:
        print("No active listings found.")
        return
    print(f"Active listings ({len(listings)}):\n")
    for listing in listings:
        lid = listing.get("listing_id", "?")
        title = listing.get("title", "?")[:60]
        price = listing.get("price", {})
        price_str = f"${price.get('amount', 0) / price.get('divisor', 100):.2f}" if price else "?"
        print(f"  [{lid}] {price_str:>8s}  {title}")


def create_listing(key):
    """Create a listing on Etsy from a template."""
    if key not in LISTINGS:
        print(f"Unknown listing key: {key}")
        print(f"Available: {', '.join(LISTINGS.keys())}")
        return

    data = LISTINGS[key]
    client = EtsyClient()

    print(f"Creating listing: {key}")
    print(f"  Title: {data['title'][:70]}...")
    print(f"  Price: ${data['price_cents'] / 100:.2f}")
    print(f"  Tags: {len(data['tags'])}")

    # Note: taxonomy_id and shipping_profile_id need to be set
    # based on your shop's configuration. Run 'list' first to see
    # existing listings and their IDs, or check Etsy's taxonomy API.
    result = client.create_listing(
        title=data["title"],
        description=data["description"],
        price_cents=data["price_cents"],
        tags=data["tags"],
    )

    if result:
        listing_id = result.get("listing_id", "unknown")
        print(f"\n  Created! Listing ID: {listing_id}")
        print(f"  Status: {result.get('state', 'unknown')}")
        print(f"\n  IMPORTANT: Add photos and set shipping profile on Etsy.")
        print(f"  Edit at: https://www.etsy.com/your/shops/DramaNerdDesigns/"
              f"tools/listings/{listing_id}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        list_available()
        sys.exit(0)

    command = sys.argv[1]
    if command == "list":
        show_listings()
    elif command == "create" and len(sys.argv) >= 3:
        create_listing(sys.argv[2])
    elif command == "templates":
        list_available()
    else:
        list_available()
