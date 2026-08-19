#!/usr/bin/env python3
"""
EVALS Test Suite: Property Fact Reconciliation Engine
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts"))

from provenance import FactProvenance
from fact_reconciler import FactReconciler

def test_fact_reconciliation_conflict_resolution():
    reconciler = FactReconciler()
    unit_observations = [
        FactProvenance(5, "County Assessor", confidence_rating=95.0),
        FactProvenance(5, "Tax Records", confidence_rating=95.0),
        FactProvenance(4, "MLS Listing", confidence_rating=75.0)
    ]

    res = reconciler.reconcile_fact("unit_count", unit_observations)
    assert res["canonical_value"] == 5
    assert res["has_conflict"] is True
    assert len(res["evidence"]) == 3
