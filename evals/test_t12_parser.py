#!/usr/bin/env python3
"""
EVALS Test Suite: T12 Financial Statement Parser
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts"))

from parse_t12 import T12Parser

def test_t12_parsing():
    sample_t12 = {
        "gross_potential_rent": 200000.0,
        "vacancy_loss": 10000.0,
        "other_income": 5000.0,
        "property_taxes": 20000.0,
        "insurance": 8000.0,
        "utilities": 12000.0,
        "management_fees": 15000.0,
        "repairs_maintenance": 10000.0,
        "admin_other": 3000.0
    }
    parser = T12Parser()
    res = parser.parse_dict(sample_t12)

    # EGI = 200,000 - 10,000 + 5,000 = 195,000
    assert res["effective_gross_income"] == 195000.0
    # Total Expenses = 20k+8k+12k+15k+10k+3k = 68,000
    assert res["expenses"]["total_operating_expenses"] == 68000.0
    # NOI = 195,000 - 68,000 = 127,000
    assert res["net_operating_income"] == 127000.0
    # Expense Ratio = 68,000 / 195,000 * 100 = 34.87%
    assert res["expense_ratio_pct"] == 34.87
