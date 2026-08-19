#!/usr/bin/env python3
"""
Multi-Constraint Offer Price Optimizer & Three-Value Valuation Engine

Calculates:
1. Three Distinct Values (Sales Comp FMV, Income Approach Value, Investor Value)
2. Constraint-Based Offer Optimization (Cap Rate >= Target, CoC >= Target, DSCR >= 1.25, Cash Flow >= Min)
3. 4-Tier Offer Price Bands (Aggressive, Recommended, Max Rational, Market Ceiling)
"""

from typing import Dict, Any, Tuple
from score_property import calculate_mortgage_payment, calculate_cash_on_cash

class OfferOptimizer:
    def calculate_income_value(self, noi: float, market_cap_rate_pct: float = 8.5) -> float:
        """Calculates Income Approach Value = NOI / Market Cap Rate."""
        if market_cap_rate_pct <= 0:
            return 0.0
        return round(noi / (market_cap_rate_pct / 100.0), 2)

    def calculate_dscr(self, noi: float, annual_debt_service: float) -> float:
        """Calculates Debt Service Coverage Ratio (DSCR) = NOI / Annual Debt Service."""
        if annual_debt_service <= 0:
            return 999.0 # Fully paid off / cash deal
        return round(noi / annual_debt_service, 2)

    def optimize_offer_price(
        self,
        normalized_noi: float,
        sales_comp_fmv: float,
        market_cap_rate_pct: float = 8.5,
        target_cap_rate_pct: float = 10.0,
        target_coc_pct: float = 12.0,
        min_dscr: float = 1.25,
        min_monthly_cash_flow: float = 500.0,
        down_payment_pct: float = 20.0,
        interest_rate_pct: float = 7.0,
        loan_years: int = 20
    ) -> Dict[str, Any]:
        """
        Solves for maximum purchase price meeting ALL investment constraints.
        Outputs Three-Value Model & 4-Tier Offer Price Bands.
        """
        income_val = self.calculate_income_value(normalized_noi, market_cap_rate_pct)

        # 1. Cap Rate Ceiling MAO
        mao_cap_rate = normalized_noi / (target_cap_rate_pct / 100.0) if target_cap_rate_pct > 0 else income_val

        # Iterative solver for CoC, DSCR, and Cash Flow constraints
        # Step down from sales_comp_fmv to find maximum compliant price
        step_price = min(sales_comp_fmv, income_val * 1.25)
        if step_price <= 0:
            step_price = 500000.0

        max_rational_price = step_price
        while max_rational_price > 50000.0:
            down_payment = max_rational_price * (down_payment_pct / 100.0)
            loan_amount = max_rational_price - down_payment
            monthly_m = calculate_mortgage_payment(loan_amount, interest_rate_pct, loan_years)
            ann_debt = monthly_m * 12.0
            
            dscr = self.calculate_dscr(normalized_noi, ann_debt)
            ann_cash_flow = normalized_noi - ann_debt
            monthly_cash_flow = ann_cash_flow / 12.0
            total_initial_cash = down_payment + (max_rational_price * 0.01) # 1% closing costs
            coc = calculate_cash_on_cash(ann_cash_flow, total_initial_cash)
            cap_rate = (normalized_noi / max_rational_price) * 100.0

            # Check constraints
            if (
                dscr >= min_dscr and
                monthly_cash_flow >= min_monthly_cash_flow and
                coc >= target_coc_pct and
                cap_rate >= target_cap_rate_pct
            ):
                break # Found maximum price satisfying all constraints!

            max_rational_price -= 2500.0

        max_rational_offer = round(max(max_rational_price, 50000.0), 2)
        recommended_offer = round(max_rational_offer * 0.95, 2) # 5% below ceiling for negotiation room
        aggressive_offer = round(max_rational_offer * 0.90, 2)  # 10% below ceiling (best case)
        market_ceiling = round(max(sales_comp_fmv, income_val), 2)

        # Underwriting metrics at Recommended Offer
        rec_down = recommended_offer * (down_payment_pct / 100.0)
        rec_loan = recommended_offer - rec_down
        rec_monthly_m = calculate_mortgage_payment(rec_loan, interest_rate_pct, loan_years)
        rec_ann_debt = rec_monthly_m * 12.0
        rec_cash_flow = normalized_noi - rec_ann_debt
        rec_dscr = self.calculate_dscr(normalized_noi, rec_ann_debt)
        rec_coc = calculate_cash_on_cash(rec_cash_flow, rec_down + (recommended_offer * 0.01))
        rec_cap = (normalized_noi / recommended_offer) * 100.0 if recommended_offer > 0 else 0.0

        return {
            "three_values": {
                "sales_comp_fmv": sales_comp_fmv,
                "income_approach_value": income_val,
                "investor_max_value": max_rational_offer
            },
            "offer_price_bands": {
                "aggressive_offer": aggressive_offer,
                "recommended_offer": recommended_offer,
                "maximum_rational_offer": max_rational_offer,
                "market_value_ceiling": market_ceiling
            },
            "recommended_offer_underwriting": {
                "offer_price": recommended_offer,
                "down_payment": round(rec_down, 2),
                "loan_amount": round(rec_loan, 2),
                "monthly_mortgage": rec_monthly_m,
                "annual_debt_service": round(rec_ann_debt, 2),
                "annual_net_cash_flow": round(rec_cash_flow, 2),
                "monthly_net_cash_flow": round(rec_cash_flow / 12.0, 2),
                "cap_rate_pct": round(rec_cap, 2),
                "dscr": rec_dscr,
                "coc_return_pct": rec_coc
            }
        }

if __name__ == "__main__":
    optimizer = OfferOptimizer()
    res = optimizer.optimize_offer_price(
        normalized_noi=53825.27,
        sales_comp_fmv=540000.0,
        market_cap_rate_pct=8.5,
        target_cap_rate_pct=10.0,
        target_coc_pct=12.0,
        min_dscr=1.25,
        min_monthly_cash_flow=500.0,
        down_payment_pct=20.0,
        interest_rate_pct=7.0,
        loan_years=20
    )
    print("Offer Optimizer Test:")
    import json
    print(json.dumps(res, indent=2))
