#!/usr/bin/env python3
"""
EVALS Test Suite: Multi-Constraint Offer Optimizer & Three-Value Engine
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts"))

from offer_optimizer import OfferOptimizer

def test_three_value_model_and_offer_bands():
    optimizer = OfferOptimizer()
    res = optimizer.optimize_offer_price(
        normalized_noi=50000.0,
        sales_comp_fmv=520000.0,
        market_cap_rate_pct=8.0, # Income Value = 50k / 8% = $625,000
        target_cap_rate_pct=10.0,
        target_coc_pct=10.0,
        min_dscr=1.25,
        min_monthly_cash_flow=400.0,
        down_payment_pct=20.0,
        interest_rate_pct=7.0,
        loan_years=20
    )

    three_vals = res["three_values"]
    assert three_vals["sales_comp_fmv"] == 520000.0
    assert three_vals["income_approach_value"] == 625000.0
    assert three_vals["investor_max_value"] > 0.0

    bands = res["offer_price_bands"]
    # Aggressive < Recommended < Max Rational <= Market Ceiling
    assert bands["aggressive_offer"] < bands["recommended_offer"]
    assert bands["recommended_offer"] <= bands["maximum_rational_offer"]
    assert bands["maximum_rational_offer"] <= bands["market_value_ceiling"]

def test_dscr_calculation():
    optimizer = OfferOptimizer()
    # NOI = $50,000, Annual Debt = $35,000 => DSCR = 1.43
    dscr = optimizer.calculate_dscr(50000.0, 35000.0)
    assert dscr == 1.43
