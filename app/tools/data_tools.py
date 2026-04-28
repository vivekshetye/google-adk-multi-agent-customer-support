# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Shared data access tools for all specialist agents."""

import json
import os
from pathlib import Path
from typing import Any

# Project root is two levels up from app/tools/data_tools.py
_PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = _PROJECT_ROOT / "data"


def _load_orders() -> list[dict[str, Any]]:
    with open(DATA_DIR / "orders.json") as f:
        return json.load(f)


def _load_products() -> list[dict[str, Any]]:
    with open(DATA_DIR / "products.json") as f:
        return json.load(f)


# ─── Logistician tools ────────────────────────────────────────────────────────


def get_order_status(order_id: str) -> dict[str, Any]:
    """Get the status and details of an order by order ID.

    Args:
        order_id: The order identifier (e.g. ORD-001).

    Returns:
        Order details dict or {"error": "Order not found"}.
    """
    orders = _load_orders()
    for order in orders:
        if order["id"] == order_id:
            return order
    return {"error": f"Order {order_id} not found"}


def get_shipment_tracking(tracking_number: str) -> dict[str, Any]:
    """Get real-time tracking information for a shipment.

    Args:
        tracking_number: The tracking number (e.g. TRK-001).

    Returns:
        Tracking details dict or {"error": "Tracking number not found"}.
    """
    orders = _load_orders()
    for order in orders:
        if order.get("tracking_number") == tracking_number:
            return {
                "tracking_number": tracking_number,
                "order_id": order["id"],
                "status": order["status"],
                "shipping_provider": order.get("shipping_provider"),
                "estimated_delivery": order.get("estimated_delivery"),
                "delivery_date": order.get("delivery_date"),
            }
    return {"error": f"Tracking number {tracking_number} not found"}


def check_inventory(product_id: str) -> dict[str, Any]:
    """Check current inventory level for a product.

    Args:
        product_id: The product identifier (e.g. PROD-001).

    Returns:
        Inventory info dict or {"error": "Product not found"}.
    """
    products = _load_products()
    for product in products:
        if product["id"] == product_id:
            return {
                "product_id": product_id,
                "name": product["name"],
                "stock": product["stock"],
                "in_stock": product["stock"] > 0,
            }
    return {"error": f"Product {product_id} not found"}


def list_orders(customer_id: str) -> dict[str, Any]:
    """List all orders for a customer.

    Args:
        customer_id: The customer identifier (e.g. CUST-001).

    Returns:
        Dict with customer info and list of orders.
    """
    orders = _load_orders()
    customer_orders = [o for o in orders if o["customer_id"] == customer_id]
    if not customer_orders:
        return {"error": f"No orders found for customer {customer_id}"}
    return {
        "customer_id": customer_id,
        "customer_name": customer_orders[0]["customer_name"],
        "order_count": len(customer_orders),
        "orders": customer_orders,
    }


# ─── Stylist tools ────────────────────────────────────────────────────────────


def search_products(
    query: str,
    category: str | None = None,
    brand: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    color: str | None = None,
    size: str | None = None,
    tags: list[str] | None = None,
    limit: int = 10,
) -> dict[str, Any]:
    """Search products by keyword and metadata filters.

    Args:
        query: Free-text keyword search across name, brand, tags.
        category: Filter by category (e.g. clothing, footwear, accessories).
        brand: Filter by brand name (exact or partial match).
        min_price: Minimum price filter.
        max_price: Maximum price filter.
        color: Filter by color.
        size: Filter by available size.
        tags: List of tags to match (all must be present).
        limit: Maximum number of results to return.

    Returns:
        Dict with search results and total count.
    """
    products = _load_products()
    results = []

    query_lower = query.lower()
    for product in products:
        # Keyword match on name, brand, tags
        if query_lower:
            name_match = query_lower in product["name"].lower()
            brand_match = query_lower in product["brand"].lower()
            tag_match = any(query_lower in tag.lower() for tag in product.get("tags", []))
            keyword_ok = name_match or brand_match or tag_match
        else:
            keyword_ok = True

        if not keyword_ok:
            continue

        # Category filter
        if category and product["category"] != category:
            continue

        # Brand filter
        if brand and brand.lower() not in product["brand"].lower():
            continue

        # Price filters
        if min_price is not None and product["price"] < min_price:
            continue
        if max_price is not None and product["price"] > max_price:
            continue

        # Color filter
        if color and color.lower() not in " ".join(product.get("colors", [])).lower():
            continue

        # Size filter
        if size and size not in product.get("sizes", []) and size.lower() not in " ".join(product.get("sizes", [])).lower():
            continue

        # Tags filter (all requested tags must be present)
        if tags:
            product_tags_lower = [t.lower() for t in product.get("tags", [])]
            if not all(t.lower() in product_tags_lower for t in tags):
                continue

        results.append(product)

    return {
        "query": query,
        "filters": {
            "category": category,
            "brand": brand,
            "min_price": min_price,
            "max_price": max_price,
            "color": color,
            "size": size,
            "tags": tags,
        },
        "total_results": len(results),
        "results": results[:limit],
    }


