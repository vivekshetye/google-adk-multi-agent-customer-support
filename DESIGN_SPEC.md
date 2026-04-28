# Customer Support Multi-Agent Team — Design Specification

## Overview

A 4-agent customer support team built on Google ADK (Agent Development Kit) with A2A (Agent-to-Agent) protocol. The Concierge agent acts as the single entry point and orchestrates traffic to specialized agents.

## Architecture

```
User Input
    │
    ▼
┌─────────────────┐
│   Concierge     │ ← Always the entry point (root agent)
│  (Dispatcher &  │
│   Triage)       │
└────────┬────────┘
         │ A2A calls
  ┌──────┴───────────────────────────┐
  │                                  │
  ▼                                  ▼
┌──────────────┐            ┌──────────────┐
│ Logistician  │◄──────────►│   Resolver   │
│ (Orders &    │            │ (Returns &   │
│  Warehouse)  │            │  Conflicts) │
└──────────────┘            └──────────────┘
  │
  ▼
┌──────────────┐
│   Stylist    │
│ (Product     │
│  Discovery)  │
└──────────────┘
```

**Agent Types:**

| Agent | Role | Entry via Concierge | Can delegate to others |
|-------|------|---------------------|------------------------|
| Concierge | Root dispatcher & triage | Yes (root) | All agents |
| Logistician | Order & warehouse specialist | Yes | Stylist |
| Stylist | Product discovery & curation | Yes | None |
| Resolver | Returns & conflict resolution | Yes | None |

## Agents

### 1. Concierge (Root Agent)

**Purpose:** Primary point of entry for all user conversations. Identifies user intent and routes to the correct specialist.

**Instruction:** You are a customer service concierge. Your role is to greet customers, understand their needs, and route them to the appropriate specialist. Always be courteous and professional. Route to: Logistician (shipping/tracking), Stylist (product advice), Resolver (returns/complaints).

**Tools:** Intent classifier (LLM-based routing)

### 2. Logistician

**Purpose:** Handles all factual data regarding shipments, inventory, and order status.

**Instruction:** You are a logistics and warehouse specialist. You handle "Where is my order?" requests, check inventory levels, and provide real-time shipping updates. Be factual and precise. Use data from the orders database.

**Tools:**
- `get_order_status(order_id)` — Returns order details and current status
- `get_shipment_tracking(tracking_number)` — Returns real-time tracking info
- `check_inventory(product_id)` — Returns stock levels
- `list_orders(customer_id)` — Returns all orders for a customer

**Data:** `data/orders.json` — Mock order and shipment data

### 3. Stylist

**Purpose:** Provides personalized product advice by searching through product catalogs.

**Instruction:** You are a fashion and product stylist. Help customers find products that match their preferences, style, and needs. Ask clarifying questions about size, color, occasion, and budget. Use keyword and metadata filters to find the best matches.

**Tools:**
- `search_products(query, filters)` — Search products.json by keyword and metadata
- `get_product_details(product_id)` — Get full product details
- `get_recommendations(preferences)` — Get curated recommendations based on preferences

**Data:** `data/products.json` — Mock product catalog

### 4. Resolver

**Purpose:** Manages returns and conflict resolution with human-in-the-loop for high-value refunds.

**Instruction:** You are a returns and conflict resolution specialist. Handle customer complaints, process returns, and issue refunds. For high-value refunds (>$100), you must flag for human review before finalizing. Always aim for customer satisfaction while following company policy.

**Tools:**
- `process_return(order_id, items, reason)` — Initiate return
- `issue_refund(order_id, amount, reason)` — Issue a refund
- `escalate_to_human(order_id, reason, refund_amount)` — Flag high-value refund for human review (sets status to `pending_human_approval` and notifies the user)

**Data:** `data/orders.json` (for read-only order lookup)

## A2A Communication

- All agents expose an A2A agent card
- Concierge is the root/entry-point agent
- Agents can call each other directly using A2A client calls
- Session state is shared across agents within a conversation (in-memory session)

## Mock Data

### `data/products.json`
- 20+ products across categories: clothing, accessories, footwear
- Metadata: brand, color, size, price, category, tags, rating

### `data/orders.json`
- 15+ orders across multiple customers
- Statuses: processing, shipped, delivered, returned, cancelled
- Tracking numbers and shipping providers

## Session Persistence

- In-memory session storage (prototype mode)
- Each conversation session maintains context across all agents
- Session expires after 30 minutes of inactivity

## Human-in-the-Loop (HITL)

For the Resolver agent only:

**Trigger conditions:**
- Refund amount > $100 → automatically flag for human review
- Flag reason: user disputes charge, suspected fraud

**HITL behavior:**
1. Agent calls `escalate_to_human(order_id, reason, refund_amount)`
2. System sets order status to `pending_human_approval`
3. User receives notification: "Your request has been forwarded to our human team for review. You'll receive an update within 24 hours."

## Success Criteria

1. Concierge correctly routes ≥95% of requests to the right specialist
2. Logistician returns accurate order/shipping info from mock data
3. Stylist returns relevant product results for keyword + filter searches
4. Resolver processes standard returns without escalation
5. High-value refunds are flagged with `pending_human_approval` status
6. All agents can communicate via A2A within a session
