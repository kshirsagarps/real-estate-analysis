#!/usr/bin/env python3
"""
Mandatory Underwriting Stress Testing Engine

Evaluates 3 mandatory underwriting scenarios:
1. Base Scenario (Current tax, current insurance, normalized rent/vacancy)
2. Post-Acquisition Scenario (Reassessed tax, updated insurance quote)
3. Stress Scenario (Taxes +25%, Insurance +20%, Maintenance +15%, Rent -5%, Vacancy +5%)
"""

from typing import Dict, Any
from score_property import calculate_mortgage_payment, calculate_cash_on_cash

class StressTester:
    def run_stress_test(
        self,
        gpr: float,
        current_tax: float,
        reassessed_tax: float,
        current_insurance: float,
        updated_insurance: float,
        utilities: float,
        pm_fee: float,
        maintenance: float,
        purchase_price: float,
        down_payment_pct: float = 20.0,
        interest_rate_pct: float = 7.0,
        loan_years: int = 20
    ) -> Dict[str, Any]:
        """
        Runs 3 mandatory underwriting scenarios and checks for cash flow/DSCR failures.
        """
        loan_amount = purchase_price * (1.0 - (down_payment_pct / 100.0))
        monthly_m = calculate_mortgage_payment(loan_amount, interest_rate_pct, loan_years)
        ann_debt = monthly_m * 12.0

        # Scenario 1: Base Scenario
        base_egi = gpr * 0.95
        base_exp = current_tax + current_insurance + utilities + pm_fee + maintenance
        base_noi = base_egi - base_exp
        base_cash_flow = base_noi - ann_debt
        base_dscr = base_noi / ann_debt if ann_debt > 0 else 999.0

        # Scenario 2: Post-Acquisition Scenario
        post_egi = gpr * 0.95
        post_exp = reassessed_tax + updated_insurance + utilities + pm_fee + maintenance
        post_noi = post_egi - post_exp
        post_cash_flow = post_noi - ann_debt
        post_dscr = post_noi / ann_debt if ann_debt > 0 else 999.0

        # Scenario 3: Stress Scenario (Rent -5%, Vacancy 10%, Taxes +25%, Insurance +20%, Maintenance +15%)
        stress_egi = (gpr * 0.95) * 0.90 # Rent drop & vacancy bump
        stress_exp = (
            (reassessed_tax * 1.25) +
            (updated_insurance * 1.20) +
            (utilities * 1.10) +
            pm_fee +
            (maintenance * 1.15)
        )
        stress_noi = stress_egi - stress_exp
        stress_cash_flow = stress_noi - ann_debt
        stress_dscr = stress_noi / ann_debt if ann_debt > 0 else 999.0

        # Flags & Alerts
        stress_failed = stress_cash_flow < 0 or stress_dscr < 1.0
        warning = "CRITICAL: Deal fails downside stress scenario (negative cash flow under stress)!" if stress_failed else "Passes stress scenario."

        return {
            "base_scenario": {
                "noi": round(base_noi, 2),
                "annual_cash_flow": round(base_cash_flow, 2),
                "monthly_cash_flow": round(base_cash_flow / 12.0, 2),
                "dscr": round(base_dscr, 2),
                "cap_rate_pct": round((base_noi / purchase_price) * 100.0, 2)
            },
            "post_acquisition_scenario": {
                "noi": round(post_noi, 2),
                "annual_cash_flow": round(post_cash_flow, 2),
                "monthly_cash_flow": round(post_cash_flow / 12.0, 2),
                "dscr": round(post_dscr, 2),
                "cap_rate_pct": round((post_noi / purchase_price) * 100.0, 2)
            },
            "stress_scenario": {
                "noi": round(stress_noi, 2),
                "annual_cash_flow": round(stress_cash_flow, 2),
                "monthly_cash_flow": round(stress_cash_flow / 12.0, 2),
                "dscr": round(stress_dscr, 2),
                "cap_rate_pct": round((stress_noi / purchase_price) * 100.0, 2),
                "stress_failed": stress_failed,
                "warning": warning
            }
        }

if __name__ == "__main__":
    tester = StressTester()
    res = tester.run_stress_test(
        gpr=73908.0, current_tax=2676.38, reassessed_tax=7500.0,
        current_insurance=4215.0, updated_insurance=4215.0,
        utilities=4230.0, pm_fee=1755.32, maintenance=3510.63,
        purchase_price=500000.0
    )
    print("Stress Tester Test:")
    import json
    print(json.dumps(res, indent=2))
