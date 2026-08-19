#!/usr/bin/env python3
"""
T12 Audit & Normalization Engine

Performs anomaly detection on T12 operating statements, calculates 
Seller NOI vs Normalized NOI vs Conservative NOI, models post-purchase tax reassessment,
and normalizes landlord-paid vs tenant-paid utilities.
"""

from typing import Dict, Any, List

class T12Auditor:
    def audit_and_normalize(
        self,
        seller_t12_data: Dict[str, Any],
        purchase_price: float,
        tax_reassessment_rate: float = 0.015, # 1.5% estimated post-sale tax rate
        min_vacancy_pct: float = 5.0,
        capex_reserve_per_unit: float = 300.0, # $300/unit/yr CapEx reserve
        unit_count: int = 5,
        landlord_water_annual: float = 0.0,
        landlord_common_electric_annual: float = 0.0
    ) -> Dict[str, Any]:
        """
        Audits raw seller T12 and outputs Seller NOI, Normalized NOI, and Conservative NOI.
        """
        anomalies = []

        gpr = float(seller_t12_data.get("gross_potential_rent", 0.0))
        seller_vacancy = abs(float(seller_t12_data.get("vacancy_loss", 0.0)))
        seller_other_income = float(seller_t12_data.get("other_income", 0.0))

        # Check Vacancy Anomaly
        seller_vacancy_pct = (seller_vacancy / gpr * 100.0) if gpr > 0 else 0.0
        normalized_vacancy_pct = max(seller_vacancy_pct, min_vacancy_pct)
        if seller_vacancy_pct < min_vacancy_pct:
            anomalies.append(f"Seller reported vacancy ({seller_vacancy_pct:.1f}%) is below market standard ({min_vacancy_pct:.1f}%). Adjusted upward.")

        normalized_vacancy_loss = gpr * (normalized_vacancy_pct / 100.0)
        normalized_egi = gpr - normalized_vacancy_loss + seller_other_income
        seller_egi = gpr - seller_vacancy + seller_other_income

        # Seller Expenses
        seller_taxes = float(seller_t12_data.get("property_taxes", 0.0))
        seller_insurance = float(seller_t12_data.get("insurance", 0.0))
        seller_utilities = float(seller_t12_data.get("utilities", 0.0)) + landlord_water_annual + landlord_common_electric_annual
        seller_mgmt = float(seller_t12_data.get("management_fees", 0.0))
        seller_maint = float(seller_t12_data.get("repairs_maintenance", 0.0))
        seller_admin = float(seller_t12_data.get("admin_other", 0.0))
        seller_capex = float(seller_t12_data.get("capex_reserves", 0.0))

        seller_total_exp = (
            seller_taxes + seller_insurance + seller_utilities +
            seller_mgmt + seller_maint + seller_admin + seller_capex
        )
        seller_noi = seller_egi - seller_total_exp

        # Normalized Tax Reassessment Audit
        reassessed_tax = max(seller_taxes, purchase_price * tax_reassessment_rate)
        if reassessed_tax > seller_taxes:
            anomalies.append(f"Post-sale property tax reassessment estimated to increase taxes from ${seller_taxes:,.2f} to ${reassessed_tax:,.2f}/yr.")

        # Property Management Normalization (at least 5% or actual)
        normalized_mgmt = max(seller_mgmt, normalized_egi * 0.05)
        if normalized_mgmt > seller_mgmt:
            anomalies.append("Normalized property management fees to market minimum (5% of EGI).")

        # CapEx Reserve Normalization
        required_capex = unit_count * capex_reserve_per_unit
        normalized_capex = max(seller_capex, required_capex)
        if normalized_capex > seller_capex:
            anomalies.append(f"Seller omitted CapEx reserves. Normalized to ${required_capex:,.2f}/yr (${capex_reserve_per_unit:.0f}/unit).")

        # Normalized Expenses
        normalized_total_exp = (
            reassessed_tax + seller_insurance + seller_utilities +
            normalized_mgmt + seller_maint + seller_admin + normalized_capex
        )
        normalized_noi = normalized_egi - normalized_total_exp

        # Conservative Scenario (+10% maintenance & +15% insurance buffer)
        conservative_exp = (
            (reassessed_tax * 1.05) +
            (seller_insurance * 1.15) +
            (seller_utilities * 1.05) +
            normalized_mgmt +
            (seller_maint * 1.10) +
            seller_admin +
            (normalized_capex * 1.20)
        )
        conservative_noi = normalized_egi - conservative_exp

        return {
            "seller_noi": round(seller_noi, 2),
            "normalized_noi": round(normalized_noi, 2),
            "conservative_noi": round(conservative_noi, 2),
            "gpr": round(gpr, 2),
            "normalized_egi": round(normalized_egi, 2),
            "expenses": {
                "seller_total_expenses": round(seller_total_exp, 2),
                "normalized_total_expenses": round(normalized_total_exp, 2),
                "conservative_total_expenses": round(conservative_exp, 2),
                "reassessed_tax": round(reassessed_tax, 2),
                "normalized_mgmt": round(normalized_mgmt, 2),
                "normalized_capex": round(normalized_capex, 2)
            },
            "anomalies_detected": anomalies
        }

if __name__ == "__main__":
    auditor = T12Auditor()
    sample_raw = {
        "gross_potential_rent": 73908.0,
        "vacancy_loss": 0.0, # Seller reported 0 vacancy!
        "other_income": 0.0,
        "property_taxes": 2676.38,
        "insurance": 4215.00,
        "utilities": 1230.0,
        "management_fees": 0.0, # Seller self-managed!
        "repairs_maintenance": 3500.0,
        "admin_other": 0.0
    }
    res = auditor.audit_and_normalize(sample_raw, purchase_price=500000.0, unit_count=5, landlord_water_annual=2400.0, landlord_common_electric_annual=600.0)
    print("T12 Audit & Normalization Test:")
    import json
    print(json.dumps(res, indent=2))
