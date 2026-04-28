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

"""Tools for the customer support specialist agents."""

from app.tools.data_tools import (
    check_inventory,
    escalate_to_human,
    get_order_status,
    get_product_details,
    get_recommendations,
    get_shipment_tracking,
    issue_refund,
    list_orders,
    process_return,
    search_products,
)

__all__ = [
    "get_order_status",
    "get_shipment_tracking",
    "check_inventory",
    "list_orders",
    "search_products",
    "get_product_details",
    "get_recommendations",
    "process_return",
    "issue_refund",
    "escalate_to_human",
]
