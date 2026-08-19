#!/usr/bin/env python3
"""
Deterministic Comp Eligibility, Similarity Scoring, Valuation Dispersion, and Trimmed FMV Engine

Implements:
1. Comp Eligibility Funnel (Property Type & Unit Count Tiering)
2. Comp Similarity Score (0-100)
3. Outlier Exclusions (Distressed/Foreclosure/Extreme PPSF outliers)
4. Valuation Dispersion & Coefficient of Variation (CV)
5. Weighted Trimmed-Mean Sales Comp Valuation
6. Low Comp Count Safeguard (<3 primary comps trigger MANUAL COMP REVIEW REQUIRED)
"""

import math
from typing import Dict, Any, List, Tuple

class CompEngine:
    def __init__(self):
        pass

    def evaluate_comp_eligibility(self, subject: Dict[str, Any], comp: Dict[str, Any]) -> Tuple[str, float, str]:
        """
        Evaluates Comp Eligibility Tier (Primary, Secondary, Fallback, Excluded).
        """
        subj_type = subject.get("property_type", "multi_family").lower()
        comp_type = comp.get("property_type", "multi_family").lower()
        subj_units = int(subject.get("unit_count", 4))
        comp_units = int(comp.get("unit_count", 4))

        # Tier 1: Property Type Match
        if subj_type != comp_type:
            if subj_type == "multi_family" and comp_type in ["single_family", "condo"]:
                return ("Excluded", 0.0, "Rejected: Single-Family/Condo comp for Multi-Family subject")
            elif subj_type == "multi_family" and comp_type == "commercial_complex":
                return ("Excluded", 0.0, "Rejected: Commercial complex comp for Residential Multi-Family subject")

        # Tier 2: Unit Count Similarity
        unit_diff = abs(subj_units - comp_units)
        if unit_diff == 0:
            return ("Primary (Tier A)", 1.0, "Exact unit count match")
        elif unit_diff == 1:
            return ("Secondary (Tier B)", 0.85, "Unit count within +/- 1 unit")
        elif unit_diff == 2:
            return ("Fallback (Tier C)", 0.70, "Unit count within +/- 2 units (penalty applied)")
        else:
            return ("Excluded", 0.0, f"Rejected: Unit count difference too large ({comp_units} vs {subj_units})")

    def calculate_comp_similarity_score(
        self,
        subject: Dict[str, Any],
        comp: Dict[str, Any],
        tier_weight: float
    ) -> float:
        """Calculates Comp Similarity Score (0-100)."""
        dist_miles = float(comp.get("distance_miles", 1.0))
        dist_score = max(0.0, 100.0 - (dist_miles * 30.0))

        days_ago = int(comp.get("days_since_sale", 60))
        recency_score = max(0.0, 100.0 - (days_ago / 3.65))

        subj_sf = float(subject.get("building_sf", 4000))
        comp_sf = float(comp.get("building_sf", 4000))
        sf_diff_pct = abs(subj_sf - comp_sf) / max(subj_sf, 1.0)
        sf_score = max(0.0, 100.0 - (sf_diff_pct * 200.0))

        subj_year = int(subject.get("year_built", 1950))
        comp_year = int(comp.get("year_built", 1950))
        year_diff = abs(subj_year - comp_year)
        year_score = max(0.0, 100.0 - (year_diff * 2.5))

        base_match = tier_weight * 100.0

        similarity_score = (
            (base_match * 0.50) +
            (dist_score * 0.15) +
            (recency_score * 0.10) +
            (sf_score * 0.10) +
            (year_score * 0.05) +
            (90.0 * 0.05) +
            (90.0 * 0.05)
        )

        return round(max(0.0, min(100.0, similarity_score)), 1)

    def is_outlier(self, comp: Dict[str, Any], median_ppsf: float) -> Tuple[bool, str]:
        """Detects whether a comp is an outlier."""
        is_distressed = comp.get("is_distressed", False) or comp.get("is_foreclosure", False)
        if is_distressed:
            return (True, "Excluded: Foreclosure / Distressed Transaction")

        price = float(comp.get("sale_price", 0))
        sf = float(comp.get("building_sf", 1))
        ppsf = price / max(sf, 1.0)

        if median_ppsf > 0:
            if ppsf > (median_ppsf * 2.5):
                return (True, f"Excluded: High PPSF Outlier (${ppsf:.1f}/sqft vs median ${median_ppsf:.1f}/sqft)")
            elif ppsf < (median_ppsf * 0.4):
                return (True, f"Excluded: Low PPSF Outlier (${ppsf:.1f}/sqft vs median ${median_ppsf:.1f}/sqft)")

        return (False, "Valid Comp")

    def time_adjust_sale_price(self, sale_price: float, days_since_sale: int, annual_trend_rate: float = -0.032) -> float:
        """Adjusts historical sale price to current market date using local trend rate."""
        years_ago = days_since_sale / 365.0
        adjusted_price = sale_price * (1.0 + (annual_trend_rate * years_ago))
        return round(adjusted_price, 2)

    def calculate_valuation_dispersion(self, prices: List[float]) -> Tuple[float, float]:
        """Calculates Standard Deviation, Coefficient of Variation (CV), and Interquartile Range (IQR)."""
        if not prices or len(prices) < 2:
            return 0.0, 0.0
        
        mean_val = sum(prices) / len(prices)
        variance = sum((p - mean_val) ** 2 for p in prices) / len(prices)
        std_dev = math.sqrt(variance)
        cv = std_dev / max(mean_val, 1.0)

        sorted_prices = sorted(prices)
        n = len(sorted_prices)
        q1 = sorted_prices[n // 4]
        q3 = sorted_prices[(3 * n) // 4]
        iqr = q3 - q1

        return round(cv, 3), round(iqr, 2)

    def calculate_sales_comp_fmv(self, subject: Dict[str, Any], raw_comps: List[Dict[str, Any]], annual_trend_rate: float = -0.032) -> Dict[str, Any]:
        """
        Runs the complete Comp Eligibility Funnel, Time Adjustment, Outlier Exclusion,
        Valuation Dispersion Analysis, and Trimmed-Mean Weighted FMV.
        """
        ppsfs = [c["sale_price"] / max(float(c.get("building_sf", 1)), 1.0) for c in raw_comps if c.get("sale_price", 0) > 0]
        median_ppsf = sorted(ppsfs)[len(ppsfs)//2] if ppsfs else 0.0

        evaluated_comps = []
        valid_prices = []
        valid_weights = []
        primary_count = 0
        fallback_count = 0

        for c in raw_comps:
            tier_name, tier_weight, tier_reason = self.evaluate_comp_eligibility(subject, c)
            if tier_name == "Excluded":
                c_copy = dict(c)
                c_copy.update({"status": "Excluded", "reason": tier_reason, "similarity_score": 0.0})
                evaluated_comps.append(c_copy)
                continue

            is_out, out_reason = self.is_outlier(c, median_ppsf)
            if is_out:
                c_copy = dict(c)
                c_copy.update({"status": "Excluded", "reason": out_reason, "similarity_score": 0.0})
                evaluated_comps.append(c_copy)
                continue

            adj_price = self.time_adjust_sale_price(c["sale_price"], c.get("days_since_sale", 0), annual_trend_rate)
            similarity_score = self.calculate_comp_similarity_score(subject, c, tier_weight)
            weight = (similarity_score / 100.0) * tier_weight

            valid_prices.append(adj_price)
            valid_weights.append(weight)

            if "Primary" in tier_name:
                primary_count += 1
            else:
                fallback_count += 1

            c_copy = dict(c)
            c_copy.update({
                "status": "Selected",
                "tier": tier_name,
                "similarity_score": similarity_score,
                "time_adjusted_price": adj_price,
                "weight": round(weight, 3),
                "reason": tier_reason
            })
            evaluated_comps.append(c_copy)

        # Dispersion Analysis
        cv, iqr = self.calculate_valuation_dispersion(valid_prices)

        # Low Comp Safeguard Check
        requires_manual_review = primary_count < 3
        safeguard_warning = "MANUAL COMP REVIEW REQUIRED: Fewer than 3 primary comps available." if requires_manual_review else "Comp count sufficient."

        # Trimmed Weighted Mean calculation
        if len(valid_prices) >= 4:
            # Sort prices & weights by price, trim top and bottom 10%
            pairs = sorted(zip(valid_prices, valid_weights), key=lambda x: x[0])
            trim_n = max(1, len(pairs) // 5)
            trimmed_pairs = pairs[trim_n:-trim_n] if len(pairs) > (2 * trim_n) else pairs
            total_weighted_val = sum(p * w for p, w in trimmed_pairs)
            total_w = sum(w for p, w in trimmed_pairs)
        else:
            total_weighted_val = sum(p * w for p, w in zip(valid_prices, valid_weights))
            total_w = sum(valid_weights)

        sales_comp_fmv = (total_weighted_val / total_w) if total_w > 0 else 0.0

        return {
            "sales_comp_fmv": round(sales_comp_fmv, 2),
            "primary_comps_count": primary_count,
            "fallback_comps_count": fallback_count,
            "valuation_dispersion_cv": cv,
            "iqr": iqr,
            "requires_manual_review": requires_manual_review,
            "safeguard_warning": safeguard_warning,
            "evaluated_comps": evaluated_comps
        }

if __name__ == "__main__":
    engine = CompEngine()
    subject = {"property_type": "multi_family", "unit_count": 5, "building_sf": 5194}
    raw_comps = [
        {"address": "Comp 1", "property_type": "multi_family", "unit_count": 5, "sale_price": 540000, "building_sf": 5000, "days_since_sale": 30},
        {"address": "Comp 2", "property_type": "multi_family", "unit_count": 4, "sale_price": 495000, "building_sf": 4400, "days_since_sale": 60},
        {"address": "Comp 3", "property_type": "multi_family", "unit_count": 5, "sale_price": 525000, "building_sf": 5100, "days_since_sale": 120}
    ]
    res = engine.calculate_sales_comp_fmv(subject, raw_comps)
    print("Comp Engine Test:")
    import json
    print(json.dumps(res, indent=2))