def get_product_details(product_id: str) -> dict[str, Any]:
    """Get full product details by product ID.

    Args:
        product_id: The product identifier (e.g. PROD-001).

    Returns:
        Full product details dict or {"error": "Product not found"}.
    """
    products = _load_products()
    for product in products:
        if product["id"] == product_id:
            return product
    return {"error": f"Product {product_id} not found"}


def get_recommendations(
    occasion: str | None = None,
    style: str | None = None,
    budget: float | None = None,
    category: str | None = None,
) -> dict[str, Any]:
    """Get curated product recommendations based on preferences.

    Args:
        occasion: e.g. casual, office, vacation, sport
        style: e.g. vintage, modern, minimalist, streetwear
        budget: Maximum price the customer wants to spend
        category: Preferred product category

    Returns:
        Dict with recommendation list.
    """
    products = _load_products()
    scores: dict[int, int] = {}

    for i, product in enumerate(products):
        score = 0
        product_tags_lower = [t.lower() for t in product.get("tags", [])]
        product_category_lower = product.get("category", "").lower()

        if occasion:
            if occasion.lower() in product_tags_lower:
                score += 3
            elif occasion.lower() in product.get("name", "").lower():
                score += 1

        if style:
            if style.lower() in product_tags_lower:
                score += 3
            elif style.lower() in product.get("name", "").lower():
                score += 1

        if category and product_category_lower == category.lower():
            score += 2

        if budget is not None:
            if product["price"] <= budget:
                score += 1

        # Prefer higher-rated products slightly
        if product.get("rating", 0) >= 4.5:
            score += 1

        scores[i] = score

    sorted_indices = sorted(scores, key=scores.get, reverse=True)
    recommendations = [products[i] for i in sorted_indices[:5] if scores[i] > 0]

    return {
        "preferences": {
            "occasion": occasion,
            "style": style,
            "budget": budget,
            "category": category,
        },
        "recommendations": recommendations,
    }


# ─── Resolver tools ────────────────────────────────────────────────────────────


def process_return(order_id: str, items: list[str], reason: str) -> dict[str, Any]:
    """Initiate a return for an order.

    Args:
        order_id: The order identifier.
        items: List of product IDs to return.
        reason: Reason for the return.

    Returns:
        Return confirmation dict.
    """
    orders = _load_orders()
    for order in orders:
        if order["id"] == order_id:
            return {
                "status": "return_initiated",
                "order_id": order_id,
                "items": items,
                "reason": reason,
                "message": f"Return initiated for order {order_id}. You will receive a return shipping label via email within 24 hours.",
            }
    return {"error": f"Order {order_id} not found"}


def issue_refund(order_id: str, amount: float, reason: str) -> dict[str, Any]:
    """Issue a refund for an order (standard, low-value).

    Args:
        order_id: The order identifier.
        amount: Refund amount in dollars.
        reason: Reason for the refund.

    Returns:
        Refund confirmation dict.
    """
    orders = _load_orders()
    for order in orders:
        if order["id"] == order_id:
            # High-value threshold: $100
            if amount > 100:
                return {
                    "status": "requires_human_review",
                    "order_id": order_id,
                    "message": f"Refund amount ${amount:.2f} exceeds the automatic approval threshold. Your request has been forwarded to our human team for review.",
                }
            return {
                "status": "refund_approved",
                "order_id": order_id,
                "amount": amount,
                "reason": reason,
                "message": f"Refund of ${amount:.2f} has been approved and will be processed within 5-7 business days.",
            }
    return {"error": f"Order {order_id} not found"}


def escalate_to_human(order_id: str, reason: str, refund_amount: float) -> dict[str, Any]:
    """Flag a high-value refund for human review (HITL).

    Args:
        order_id: The order identifier.
        reason: Reason escalation is needed.
        refund_amount: The refund amount being requested.

    Returns:
        Escalation confirmation dict.
    """
    # In production this would update a database/CRM ticket.
    # Here we just return a confirmation.
    return {
        "status": "pending_human_approval",
        "order_id": order_id,
        "reason": reason,
        "refund_amount": refund_amount,
        "message": "Your request has been forwarded to our human team for review. You'll receive an update within 24 hours.",
    }
