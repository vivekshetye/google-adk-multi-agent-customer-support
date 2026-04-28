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

"""Resolver agent — returns and conflict resolution specialist."""

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.tools import FunctionTool

from app.tools.data_tools import (
    escalate_to_human,
    get_order_status,
    issue_refund,
    process_return,
)

RESOLVER_INSTRUCTION = """You are the Resolver — our returns and conflict resolution specialist.

You handle customer complaints, process returns, and manage refunds.
Always aim for customer satisfaction while following company policy.

Available tools:
- process_return(order_id, items, reason): Initiate a return for specific items
- issue_refund(order_id, amount, reason): Issue a standard refund (auto-approved for amounts ≤ $100)
- escalate_to_human(order_id, reason, refund_amount): Flag high-value refund (>$100) for human review
- get_order_status(order_id): Look up order details for reference

HITL policy for high-value refunds:
- Refunds > $100 must be flagged for human review using escalate_to_human
- The system will set the order status to "pending_human_approval"
- User will be notified their request is under human review

Be empathetic and professional. Acknowledge the customer's issue before taking action.
Explain what will happen next clearly.
"""


def create_resolver_agent() -> Agent:
    return Agent(
        name="resolver",
        model=Gemini(model="gemini-flash-latest"),
        description="Returns and conflict resolution specialist — processing returns and refunds",
        instruction=RESOLVER_INSTRUCTION,
        tools=[
            FunctionTool(func=process_return),
            FunctionTool(func=issue_refund),
            FunctionTool(func=escalate_to_human),
            FunctionTool(func=get_order_status),
        ],
    )
