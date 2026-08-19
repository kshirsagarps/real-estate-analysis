#!/usr/bin/env python3
"""
Complete Industrial-Grade Underwriting & Offer Price Engine Execution Script

Demonstrates end-to-end data provenance, fact reconciliation, T12 anomaly auditing,
comp eligibility funnel, similarity scoring, 3-value model, and multi-constraint MAO solver.
"""

import json
from provenance import FactProvenance, OfferConfidenceEvaluator
from fact_reconciler import FactReconciler
from t12_auditor import T12Auditor
from comp_engine import CompEngine
from offer_optimizer import OfferOptimizer
from score_property import compute_property_score
from memory_engine import MemoryEngine
from generate_pdf import generate_pdf_report

def run_underwriting():
    print("=" * 70)
    print("  RUNNING DETERMINISTIC COMP & MULTI-CONSTRAINT OFFER ENGINE")
    print("=" * 70)

    # 1. Fact Reconciliation
    reconciler = FactReconciler()
    unit_obs = [
        FactProvenance(5, "County Assessor", confidence_rating=95.0),
        FactProvenance(5, "Tax Records", confidence_rating=95.0),
        FactProvenance(5, "Rent Roll / Leases", confidence_rating=90.0)
    ]
    reconciled_units = reconciler.reconcile_fact("unit_count", unit_obs)
    canonical_unit_count = reconciled_units["canonical_value"]

    # 2. T12 Audit & Expense Normalization
    raw_t12 = {
        "gross_potential_rent": 73908.0, # Unit 1-4 leases + Unit 5 @ $1,100/mo
        "vacancy_loss": 0.0,             # Seller reported 0 vacancy
        "other_income": 0.0,
        "property_taxes": 2676.38,
        "insurance": 4215.00,
        "utilities": 880.0 + 350.0,      # Sewer & Garbage
        "management_fees": 0.0,          # Seller self-managed
        "repairs_maintenance": 3510.63,
        "admin_other": 0.0
    }

    auditor = T12Auditor()
    t12_res = auditor.audit_and_normalize(
        raw_t12,
        purchase_price=500000.0,
        unit_count=canonical_unit_count,
        landlord_water_annual=2400.0,
        landlord_common_electric_annual=600.0
    )
    normalized_noi = t12_res["normalized_noi"] # $53,825.27

    # 3. Comp Eligibility Funnel & Quality Scoring
    comp_engine = CompEngine()
    subject = {
        "property_type": "multi_family",
        "unit_count": canonical_unit_count,
        "building_sf": 5194,
        "year_built": 1930
    }
    raw_comps = [
        {"address": "Comp 1: 140 N Hancock St (5-unit)", "property_type": "multi_family", "unit_count": 5, "sale_price": 540000, "building_sf": 5000, "days_since_sale": 30, "distance_miles": 0.3},
        {"address": "Comp 2: 88 E Northampton St (4-unit)", "property_type": "multi_family", "unit_count": 4, "sale_price": 495000, "building_sf": 4400, "days_since_sale": 60, "distance_miles": 0.5},
        {"address": "Comp 3: 210 S Main St (5-unit)", "property_type": "multi_family", "unit_count": 5, "sale_price": 525000, "building_sf": 5100, "days_since_sale": 120, "distance_miles": 0.8},
        {"address": "Comp 4: 12 SFH Distress (1-unit)", "property_type": "single_family", "unit_count": 1, "sale_price": 220000, "building_sf": 1800, "days_since_sale": 15, "distance_miles": 0.2} # Should be excluded by funnel
    ]
    comp_res = comp_engine.calculate_sales_comp_fmv(subject, raw_comps)
    sales_comp_fmv = comp_res["sales_comp_fmv"]

    # 4. Multi-Constraint Offer Price Optimization & 4-Tier Bands
    optimizer = OfferOptimizer()
    offer_res = optimizer.optimize_offer_price(
        normalized_noi=normalized_noi,
        sales_comp_fmv=sales_comp_fmv,
        market_cap_rate_pct=8.5,
        target_cap_rate_pct=10.0,
        target_coc_pct=12.0,
        min_dscr=1.25,
        min_monthly_cash_flow=500.0,
        down_payment_pct=20.0,
        interest_rate_pct=7.0,
        loan_years=20
    )

    # 5. Offer Data Provenance & Confidence Evaluation
    evaluator = OfferConfidenceEvaluator()
    conf_res = evaluator.evaluate_offer_confidence(
        comps_count=len(comp_res["evaluated_comps"]),
        primary_comps_count=comp_res["primary_comps_count"],
        fallback_comps_count=comp_res["fallback_comps_count"],
        old_comps_count=0,
        has_t12=True,
        has_lease_agreements=True,
        has_tax_bills=True
    )

    # Output Summary
    print(f"Property: 273-275 New Hancock Street, Wilkes-Barre PA")
    print(f"Offer Confidence: {conf_res['confidence_level']} ({conf_res['offer_confidence_score']}/100)")
    print(f"Normalized NOI: ${normalized_noi:,.2f} (Seller NOI was ${t12_res['seller_noi']:,.2f})")
    print("-" * 70)
    print("THREE DISTINCT VALUES:")
    print(f"  1. Sales Comp FMV:         ${offer_res['three_values']['sales_comp_fmv']:,.2f}")
    print(f"  2. Income Approach Value:  ${offer_res['three_values']['income_approach_value']:,.2f}")
    print(f"  3. Investor Max Value:     ${offer_res['three_values']['investor_max_value']:,.2f}")
    print("-" * 70)
    print("FOUR-TIER OFFER PRICE BANDS:")
    bands = offer_res["offer_price_bands"]
    print(f"  • Aggressive Offer:       ${bands['aggressive_offer']:,.2f}")
    print(f"  • Recommended Offer:      ${bands['recommended_offer']:,.2f}")
    print(f"  • Max Rational Offer:     ${bands['maximum_rational_offer']:,.2f}")
    print(f"  • Market Value Ceiling:   ${bands['market_value_ceiling']:,.2f}")
    print("=" * 70)

if __name__ == "__main__":
    run_underwriting()
