#!/usr/bin/env python3
"""
EVALS Test Suite: Property Composite Scoring Engine
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts"))

from score_property import compute_property_score, get_grade_and_signal

def test_score_bounds_and_weights():
    # 80*0.25 + 80*0.20 + 80*0.20 + 80*0.20 + 80*0.15 = 80.0
    res = compute_property_score(80, 80, 80, 80, 80)
    assert res["composite_score"] == 80.0
    assert res["grade"] == "A"

def test_grade_thresholds():
    assert get_grade_and_signal(90.0)[0] == "A+"
    assert get_grade_and_signal(75.0)[0] == "A"
    assert get_grade_and_signal(60.0)[0] == "B"
    assert get_grade_and_signal(45.0)[0] == "C"
    assert get_grade_and_signal(30.0)[0] == "D"
    assert get_grade_and_signal(15.0)[0] == "F"

def test_out_of_bounds_clamping():
    # Inputs out of 0-100 range should be clamped
    res = compute_property_score(150, -50, 100, 100, 100)
    # clamped: v=100, inc=0, n=100, u=100, m=100
    # 100*0.25 + 0*0.20 + 100*0.20 + 100*0.20 + 100*0.15 = 25+0+20+20+15 = 80.0
    assert res["composite_score"] == 80.0
