#!/usr/bin/env python3
"""
Industrial-Grade Phase 2 Underwriting Execution Script

Demonstrates:
1. Candidate Comp Discovery separation
2. Fact Reconciliation & Provenance 4-Tier Hierarchy
3. T12 Normalization & Tax Reassessment
4. Comp Eligibility Funnel, Similarity Scoring & Dispersion (CV, IQR)
5. Mandatory Stress Testing Engine (Base vs Post-Acquisition vs Stress)
6. Strategy-Specific MAO (Buy-Hold vs BRRRR vs Flip)
7. 4-Tier Offer Price Bands & Hard Walk-Away Price
"""

import json
from provenance import FactProvenance, OfferConfidenceEvaluator
from fact_reconciler import FactReconciler
from t12_auditor import T12Auditor
from comp_engine import CompEngine
from stress_tester import StressTester
from offer_optimizer import OfferOptimizer
from score_property import compute_property_score
from memory_engine import MemoryEngine
from generate_pdf import generate_pdf_report

def run_underwriting():
    print("=" * 75)
    print("  RUNNING PHASE 2 INDUSTRIAL-GRADE COMP & OFFER ENGINE")
    print("=" * 75)

    # 1. Fact Reconciliation with 4-Tier Provenance
    reconciler = FactReconciler()
    unit_obs = [
        FactProvenance(5, "County Assessor", observation_date="2026-04-10", confidence_rating=98.0), # Tier 1
        FactProvenance(5, "Official Tax Authority", observation_date="2026-05-01", confidence_rating=95.0), # Tier 1
        FactProvenance(5, "Signed Lease Agreement", observation_date="2026-06-17", confidence_rating=95.0) # Tier 1
    ]
    reconciled_units = reconciler.reconcile_fact("unit_count", unit_obs)
    canonical_unit_count = reconciled_units["canonical_value"]

    # 2. T12 Audit & Normalization
    raw_t12 = {
        "gross_potential_rent": 73908.0,
        "vacancy_loss": 0.0,
        "other_income": 0.0,
        "property_taxes": 2676.38,
        "insurance": 4215.00,
        "utilities": 880.0 + 350.0,
        "management_fees": 0.0,
        "repairs_maintenance": 3510.63,
        "admin_other": 0.0
    }

    auditor = T12Auditor()
    t12_res = auditor.audit_and_normalize(
        raw_t12,
        purchase_price=500000.0,
        tax_reassessment_rate=0.015,
        unit_count=canonical_unit_count,
        landlord_water_annual=2400.0,
        landlord_common_electric_annual=600.0
    )
    normalized_noi = t12_res["normalized_noi"] # $44,825.27

    # 3. Comp Eligibility Funnel, Similarity Scoring & Dispersion
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
        {"address": "Comp 4: 12 SFH Distress (1-unit)", "property_type": "single_family", "unit_count": 1, "sale_price": 220000, "building_sf": 1800, "days_since_sale": 15, "distance_miles": 0.2}
    ]
    comp_res = comp_engine.calculate_sales_comp_fmv(subject, raw_comps)
    sales_comp_fmv = comp_res["sales_comp_fmv"]

    # 4. Mandatory Stress Testing Engine
    tester = StressTester()
    stress_res = tester.run_stress_test(
        gpr=73908.0,
        current_tax=2676.38,
        reassessed_tax=t12_res["expenses"]["reassessed_tax"],
        current_insurance=4215.0,
        updated_insurance=4215.0,
        utilities=3630.0,
        pm_fee=t12_res["expenses"]["normalized_mgmt"],
        maintenance=3510.63,
        purchase_price=500000.0,
        down_payment_pct=20.0,
        interest_rate_pct=7.0,
        loan_years=20
    )

    # 5. Multi-Constraint Offer Price Optimization
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
        loan_years=20,
        arv=sales_comp_fmv,
        rehab_costs=0.0
    )

    # 6. Offer Data Provenance & Confidence Evaluation
    evaluator = OfferConfidenceEvaluator()
    conf_res = evaluator.evaluate_offer_confidence(
        comps_count=len(comp_res["evaluated_comps"]),
        primary_comps_count=comp_res["primary_comps_count"],
        fallback_comps_count=comp_res["fallback_comps_count"],
        old_comps_count=0,
        has_t12=True,
        has_lease_agreements=True,
        has_tax_bills=True,
        valuation_dispersion_cv=comp_res["valuation_dispersion_cv"]
    )

    # Print Summary
    print(f"Property: 273-275 New Hancock Street, Wilkes-Barre PA")
    print(f"Offer Confidence: {conf_res['confidence_level']} ({conf_res['offer_confidence_score']}/100)")
    print(f"Valuation Dispersion (CV): {comp_res['valuation_dispersion_cv']} | Low Comp Warning: {comp_res['safeguard_warning']}")
    print(f"Normalized NOI: ${normalized_noi:,.2f} (Seller NOI was ${t12_res['seller_noi']:,.2f})")
    print("-" * 75)
    print("THREE DISTINCT VALUES:")
    print(f"  1. Sales Comp FMV:         ${offer_res['three_values']['sales_comp_fmv']:,.2f}")
    print(f"  2. Income Approach Value:  ${offer_res['three_values']['income_approach_value']:,.2f}")
    print(f"  3. Investor Max Value:     ${offer_res['three_values']['investor_max_value']:,.2f}")
    print("-" * 75)
    print("STRATEGY-SPECIFIC MAXIMUM ALLOWABLE OFFERS (MAO):")
    smaos = offer_res["strategy_maos"]
    print(f"  • Buy & Hold MAO:          ${smaos['mao_buy_hold']:,.2f}")
    print(f"  • BRRRR MAO (Refi):        ${smaos['mao_brrrr']:,.2f}")
    print(f"  • Fix & Flip MAO:          ${smaos['mao_flip']:,.2f}")
    print("-" * 75)
    print("FOUR OFFER PRICES + WALK-AWAY PRICE:")
    bands = offer_res["offer_price_bands"]
    print(f"  • Opening Offer:           ${bands['opening_offer']:,.2f}")
    print(f"  • Recommended Offer:       ${bands['recommended_offer']:,.2f}")
    print(f"  • Max Rational Offer:      ${bands['maximum_rational_offer']:,.2f}")
    print(f"  • WALK-AWAY PRICE:         ${bands['walk_away_price']:,.2f}  [Hard Threshold]")
    print(f"  • Market Value Ceiling:    ${bands['market_value_ceiling']:,.2f}")
    print("-" * 75)
    print("UNDERWRITING STRESS TEST:")
    print(f"  • Base Cash Flow:          ${stress_res['base_scenario']['monthly_cash_flow']:,.2f}/mo (DSCR: {stress_res['base_scenario']['dscr']})")
    print(f"  • Post-Acquisition Flow:   ${stress_res['post_acquisition_scenario']['monthly_cash_flow']:,.2f}/mo (DSCR: {stress_res['post_acquisition_scenario']['dscr']})")
    print(f"  • Stress Scenario Flow:     ${stress_res['stress_scenario']['monthly_cash_flow']:,.2f}/mo (DSCR: {stress_res['stress_scenario']['dscr']})")
    print("=" * 75)

if __name__ == "__main__":
    run_underwriting()
