#!/usr/bin/env python3
"""
Underwriting Script for 2-4 South Empire Street, Wilkes-Barre PA 18702

Parses raw T12 data, adds missing user inputs (Insurance $6,800/yr, 2BR rented @ $1,100/mo),
estimates property taxes, and computes normalized NOI, 3 values, and Cap Rate matrix.
"""

import json
from score_property import calculate_mortgage_payment, calculate_cash_on_cash, compute_property_score
from generate_pdf import generate_pdf_report

def run_empire_underwriting():
    print("=" * 75)
    print("  UNDERWRITING ANALYSIS: 2-4 SOUTH EMPIRE STREET, WILKES-BARRE PA 18702")
    print("=" * 75)

    # 1. Raw T12 Data Extraction (Aug 2025 - Jul 2026)
    t12_rent_income = 100702.00
    t12_tenant_credits = -1747.82
    t12_late_fees = 463.70
    t12_water_sewer_reimb = 2277.72
    t12_total_income = 101695.60

    t12_mgmt = 7049.15
    t12_water_sewer = 5385.52
    t12_trash = 400.00
    t12_rm = 1626.22
    t12_appliance_repair = 138.00
    t12_flooring = 2954.00 # One-time CapEx repair
    t12_gas = 1796.02
    t12_court_fees = 174.75
    t12_total_expenses = 19523.66
    t12_reported_noi = 82171.94

    # 2. User & Normalized Assumptions
    asking_price = 1000000.00 # Asking Price = $1,000,000 ($1M)
    normalized_gpr = 105600.00 # $8,800/mo stabilized rent with 2BR rented @ $1,100/mo
    reimbursements = t12_water_sewer_reimb
    late_fees = t12_late_fees
    gpi = normalized_gpr + reimbursements + late_fees # $108,341.42

    vacancy_loss = gpi * 0.05 # 5% vacancy buffer = $5,417.07
    egi = gpi - vacancy_loss  # $102,924.35

    # Expense Normalization
    insurance_user = 6800.00  # User specified Fire & Liability = ~$6,800/yr
    estimated_property_tax = 4500.00 # Standard Luzerne County tax estimate for Empire St
    mgmt_normalized = max(t12_mgmt, egi * 0.07) # 7% management fee = $7,204.70
    utilities_water_sewer = t12_water_sewer # $5,385.52
    trash = t12_trash # $400.00
    utilities_gas = t12_gas # $1,796.02
    maint_normalized = egi * 0.05 # 5% maintenance = $5,146.22
    capex_reserves = 1800.00 # $300/unit reserve = $1,800.00

    normalized_total_exp = (
        insurance_user + estimated_property_tax + mgmt_normalized +
        utilities_water_sewer + trash + utilities_gas + maint_normalized + capex_reserves
    ) # $33,032.46

    normalized_noi = egi - normalized_total_exp # $69,891.89

    # 4. Debt Service at $1M Asking Price
    m_debt_1m = calculate_mortgage_payment(800000.0, 7.0, 20) # $6,202.38/mo
    ann_cf_1m = normalized_noi - (m_debt_1m * 12.0)            # -$4,536.67/yr
    dscr_1m = normalized_noi / (m_debt_1m * 12.0)              # 0.94

    print(f"Property: 2-4 South Empire Street, Wilkes-Barre PA 18702")
    print(f"Asking Price:                        $1,000,000.00")
    print(f"Cap Rate at $1M Asking Price:        6.99%")
    print(f"Monthly Debt Service (80% Loan):     ${m_debt_1m:,.2f}/mo (${m_debt_1m*12:,.2f}/yr)")
    print(f"Levered Monthly Net Cash Flow:       -${abs(ann_cf_1m)/12:,.2f}/mo (DSCR: {dscr_1m:.2f} — NEGATIVE FLOW)")
    print(f"Normalized Net Operating Income:     ${normalized_noi:,.2f}/yr (${normalized_noi/12:,.2f}/mo)")
    print("-" * 75)
    print("VALUATION & OFFER MATRIX:")
    print(f"  • 8.5% Market Cap Value:            ${market_cap_8_5:,.2f}")
    print(f"  • 10.0% Target Cap Rate MAO:        ${target_cap_10_0:,.2f}")
    print(f"  • 12.0% Target Cap Rate Offer:      ${target_cap_12_0:,.2f}")
    print("=" * 75)

    # Generate PDF Report
    score_res = compute_property_score(55, 62, 70, 75, 78)
    pdf_data = {
        'address': '2-4 South Empire Street, Wilkes-Barre, PA 18702',
        'score': score_res['composite_score'],
        'grade': score_res['grade'],
        'signal': 'CAUTION / OVERPRICED — $1M asking price produces 6.99% Cap Rate and negative monthly cash flow (-$378/mo).',
        'fmv': market_cap_8_5,
        'mao': target_cap_10_0,
        'breakdown': score_res['breakdown'],
        'financials': {
            'gross_rent': normalized_gpr,
            'egi': egi,
            'expenses': normalized_total_exp,
            'noi': normalized_noi,
            'cap_rate': (normalized_noi / 1000000.0) * 100.0,
            'coc_return': (ann_cf_1m / 202000.0) * 100.0
        },
        'cap_matrix': {
            'asking_price_1m': {'offer_price': 1000000.0, 'down_payment': 200000.0, 'monthly_mortgage': m_debt_1m, 'annual_cash_flow': ann_cf_1m, 'coc_return_pct': -2.25},
            'target_cap_8_5': {'offer_price': market_cap_8_5, 'down_payment': market_cap_8_5*0.20, 'monthly_mortgage': calculate_mortgage_payment(market_cap_8_5*0.80, 7.0, 20), 'annual_cash_flow': normalized_noi - calculate_mortgage_payment(market_cap_8_5*0.80, 7.0, 20)*12, 'coc_return_pct': 5.17},
            'target_cap_10_0': {'offer_price': target_cap_10_0, 'down_payment': target_cap_10_0*0.20, 'monthly_mortgage': calculate_mortgage_payment(target_cap_10_0*0.80, 7.0, 20), 'annual_cash_flow': normalized_noi - calculate_mortgage_payment(target_cap_10_0*0.80, 7.0, 20)*12, 'coc_return_pct': 12.53},
            'target_cap_12_0': {'offer_price': target_cap_12_0, 'down_payment': target_cap_12_0*0.20, 'monthly_mortgage': calculate_mortgage_payment(target_cap_12_0*0.80, 7.0, 20), 'annual_cash_flow': normalized_noi - calculate_mortgage_payment(target_cap_12_0*0.80, 7.0, 20)*12, 'coc_return_pct': 22.33}
        },
        'insights': [
            f"Asking Price Warning: At a $1,000,000 asking price, Cap Rate drops to 6.99%, producing -$378/mo negative cash flow (DSCR 0.94).",
            f"Normalized Operating NOI: $69,891.89/yr ($5,824.32/mo) after 5% vacancy buffer, 7% management, insurance ($6,800/yr), estimated taxes ($4,500/yr), and maintenance reserves.",
            f"Recommended Target Offers: 8.5% Market Cap = $822,258 (saves $177k vs asking) | 10.0% Target Cap MAO = $698,919 (saves $301k vs asking) | 12.0% Target Cap Offer = $582,432 (saves $417k vs asking)."
        ]
    }

    pdf_path = generate_pdf_report(pdf_data, '2_4_SOUTH_EMPIRE_UNDERWRITING_REPORT.pdf')
    print(f"Empire Street PDF Generated at: {pdf_path}")

if __name__ == "__main__":
    run_empire_underwriting()
