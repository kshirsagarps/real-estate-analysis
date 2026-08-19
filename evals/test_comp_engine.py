#!/usr/bin/env python3
"""
EVALS Test Suite: Comp Eligibility Funnel, Similarity Scoring & Weighted Valuation
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts"))

from comp_engine import CompEngine

def test_comp_eligibility_funnel():
    engine = CompEngine()
    subj = {"property_type": "multi_family", "unit_count": 4}

    # Exact match -> Primary
    tier_exact, penalty_exact, _ = engine.evaluate_comp_eligibility(subj, {"property_type": "multi_family", "unit_count": 4})
    assert "Primary" in tier_exact

    # +/- 1 unit -> Secondary
    tier_sec, penalty_sec, _ = engine.evaluate_comp_eligibility(subj, {"property_type": "multi_family", "unit_count": 5})
    assert "Secondary" in tier_sec

    # Single family comp for multi-family subject -> Excluded
    tier_ex, _, _ = engine.evaluate_comp_eligibility(subj, {"property_type": "single_family", "unit_count": 1})
    assert tier_ex == "Excluded"

def test_outlier_detection():
    engine = CompEngine()

    # Foreclosure should be flagged
    is_out, reason = engine.is_outlier({"is_foreclosure": True, "sale_price": 200000, "building_sf": 4000}, median_ppsf=100.0)
    assert is_out is True
    assert "Foreclosure" in reason

    # High PPSF outlier ($300/sqft vs median $100/sqft)
    is_out_high, reason_high = engine.is_outlier({"sale_price": 1200000, "building_sf": 4000}, median_ppsf=100.0)
    assert is_out_high is True
    assert "High PPSF Outlier" in reason_high

def test_time_adjustment():
    engine = CompEngine()
    # $500k comp sold 365 days ago with -3.2% annual trend rate => $484,000
    adj_price = engine.time_adjust_sale_price(500000.0, days_since_sale=365, annual_trend_rate=-0.032)
    assert adj_price == 484000.0
