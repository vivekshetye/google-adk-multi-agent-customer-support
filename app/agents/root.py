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

"""Root Concierge agent — wired with specialist sub-agents via sub_agents."""

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.tools import agent_tool

from app.agents.logistician import create_logistician_agent
from app.agents.resolver import create_resolver_agent
from app.agents.stylist import create_stylist_agent


def create_root_agent() -> Agent:
    logistician = create_logistician_agent()
    stylist = create_stylist_agent()
    resolver = create_resolver_agent()

    return Agent(
        name="concierge",
        model=Gemini(model="gemini-flash-latest"),
        description="Customer support dispatcher and triage specialist — routes to the right specialist.",
        instruction=(
            "You are the Concierge for our customer support team — the single point of entry for all customer conversations.\n\n"
            "Your role is to:\n"
            "1. Greet the customer warmly and identify their intent\n"
            "2. Route them to the correct specialist using the transfer_to_agent tool\n\n"
            "Route to:\n"
            "- logistician: For shipping, tracking, delivery, or order status questions\n"
            "- stylist: For product advice, recommendations, styling, or catalog search\n"
            "- resolver: For returns, refunds, complaints, or disputes\n\n"
            "Be courteous and professional. Use transfer_to_agent to delegate to the appropriate specialist.\n"
        ),
        sub_agents=[logistician, stylist, resolver],
        tools=[
            agent_tool.AgentTool(agent=logistician),
            agent_tool.AgentTool(agent=stylist),
            agent_tool.AgentTool(agent=resolver),
        ],
    )
