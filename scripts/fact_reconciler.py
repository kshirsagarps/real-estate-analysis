#!/usr/bin/env python3
"""
Property Fact Reconciliation Engine

Reconciles conflicting facts (unit counts, building SF, taxes, year built)
across County Assessor, MLS, Rent Rolls, and Listing Pages.
"""

from typing import Dict, Any, List
from provenance import FactProvenance

class FactReconciler:
    def reconcile_fact(self, field_name: str, observations: List[FactProvenance]) -> Dict[str, Any]:
        """
        Reconciles multiple sources for a single property attribute.
        Prioritizes official public records (County/Tax) over marketing listings.
        """
        if not observations:
            return {"canonical_value": None, "confidence": 0.0, "has_conflict": False, "evidence": []}

        source_weights = {
            "County Assessor": 1.0,
            "Tax Records": 0.95,
            "Rent Roll / Leases": 0.90,
            "T12 Statement": 0.85,
            "MLS Listing": 0.75,
            "Web Listing": 0.60
        }

        # Check for conflicts
        values = [obs.value for obs in observations]
        unique_values = list(set(values))
        has_conflict = len(unique_values) > 1

        # Calculate weighted voting score for each value
        value_scores = {}
        evidence_list = []
        for obs in observations:
            weight = source_weights.get(obs.source_name, 0.5) * (obs.confidence_rating / 100.0)
            value_scores[obs.value] = value_scores.get(obs.value, 0.0) + weight
            evidence_list.append(f"{obs.source_name}: {obs.value} (Confidence: {obs.confidence_rating}%)")

        canonical_value = max(value_scores, key=value_scores.get)
        
        # Calculate confidence
        total_weight = sum(value_scores.values())
        canonical_weight = value_scores[canonical_value]
        confidence = round(min(100.0, (canonical_weight / max(total_weight, 0.01)) * 95.0), 1)
        if not has_conflict:
            confidence = min(100.0, confidence + 5.0)

        return {
            "field_name": field_name,
            "canonical_value": canonical_value,
            "confidence": confidence,
            "has_conflict": has_conflict,
            "evidence": evidence_list
        }

if __name__ == "__main__":
    reconciler = FactReconciler()
    unit_count_obs = [
        FactProvenance(4, "County Assessor", confidence_rating=95.0),
        FactProvenance(4, "Tax Records", confidence_rating=95.0),
        FactProvenance(4, "Rent Roll / Leases", confidence_rating=90.0),
        FactProvenance(3, "MLS Listing", confidence_rating=75.0) # Conflicting MLS
    ]
    res = reconciler.reconcile_fact("unit_count", unit_count_obs)
    print("Fact Reconciliation Test:")
    import json
    print(json.dumps(res, indent=2))
