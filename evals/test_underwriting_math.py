#!/usr/bin/env python3
"""
EVALS Test Suite: Underwriting Financial Mathematics
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts"))

from score_property import (
    calculate_noi,
    calculate_cap_rate,
    calculate_cash_on_cash,
    calculate_mao
)

def test_calculate_noi():
    # EGI: $100,000, Operating Expenses: $40,000 => NOI: $60,000
    noi = calculate_noi(100000.0, 40000.0)
    assert noi == 60000.0

def test_calculate_cap_rate():
    # NOI: $60,000, Purchase Price: $1,000,000 => Cap Rate: 6.0%
    cap_rate = calculate_cap_rate(60000.0, 1000000.0)
    assert cap_rate == 6.0

def test_calculate_cap_rate_zero_price():
    assert calculate_cap_rate(60000.0, 0.0) == 0.0

def test_calculate_cash_on_cash():
    # Annual cash flow: $12,000, Cash invested: $100,000 => CoC: 12.0%
    coc = calculate_cash_on_cash(12000.0, 100000.0)
    assert coc == 12.0

def test_calculate_mao():
    # NOI: $65,000, Target Cap Rate: 6.5% => Valuation: $1,000,000
    # Rehab: $50,000, Profit: $50,000 => MAO: $900,000
    mao = calculate_mao(65000.0, 6.5, capex_rehab=50000.0, desired_profit=50000.0)
    assert mao == 900000.0
