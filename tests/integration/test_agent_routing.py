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

"""Integration tests for ADK agent behavior — smoke tests per routing path.

These tests verify code correctness: imports, agent creation, and tool-calling
behavior. They do NOT assert on LLM response content (non-deterministic).
"""

import asyncio
import os

import nest_asyncio
import pytest

nest_asyncio.apply()

# Routing tests require live API key and produce non-deterministic LLM output —
# these are smoke tests only. They run via `agents-cli run` during development
# and are fully covered by `agents-cli eval run` in CI.
SKIP_ROUTING_TESTS = True  # always skip in pytest; use agents-cli for live testing

from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from customer_support.agent import app


class TestAgentCreation:
    def test_app_has_root_agent(self) -> None:
        assert app.root_agent is not None
        assert app.name == "customer_support"

    def test_root_agent_has_sub_agents(self) -> None:
        root = app.root_agent
        assert hasattr(root, "sub_agents")
        assert len(root.sub_agents) == 3

    def test_root_agent_has_tools(self) -> None:
        root = app.root_agent
        assert hasattr(root, "tools")
        assert len(root.tools) >= 3

    def test_all_specialists_have_tools(self) -> None:
        for agent in app.root_agent.sub_agents:
            assert hasattr(agent, "tools")
            assert len(agent.tools) >= 1


class TestRunnerExecution:
    def _run(self, user_message: str) -> list:
        session_service = InMemorySessionService()
        session = session_service.create_session_sync(
            user_id="test_user", app_name="customer_support"
        )
        runner = Runner(
            app=app,
            session_service=session_service,
            auto_create_session=True,
            app_name="customer_support",
        )
        message = types.Content(
            role="user", parts=[types.Part.from_text(text=user_message)]
        )
        return list(
            runner.run(
                new_message=message,
                user_id="test_user",
                session_id=session.id,
                run_config=RunConfig(streaming_mode=StreamingMode.SSE),
            )
        )

    @pytest.mark.skipif(SKIP_ROUTING_TESTS, reason="Requires GOOGLE_API_KEY for LLM calls")
    def test_concierge_greets(self) -> None:
        events = self._run("Hello!")
        assert len(events) > 0
        # Verify at least one event has content (code correctness)
        has_content = any(e.content and e.content.parts for e in events)
        assert has_content

    @pytest.mark.skipif(SKIP_ROUTING_TESTS, reason="Requires GOOGLE_API_KEY for LLM calls")
    def test_concierge_routes_to_logistician(self) -> None:
        events = self._run(
            "I want to check my order status for order ORD-001"
        )
        assert len(events) > 0
        has_content = any(e.content and e.content.parts for e in events)
        assert has_content
        # Verify tool was called (function_call present in events)
        tool_calls = [
            e
            for e in events
            if hasattr(e, "function_calls") and e.function_calls
        ]
        assert len(tool_calls) >= 1

    @pytest.mark.skipif(SKIP_ROUTING_TESTS, reason="Requires GOOGLE_API_KEY for LLM calls")
    def test_concierge_routes_to_stylist(self) -> None:
        events = self._run("Show me some casual jackets under $200")
        assert len(events) > 0
        has_content = any(e.content and e.content.parts for e in events)
        assert has_content
        tool_calls = [
            e
            for e in events
            if hasattr(e, "function_calls") and e.function_calls
        ]
        assert len(tool_calls) >= 1

    @pytest.mark.skipif(SKIP_ROUTING_TESTS, reason="Requires GOOGLE_API_KEY for LLM calls")
    def test_concierge_routes_to_resolver(self) -> None:
        events = self._run(
            "I want to return order ORD-005 and get a refund"
        )
        assert len(events) > 0
        has_content = any(e.content and e.content.parts for e in events)
        assert has_content
        tool_calls = [
            e
            for e in events
            if hasattr(e, "function_calls") and e.function_calls
        ]
        assert len(tool_calls) >= 1

    @pytest.mark.skipif(SKIP_ROUTING_TESTS, reason="Requires GOOGLE_API_KEY for LLM calls")
    def test_concierge_routes_to_resolver_for_high_value_refund(self) -> None:
        events = self._run(
            "I want a refund for $150 on order ORD-002 — it's damaged"
        )
        assert len(events) > 0
        has_content = any(e.content and e.content.parts for e in events)
        assert has_content