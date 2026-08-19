#!/usr/bin/env python3
"""
Property Scoring & Financial Underwriting Engine

Calculates composite Property Score (0-100), letter grade (A+ to F), 
investment recommendations, and financial underwriting metrics (NOI, Cap Rate, CoC, MAO).
"""

from typing import Dict, Any, Tuple

WEIGHTS = {
    "value_comps": 0.25,
    "income_potential": 0.20,
    "neighborhood_quality": 0.20,
    "investment_upside": 0.20,
    "market_conditions": 0.15
}

def calculate_noi(effective_gross_income: float, operating_expenses: float) -> float:
    """Calculate Net Operating Income (NOI)."""
    return round(effective_gross_income - operating_expenses, 2)

def calculate_cap_rate(noi: float, purchase_price: float) -> float:
    """Calculate Capitalization Rate (Cap Rate) as percentage."""
    if purchase_price <= 0:
        return 0.0
    return round((noi / purchase_price) * 100, 2)

def calculate_cash_on_cash(annual_cash_flow: float, total_cash_invested: float) -> float:
    """Calculate Cash-on-Cash (CoC) return percentage."""
    if total_cash_invested <= 0:
        return 0.0
    return round((annual_cash_flow / total_cash_invested) * 100, 2)

def calculate_mao(noi: float, target_cap_rate: float, capex_rehab: float = 0.0, desired_profit: float = 0.0) -> float:
    """
    Calculate Maximum Allowable Offer (MAO).
    target_cap_rate is passed as percentage e.g. 6.5 for 6.5%.
    """
    if target_cap_rate <= 0:
        return 0.0
    valuation = noi / (target_cap_rate / 100.0)
    mao = valuation - capex_rehab - desired_profit
    return round(max(mao, 0.0), 2)

def calculate_mortgage_payment(loan_amount: float, interest_rate_pct: float = 7.0, loan_years: int = 20) -> float:
    """Calculates monthly mortgage payment (P&I)."""
    if loan_amount <= 0 or interest_rate_pct <= 0 or loan_years <= 0:
        return 0.0
    monthly_rate = (interest_rate_pct / 100.0) / 12.0
    total_months = loan_years * 12
    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** total_months) / ((1 + monthly_rate) ** total_months - 1)
    return round(monthly_payment, 2)

def generate_cap_rate_offer_matrix(
    noi: float,
    start_cap: float = 8.0,
    end_cap: float = 12.0,
    step: float = 0.5,
    down_payment_pct: float = 20.0,
    interest_rate_pct: float = 7.0,
    loan_years: int = 20
) -> Dict[str, Dict[str, float]]:
    """Generates detailed offer price matrix with debt service and levered cash flow."""
    matrix = {}
    current_cap = start_cap
    while current_cap <= end_cap + 0.001:
        offer_price = calculate_mao(noi, current_cap)
        down_payment = offer_price * (down_payment_pct / 100.0)
        loan_amount = offer_price - down_payment
        monthly_mortgage = calculate_mortgage_payment(loan_amount, interest_rate_pct, loan_years)
        annual_debt_service = monthly_mortgage * 12.0
        annual_cash_flow = noi - annual_debt_service
        total_initial_cash = down_payment + (offer_price * 0.01) # 1% closing costs
        coc_return = calculate_cash_on_cash(annual_cash_flow, total_initial_cash)
        
        matrix[f"{current_cap:.1f}%"] = {
            "offer_price": offer_price,
            "down_payment": round(down_payment, 2),
            "loan_amount": round(loan_amount, 2),
            "monthly_mortgage": monthly_mortgage,
            "annual_debt_service": round(annual_debt_service, 2),
            "annual_cash_flow": round(annual_cash_flow, 2),
            "coc_return_pct": coc_return
        }
        current_cap += step
    return matrix

def get_grade_and_signal(score: float) -> Tuple[str, str]:
    """Return Letter Grade and Investment Signal based on 0-100 score."""
    score = round(score, 1)
    if score >= 85:
        return "A+", "Strong Buy — excellent value across all dimensions"
    elif score >= 70:
        return "A", "Buy — favorable fundamentals with manageable risks"
    elif score >= 55:
        return "B", "Hold/Watch — mixed signals, deeper due diligence needed"
    elif score >= 40:
        return "C", "Caution — significant concerns in one or more areas"
    elif score >= 25:
        return "D", "Pass — unfavorable risk/reward at current pricing"
    else:
        return "F", "Avoid — major red flags, walk away"

def compute_property_score(
    value_score: float,
    income_score: float,
    neighborhood_score: float,
    upside_score: float,
    market_score: float
) -> Dict[str, Any]:
    """
    Computes weighted Property Score (0-100).
    Enforces score bounds [0, 100].
    """
    # Clamp individual category scores between 0 and 100
    v = max(0.0, min(100.0, float(value_score)))
    inc = max(0.0, min(100.0, float(income_score)))
    n = max(0.0, min(100.0, float(neighborhood_score)))
    u = max(0.0, min(100.0, float(upside_score)))
    m = max(0.0, min(100.0, float(market_score)))

    composite_score = round(
        (v * WEIGHTS["value_comps"]) +
        (inc * WEIGHTS["income_potential"]) +
        (n * WEIGHTS["neighborhood_quality"]) +
        (u * WEIGHTS["investment_upside"]) +
        (m * WEIGHTS["market_conditions"]),
        1
    )

    grade, signal = get_grade_and_signal(composite_score)

    return {
        "composite_score": composite_score,
        "grade": grade,
        "signal": signal,
        "breakdown": {
            "value_comps": v,
            "income_potential": inc,
            "neighborhood_quality": n,
            "investment_upside": u,
            "market_conditions": m
        }
    }

if __name__ == "__main__":
    sample_result = compute_property_score(80, 75, 90, 70, 85)
    print("Sample Property Score Calculation:")
    print(f"Score: {sample_result['composite_score']} | Grade: {sample_result['grade']}")
    print(f"Signal: {sample_result['signal']}")
