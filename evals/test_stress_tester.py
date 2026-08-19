#!/usr/bin/env python3
"""
EVALS Test Suite: Mandatory Underwriting Stress Testing Engine
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts"))

from stress_tester import StressTester

def test_stress_tester_scenarios():
    tester = StressTester()
    res = tester.run_stress_test(
        gpr=100000.0,
        current_tax=3000.0,
        reassessed_tax=7500.0,
        current_insurance=4000.0,
        updated_insurance=4000.0,
        utilities=3000.0,
        pm_fee=2500.0,
        maintenance=5000.0,
        purchase_price=500000.0,
        down_payment_pct=20.0,
        interest_rate_pct=7.0,
        loan_years=20
    )

    assert "base_scenario" in res
    assert "post_acquisition_scenario" in res
    assert "stress_scenario" in res

    # Base NOI vs Post-Acquisition NOI vs Stress NOI
    assert res["base_scenario"]["noi"] > res["post_acquisition_scenario"]["noi"]
    assert res["post_acquisition_scenario"]["noi"] > res["stress_scenario"]["noi"]
