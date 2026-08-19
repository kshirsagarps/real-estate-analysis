#!/usr/bin/env python3
"""
Data Provenance & Confidence Engine

Tracks source, retrieval metadata, transaction dates, and confidence ratings
for every property data field and comp. Calculates overall Offer Confidence Score.
"""

import time
from typing import Dict, Any, List, Optional

class FactProvenance:
    def __init__(
        self,
        value: Any,
        source_name: str,
        source_url: str = "",
        retrieved_at: Optional[float] = None,
        transaction_date: str = "",
        confidence_rating: float = 100.0,
        notes: str = ""
    ):
        self.value = value
        self.source_name = source_name
        self.source_url = source_url
        self.retrieved_at = retrieved_at or time.time()
        self.transaction_date = transaction_date
        self.confidence_rating = max(0.0, min(100.0, float(confidence_rating)))
        self.notes = notes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "source_name": self.source_name,
            "source_url": self.source_url,
            "retrieved_at": self.retrieved_at,
            "transaction_date": self.transaction_date,
            "confidence_rating": self.confidence_rating,
            "notes": self.notes
        }

class OfferConfidenceEvaluator:
    def evaluate_offer_confidence(
        self,
        comps_count: int,
        primary_comps_count: int,
        fallback_comps_count: int,
        old_comps_count: int,
        has_t12: bool,
        has_lease_agreements: bool,
        has_tax_bills: bool
    ) -> Dict[str, Any]:
        """Calculates overall Offer Confidence Score (0-100) and reason codes."""
        score = 50.0 # Base score
        reasons = []

        # Comp Quality Contribution (up to +30 pts)
        if primary_comps_count >= 3:
            score += 20.0
            reasons.append(f"{primary_comps_count} high-quality primary sales comps available")
        elif primary_comps_count >= 1:
            score += 10.0
            reasons.append(f"Only {primary_comps_count} primary sales comp available")
        else:
            score -= 15.0
            reasons.append("No exact primary property-type sales comps available")

        if fallback_comps_count > 0:
            score -= (fallback_comps_count * 5.0)
            reasons.append(f"{fallback_comps_count} fallback comps used due to limited data")

        if old_comps_count > 0:
            score -= (old_comps_count * 5.0)
            reasons.append(f"{old_comps_count} comps are older than 9 months")

        # Document Verification Contribution (up to +20 pts)
        if has_t12:
            score += 10.0
            reasons.append("T12 operating statement provided & normalized")
        else:
            score -= 5.0
            reasons.append("No T12 operating statement provided (estimated expenses used)")

        if has_lease_agreements:
            score += 5.0
            reasons.append("Signed lease agreements verified")
        
        if has_tax_bills:
            score += 5.0
            reasons.append("Verified municipal property tax records")

        final_score = round(max(0.0, min(100.0, score)), 1)
        
        if final_score >= 80:
            level = "HIGH"
        elif final_score >= 60:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {
            "offer_confidence_score": final_score,
            "confidence_level": level,
            "reasons": reasons
        }

if __name__ == "__main__":
    fact = FactProvenance(325000, "County Assessor", "https://county.gov/tax/123", confidence_rating=95.0)
    print("Fact Provenance Test:", fact.to_dict())
    evaluator = OfferConfidenceEvaluator()
    res = evaluator.evaluate_offer_confidence(
        comps_count=4, primary_comps_count=3, fallback_comps_count=1,
        old_comps_count=1, has_t12=True, has_lease_agreements=True, has_tax_bills=True
    )
    print("Offer Confidence Test:", res)
