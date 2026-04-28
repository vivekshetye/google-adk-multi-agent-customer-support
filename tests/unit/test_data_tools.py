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

"""Unit tests for data_tools.py — all specialist tool functions."""

import pytest
from customer_support.tools import data_tools


class TestLogisticianTools:
    def test_get_order_status_found(self) -> None:
        result = data_tools.get_order_status("ORD-001")
        assert "error" not in result
        assert result["id"] == "ORD-001"
        assert result["customer_id"] == "CUST-001"

    def test_get_order_status_not_found(self) -> None:
        result = data_tools.get_order_status("ORD-999")
        assert "error" in result

    def test_get_shipment_tracking_found(self) -> None:
        result = data_tools.get_shipment_tracking("TRK-001")
        assert "error" not in result
        assert result["tracking_number"] == "TRK-001"
        assert result["order_id"] == "ORD-001"

    def test_get_shipment_tracking_not_found(self) -> None:
        result = data_tools.get_shipment_tracking("TRK-999")
        assert "error" in result

    def test_check_inventory_in_stock(self) -> None:
        result = data_tools.check_inventory("PROD-001")
        assert "error" not in result
        assert result["product_id"] == "PROD-001"
        assert result["in_stock"] is True
        assert result["stock"] == 45

    def test_check_inventory_not_found(self) -> None:
        result = data_tools.check_inventory("PROD-999")
        assert "error" in result

    def test_list_orders_found(self) -> None:
        result = data_tools.list_orders("CUST-001")
        assert "error" not in result
        assert result["customer_id"] == "CUST-001"
        assert result["order_count"] >= 1

    def test_list_orders_not_found(self) -> None:
        result = data_tools.list_orders("CUST-999")
        assert "error" in result


class TestStylistTools:
    def test_search_products_by_keyword(self) -> None:
        result = data_tools.search_products("jacket")
        assert result["total_results"] >= 1
        assert any("jacket" in p["name"].lower() for p in result["results"])

    def test_search_products_empty_query(self) -> None:
        result = data_tools.search_products("")
        assert result["total_results"] >= 1

    def test_search_products_category_filter(self) -> None:
        result = data_tools.search_products("shirt", category="clothing")
        for p in result["results"]:
            assert p["category"] == "clothing"

    def test_search_products_brand_filter(self) -> None:
        result = data_tools.search_products("", brand="nike")
        for p in result["results"]:
            assert "nike" in p["brand"].lower()

    def test_search_products_price_filters(self) -> None:
        result = data_tools.search_products("", min_price=50, max_price=150)
        for p in result["results"]:
            assert 50 <= p["price"] <= 150

    def test_search_products_color_filter(self) -> None:
        result = data_tools.search_products("", color="black")
        assert result["total_results"] >= 1

    def test_search_products_size_filter(self) -> None:
        result = data_tools.search_products("", size="M")
        assert result["total_results"] >= 1

    def test_search_products_tags_filter(self) -> None:
        result = data_tools.search_products("", tags=["waterproof"])
        for p in result["results"]:
            assert any("waterproof" in t.lower() for t in p.get("tags", []))

    def test_search_products_limit(self) -> None:
        result = data_tools.search_products("", limit=3)
        assert len(result["results"]) <= 3

    def test_get_product_details_found(self) -> None:
        result = data_tools.get_product_details("PROD-001")
        assert "error" not in result
        assert result["id"] == "PROD-001"

    def test_get_product_details_not_found(self) -> None:
        result = data_tools.get_product_details("PROD-999")
        assert "error" in result

    def test_get_recommendations_by_occasion(self) -> None:
        result = data_tools.get_recommendations(occasion="casual")
        assert len(result["recommendations"]) >= 1

    def test_get_recommendations_by_style(self) -> None:
        result = data_tools.get_recommendations(style="sport")
        assert len(result["recommendations"]) >= 1

    def test_get_recommendations_by_budget(self) -> None:
        result = data_tools.get_recommendations(budget=100)
        for p in result["recommendations"]:
            assert p["price"] <= 100

    def test_get_recommendations_by_category(self) -> None:
        result = data_tools.get_recommendations(category="clothing")
        assert len(result["recommendations"]) >= 1

    def test_get_recommendations_combined(self) -> None:
        result = data_tools.get_recommendations(
            occasion="vacation", style="modern", budget=200, category="clothing"
        )
        assert len(result["recommendations"]) >= 1


class TestResolverTools:
    def test_process_return_found(self) -> None:
        result = data_tools.process_return("ORD-001", ["PROD-001"], "Wrong size")
        assert result["status"] == "return_initiated"
        assert result["order_id"] == "ORD-001"

    def test_process_return_not_found(self) -> None:
        result = data_tools.process_return("ORD-999", ["PROD-001"], "Defective")
        assert "error" in result

    def test_issue_refund_low_value_auto_approved(self) -> None:
        result = data_tools.issue_refund("ORD-001", 50.0, "Partial defective")
        assert result["status"] == "refund_approved"

    def test_issue_refund_high_value_requires_human(self) -> None:
        result = data_tools.issue_refund("ORD-001", 150.0, "Fully defective")
        assert result["status"] == "requires_human_review"

    def test_issue_refund_exactly_threshold_approved(self) -> None:
        result = data_tools.issue_refund("ORD-001", 100.0, "Damaged")
        assert result["status"] == "refund_approved"

    def test_issue_refund_not_found(self) -> None:
        result = data_tools.issue_refund("ORD-999", 50.0, "Late delivery")
        assert "error" in result

    def test_escalate_to_human(self) -> None:
        result = data_tools.escalate_to_human("ORD-001", "Customer complaint", 200.0)
        assert result["status"] == "pending_human_approval"
        assert result["order_id"] == "ORD-001"