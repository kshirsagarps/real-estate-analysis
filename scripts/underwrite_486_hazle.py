#!/usr/bin/env python3
"""
Comprehensive Underwriting & PDF Generator for 486 Hazle Ave, Wilkes-Barre PA 18702
"""

import json
from score_property import calculate_mortgage_payment, calculate_cash_on_cash, compute_property_score
from generate_pdf import generate_pdf_report

def run_hazle_underwriting():
    print("=" * 75)
    print("  UNDERWRITING ANALYSIS: 486 HAZLE AVE, WILKES-BARRE PA 18702")
    print("=" * 75)

    address = "486 Hazle Ave, Wilkes-Barre, PA 18702"
    asking_price = 585000.00
    units = 5
    sf = 4950

    # Rent Roll: Unit 1 (2BR $1250), Unit 2 (2BR $1200), Unit 3 (2BR $1200), Unit 4 (1BR $1000), Unit 5 (1BR $975)
    gpr = 67500.00 # $5,625/mo
    reimbursements = 1800.00 # $150/mo utility reimbursements
    gpi = gpr + reimbursements # $69,300.00

    vacancy_loss = gpi * 0.05 # -$3,465.00
    egi = gpi - vacancy_loss  # $65,835.00

    prop_taxes = 3250.00
    insurance = 4500.00
    water_sewer = 3600.00
    gas_electric = 1450.00
    trash = 350.00
    mgmt_fee = egi * 0.07 # $4,608.45
    maint_fee = egi * 0.05 # $3,291.75
    capex_reserves = 1500.00 # $300/unit = $1,500

    total_expenses = prop_taxes + insurance + water_sewer + gas_electric + trash + mgmt_fee + maint_fee + capex_reserves # $22,550.20
    noi = egi - total_expenses # $43,284.80

    cap_at_585k = (noi / asking_price) * 100.0 # 7.40%
    m_debt_585k = calculate_mortgage_payment(asking_price * 0.80, 7.0, 20) # $3,628.40/mo
    ann_cf_585k = noi - (m_debt_585k * 12.0) # -$255.96/yr
    coc_585k = calculate_cash_on_cash(ann_cf_585k, asking_price * 0.20 * 1.01)

    target_cap_12_0 = noi / 0.120 # $360,706.67
    target_cap_10_0 = noi / 0.100 # $432,848.00
    target_cap_9_0 = noi / 0.090  # $480,942.22
    market_cap_8_5 = noi / 0.085  # $509,232.94

    print(f"Property: {address}")
    print(f"Purchase / Listing Price:            ${asking_price:,.2f}")
    print(f"Effective Gross Income (EGI):        ${egi:,.2f}")
    print(f"Total Operating Expenses:            ${total_expenses:,.2f} (34.3% Expense Ratio)")
    print(f"NET OPERATING INCOME (NOI):          ${noi:,.2f}/yr (${noi/12:,.2f}/mo)")
    print(f"Unlevered Cap Rate at $585k:          {cap_at_585k:.2f}%")
    print(f"Monthly Debt Service (80% Loan):     ${m_debt_585k:,.2f}/mo")
    print(f"Levered Monthly Cash Flow:           -${abs(ann_cf_585k)/12:,.2f}/mo (Near Breakeven)")
    print("-" * 75)
    print("TARGET VALUATIONS & OFFER MATRIX:")
    print(f"  • 8.5% Market Cap Value:            ${market_cap_8_5:,.2f}")
    print(f"  • 9.0% Target Cap Offer:            ${target_cap_9_0:,.2f}")
    print(f"  • 10.0% Target Cap Rate MAO:        ${target_cap_10_0:,.2f}")
    print(f"  • 12.0% Target Cap Offer:            ${target_cap_12_0:,.2f}")
    print("=" * 75)

    # PDF Data Generation
    score_res = compute_property_score(82, 85, 75, 80, 78)
    pdf_data = {
        'address': address,
        'score': score_res['composite_score'],
        'grade': score_res['grade'],
        'signal': 'BUY / TARGET COUNTER-OFFER — $585k asking price produces 7.40% Cap Rate. Target $432k-$509k offer for positive cash flow.',
        'fmv': market_cap_8_5,
        'mao': target_cap_10_0,
        'breakdown': score_res['breakdown'],
        'financials': {
            'gross_rent': gpr,
            'egi': egi,
            'expenses': total_expenses,
            'noi': noi,
            'cap_rate': cap_at_585k,
            'coc_return': coc_585k
        },
        'cap_matrix': {
            'target_cap_12_0': {'offer_price': target_cap_12_0, 'down_payment': target_cap_12_0*0.20, 'monthly_mortgage': calculate_mortgage_payment(target_cap_12_0*0.80, 7.0, 20), 'annual_cash_flow': noi - calculate_mortgage_payment(target_cap_12_0*0.80, 7.0, 20)*12, 'coc_return_pct': 22.8},
            'target_cap_10_0': {'offer_price': target_cap_10_0, 'down_payment': target_cap_10_0*0.20, 'monthly_mortgage': calculate_mortgage_payment(target_cap_10_0*0.80, 7.0, 20), 'annual_cash_flow': noi - calculate_mortgage_payment(target_cap_10_0*0.80, 7.0, 20)*12, 'coc_return_pct': 12.5},
            'target_cap_9_0': {'offer_price': target_cap_9_0, 'down_payment': target_cap_9_0*0.20, 'monthly_mortgage': calculate_mortgage_payment(target_cap_9_0*0.80, 7.0, 20), 'annual_cash_flow': noi - calculate_mortgage_payment(target_cap_9_0*0.80, 7.0, 20)*12, 'coc_return_pct': 7.7},
            'market_cap_8_5': {'offer_price': market_cap_8_5, 'down_payment': market_cap_8_5*0.20, 'monthly_mortgage': calculate_mortgage_payment(market_cap_8_5*0.80, 7.0, 20), 'annual_cash_flow': noi - calculate_mortgage_payment(market_cap_8_5*0.80, 7.0, 20)*12, 'coc_return_pct': 5.3},
            'asking_price_585k': {'offer_price': asking_price, 'down_payment': asking_price*0.20, 'monthly_mortgage': m_debt_585k, 'annual_cash_flow': ann_cf_585k, 'coc_return_pct': coc_585k}
        },
        'insights': [
            f"Property Specs: 5-Unit Multi-Family (4,950 SF) renovated in 1935 with 6 paved off-street parking spaces.",
            f"Income Roll: 3x 2-Bed units ($1,200-$1,250/mo) and 2x 1-Bed units ($975-$1,000/mo) generating $67,500/yr gross rent.",
            f"Normalized NOI: $43,284.80/yr ($3,607.07/mo) after 5% vacancy, $3,250 tax, $4,500 insurance, $3,600 water/sewer, and 7% PM.",
            f"Negotiation Playbook: At $585,000, property is at breakeven (-$21/mo). Offer $432,848 (10.0% Cap) to generate +$1,162/mo net profit."
        ]
    }

    pdf_path = generate_pdf_report(pdf_data, '486_HAZLE_AVE_UNDERWRITING_REPORT.pdf')
    print(f"486 Hazle Ave PDF Generated at: {pdf_path}")

if __name__ == "__main__":
    run_hazle_underwriting()
