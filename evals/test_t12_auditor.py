#!/usr/bin/env python3
"""
EVALS Test Suite: T12 Expense Normalization & Anomaly Auditor
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts"))

from t12_auditor import T12Auditor

def test_t12_anomaly_detection_and_normalization():
    auditor = T12Auditor()
    raw_seller_t12 = {
        "gross_potential_rent": 100000.0,
        "vacancy_loss": 0.0, # Seller reported 0 vacancy!
        "other_income": 0.0,
        "property_taxes": 3000.0,
        "insurance": 4000.0,
        "utilities": 2000.0,
        "management_fees": 0.0, # Seller self-managed!
        "repairs_maintenance": 5000.0,
        "admin_other": 0.0,
        "capex_reserves": 0.0 # Omitted CapEx!
    }

    res = auditor.audit_and_normalize(
        raw_seller_t12,
        purchase_price=500000.0,
        tax_reassessment_rate=0.015, # Reassessed tax = $7,500
        min_vacancy_pct=5.0,         # Normalized vacancy = $5,000
        unit_count=5
    )

    # Seller NOI = 100,000 - 14,000 = 86,000
    assert res["seller_noi"] == 86000.0

    # Reassessed tax = max(3000, 500k * 1.5%) = $7,500
    assert res["expenses"]["reassessed_tax"] == 7500.0

    # Normalized EGI = 100k - 5k = 95k
    # Normalized Mgmt = 5% of 95k = $4,750
    # Normalized CapEx = 5 * $300 = $1,500
    # Total Normalized Exp = 7500 + 4000 + 2000 + 4750 + 5000 + 1500 = 24,750
    # Normalized NOI = 95,000 - 24,750 = 70,250
    assert res["normalized_noi"] == 70250.0

    # Anomalies detected list should contain flags for vacancy, taxes, mgmt, capex
    assert len(res["anomalies_detected"]) >= 3
