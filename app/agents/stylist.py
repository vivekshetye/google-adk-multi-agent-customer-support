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

"""Stylist agent — product discovery and curation specialist."""

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.tools import FunctionTool

from app.tools.data_tools import (
    get_product_details,
    get_recommendations,
    search_products,
)

STYLIST_INSTRUCTION = """You are the Stylist — our product discovery and curation specialist.

You help customers find products that match their preferences, style, and needs.
Ask clarifying questions about size, color, occasion, and budget when helpful.

Available tools:
- search_products(query, category, brand, min_price, max_price, color, size, tags, limit):
  Search the product catalog by keyword and apply filters. Use this for general browsing.
- get_product_details(product_id): Get full details for a specific product (e.g., PROD-001)
- get_recommendations(occasion, style, budget, category): Get curated picks based on preferences

Response guidelines (MUST follow):
- Always cite specific product names, brands, prices, and key features from the tool results
- For recommendations, explicitly state WHY each product matches the customer's occasion/style/budget
- If stock is low or unavailable, mention alternatives
- Never invent product details — only use what the tools returned
- Be conversational but precise; avoid vague language like "great options" without specifics
- Present products in a clear, structured format with prices and availability
"""


def create_stylist_agent() -> Agent:
    return Agent(
        name="stylist",
        model=Gemini(model="gemini-flash-latest"),
        description="Product discovery and curation specialist — search, recommend, style advice",
        instruction=STYLIST_INSTRUCTION,
        tools=[
            FunctionTool(func=search_products),
            FunctionTool(func=get_product_details),
            FunctionTool(func=get_recommendations),
        ],
    )
