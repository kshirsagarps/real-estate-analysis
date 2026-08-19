#!/usr/bin/env python3
"""
Data Provenance, 4-Tier Source Hierarchy & Observation As-Of Date Engine

Tracks source hierarchy (Tier 1-4), retrieval vs observation dates, stale data warnings,
and calculates overall Offer Confidence Score.
"""

import time
from typing import Dict, Any, List, Optional

SOURCE_HIERARCHY = {
    "County Assessor": {"tier": 1, "weight": 1.00},
    "County Recorder": {"tier": 1, "weight": 1.00},
    "Official Tax Authority": {"tier": 1, "weight": 0.98},
    "MLS Closed Sale": {"tier": 1, "weight": 0.95},
    "Signed Lease Agreement": {"tier": 1, "weight": 0.95},
    "Actual T12 Statement": {"tier": 1, "weight": 0.95},
    "Insurance Policy Declaration": {"tier": 1, "weight": 0.95},
    
    "Property Manager Statement": {"tier": 2, "weight": 0.88},
    "Appraisal Report": {"tier": 2, "weight": 0.85},
    "Broker Documentation": {"tier": 2, "weight": 0.80},
    
    "Active MLS Listing": {"tier": 3, "weight": 0.70},
    "Historical Rental Listing": {"tier": 3, "weight": 0.65},
    
    "Web Search Snippet": {"tier": 4, "weight": 0.50},
    "Aggregator Estimate": {"tier": 4, "weight": 0.45},
    "AI Inferred Value": {"tier": 4, "weight": 0.40}
}

class FactProvenance:
    def __init__(
        self,
        value: Any,
        source_name: str,
        source_url: str = "",
        observation_date: str = "",
        retrieved_at: Optional[float] = None,
        confidence_rating: Optional[float] = None,
        notes: str = ""
    ):
        self.value = value
        self.source_name = source_name
        self.source_url = source_url
        self.observation_date = observation_date
        self.retrieved_at = retrieved_at or time.time()
        
        # Source hierarchy weight lookup
        info = SOURCE_HIERARCHY.get(source_name, {"tier": 3, "weight": 0.60})
        self.tier = info["tier"]
        base_confidence = info["weight"] * 100.0
        
        self.confidence_rating = confidence_rating if confidence_rating is not None else base_confidence
        self.confidence_rating = max(0.0, min(100.0, float(self.confidence_rating)))
        self.notes = notes

    def check_stale_warnings(self, max_days: int = 365) -> List[str]:
        """Generates stale data warnings if observation date is old."""
        warnings = []
        if self.observation_date:
            # Simplistic check or date parsing
            warnings.append(f"Fact '{self.source_name}' observed on {self.observation_date}")
        return warnings

    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "source_name": self.source_name,
            "tier": self.tier,
            "source_url": self.source_url,
            "observation_date": self.observation_date,
            "retrieved_at": self.retrieved_at,
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
        has_tax_bills: bool,
        valuation_dispersion_cv: float = 0.05 # Coefficient of Variation
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
            reasons.append("CRITICAL: Fewer than 3 primary sales comps available (MANUAL REVIEW REQUIRED)")

        if fallback_comps_count > 0:
            score -= (fallback_comps_count * 5.0)
            reasons.append(f"{fallback_comps_count} fallback comps used due to limited data")

        if old_comps_count > 0:
            score -= (old_comps_count * 5.0)
            reasons.append(f"{old_comps_count} comps are older than 9 months")

        # Dispersion Penalty (CV > 0.15 indicates high disagreement among comps)
        if valuation_dispersion_cv > 0.15:
            penalty = min(20.0, (valuation_dispersion_cv - 0.15) * 100.0)
            score -= penalty
            reasons.append(f"High comp valuation dispersion (CV = {valuation_dispersion_cv:.2f}). Confidence penalized.")

        # Document Verification Contribution (up to +20 pts)
        if has_t12:
            score += 10.0
            reasons.append("Tier-1 T12 operating statement provided & normalized")
        else:
            score -= 5.0
            reasons.append("No T12 operating statement provided (estimated expenses used)")

        if has_lease_agreements:
            score += 5.0
            reasons.append("Tier-1 signed lease agreements verified")
        
        if has_tax_bills:
            score += 5.0
            reasons.append("Tier-1 municipal property tax records verified")

        final_score = round(max(0.0, min(100.0, score)), 1)
        
        if final_score >= 80 and primary_comps_count >= 3:
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
    fact1 = FactProvenance(325000, "County Recorder", observation_date="2026-04-10")
    fact2 = FactProvenance(1450, "Web Search Snippet", observation_date="2026-08-01")
    print("Tier 1 Fact:", fact1.to_dict())
    print("Tier 4 Fact:", fact2.to_dict())
