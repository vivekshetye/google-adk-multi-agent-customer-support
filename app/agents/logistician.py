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

"""Logistician agent — order and warehouse specialist."""

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.tools import FunctionTool

from app.tools.data_tools import (
    check_inventory,
    get_order_status,
    get_shipment_tracking,
    list_orders,
)

LOGISTICIAN_INSTRUCTION = """You are the Logistician — our order and warehouse specialist.

You have access to factual data about shipments, order statuses, and inventory.
Use the provided tools to answer customer questions accurately.

Available tools:
- get_order_status(order_id): Look up an order by ID (e.g., ORD-001)
- get_shipment_tracking(tracking_number): Get tracking info (e.g., TRK-001)
- check_inventory(product_id): Check stock for a product (e.g., PROD-001)
- list_orders(customer_id): List all orders for a customer (e.g., CUST-001)

Be factual and precise. Cite specific order IDs, tracking numbers, and dates in your responses.
If you cannot find the requested information, say so clearly rather than guessing.

When providing shipping updates, include the carrier, tracking link format, and estimated delivery date if available.
"""


def create_logistician_agent() -> Agent:
    return Agent(
        name="logistician",
        model=Gemini(model="gemini-flash-latest"),
        description="Order and warehouse specialist — shipments, tracking, and inventory",
        instruction=LOGISTICIAN_INSTRUCTION,
        tools=[
            FunctionTool(func=get_order_status),
            FunctionTool(func=get_shipment_tracking),
            FunctionTool(func=check_inventory),
            FunctionTool(func=list_orders),
        ],
    )
