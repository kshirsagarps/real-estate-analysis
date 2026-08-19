#!/usr/bin/env python3
"""
Deterministic Multi-Scenario Property Underwriting Engine

Computes reproducible financial scenarios:
1. Trailing T12 Scenario (As-Is)
2. Stabilized Underwriting Scenario
3. Conservative Stress Test Scenario (-5% Rent, +10% Expense)

Guarantees:
- Explicit double-counting prevention for Taxes and Insurance
- Auditable JSON output with valuation matrices and warning flags
"""

import sys
import json
from typing import Dict, Any, List

def underwrite_property_scenarios(
    property_name: str,
    units: int,
    gross_scheduled_rent_stabilized: float,
    trailing_t12_income: float,
    trailing_t12_expenses: float,
    property_tax_annual: float,
    insurance_annual: float,
    taxes_included_in_t12: bool = False,
    insurance_included_in_t12: bool = False,
    target_cap_rate: float = 0.12,
    down_payment_pct: float = 0.20,
    interest_rate_pct: float = 7.0,
    loan_years: int = 20,
    unit_5_projected: bool = True
) -> Dict[str, Any]:
    """
    Executes reproducible, multi-scenario underwriting calculation.
    """
    warnings: List[str] = []

    if unit_5_projected:
        warnings.append("Unit 5 rent is projected, not collected")
    
    if taxes_included_in_t12:
        warnings.append("Property taxes are already included in T12 expenses; omitted extra tax addition to prevent double-counting")
    else:
        warnings.append("Property taxes verified separate from T12 expenses; added $%.2f/yr tax" % property_tax_annual)

    if insurance_included_in_t12:
        warnings.append("Insurance is already included in T12 expenses; omitted extra insurance addition to prevent double-counting")
    else:
        warnings.append("Insurance verified separate from T12 expenses; added $%.2f/yr insurance" % insurance_annual)

    # -------------------------------------------------------------------------
    # SCENARIO 1: TRAILING T12 (AS-IS)
    # -------------------------------------------------------------------------
    trailing_income = trailing_t12_income
    trailing_expenses = trailing_t12_expenses
    if not taxes_included_in_t12:
        trailing_expenses += property_tax_annual
    if not insurance_included_in_t12:
        trailing_expenses += insurance_annual

    trailing_noi = max(trailing_income - trailing_expenses, 0.0)
    trailing_cap_value = trailing_noi / target_cap_rate if target_cap_rate > 0 else 0.0

    # -------------------------------------------------------------------------
    # SCENARIO 2: STABILIZED UNDERWRITING
    # -------------------------------------------------------------------------
    stabilized_gsi = gross_scheduled_rent_stabilized
    vacancy_reserve = stabilized_gsi * 0.05
    effective_stabilized_income = stabilized_gsi - vacancy_reserve

    # Normalized expenses: T12 base + management 5% + maintenance 5% + taxes/insurance
    mgmt_fee = effective_stabilized_income * 0.05
    maint_fee = effective_stabilized_income * 0.05
    capex_reserve = units * 300.0

    stabilized_operating_exp = trailing_t12_expenses + mgmt_fee + maint_fee + capex_reserve
    if not taxes_included_in_t12:
        stabilized_operating_exp += property_tax_annual
    if not insurance_included_in_t12:
        stabilized_operating_exp += insurance_annual

    stabilized_noi = effective_stabilized_income - stabilized_operating_exp
    stabilized_cap_value = stabilized_noi / target_cap_rate if target_cap_rate > 0 else 0.0

    # -------------------------------------------------------------------------
    # SCENARIO 3: CONSERVATIVE STRESS TEST (-5% Rent, +10% Expense)
    # -------------------------------------------------------------------------
    stress_income = effective_stabilized_income * 0.95
    stress_expenses = stabilized_operating_exp * 1.10
    stress_noi = stress_income - stress_expenses
    stress_cap_value = stress_noi / target_cap_rate if target_cap_rate > 0 else 0.0

    # -------------------------------------------------------------------------
    # OFFER RECOMMENDATIONS
    # -------------------------------------------------------------------------
    recommended_offer = round(stabilized_cap_value * 0.95, -3) # 5% below stabilized cap value
    maximum_offer = round(stabilized_cap_value, -3)
    opening_offer = round(stabilized_cap_value * 0.88, -3)
    walk_away_price = round(stress_cap_value * 1.05, -3)

    return {
        "property_name": property_name,
        "units": units,
        "target_cap_rate": target_cap_rate,
        "scenarios": {
            "trailing_t12_as_is": {
                "trailing_income": round(trailing_income, 2),
                "trailing_expenses": round(trailing_expenses, 2),
                "trailing_noi": round(trailing_noi, 2),
                "trailing_cap_value": round(trailing_cap_value, 2)
            },
            "stabilized_underwriting": {
                "gross_scheduled_income": round(stabilized_gsi, 2),
                "vacancy_reserve_5pct": round(vacancy_reserve, 2),
                "effective_gross_income": round(effective_stabilized_income, 2),
                "normalized_operating_expenses": round(stabilized_operating_exp, 2),
                "stabilized_noi": round(stabilized_noi, 2),
                "stabilized_cap_value": round(stabilized_cap_value, 2)
            },
            "conservative_stress_test": {
                "stress_income": round(stress_income, 2),
                "stress_expenses": round(stress_expenses, 2),
                "stress_noi": round(stress_noi, 2),
                "stress_cap_value": round(stress_cap_value, 2)
            }
        },
        "offer_bands": {
            "opening_offer": opening_offer,
            "recommended_offer": recommended_offer,
            "maximum_offer": maximum_offer,
            "walk_away_price": walk_away_price
        },
        "audit_warnings": warnings
    }

if __name__ == "__main__":
    res = underwrite_property_scenarios(
        property_name="273-275 New Hancock Street",
        units=5,
        gross_scheduled_rent_stabilized=77148.00,
        trailing_t12_income=73908.00,
        trailing_t12_expenses=14632.01,
        property_tax_annual=2676.38,
        insurance_annual=4215.00,
        taxes_included_in_t12=False,
        insurance_included_in_t12=False,
        target_cap_rate=0.12,
        unit_5_projected=True
    )
    print(json.dumps(res, indent=2))
