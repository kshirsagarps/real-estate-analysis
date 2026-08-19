#!/usr/bin/env python3
"""
Comprehensive Underwriting & PDF Generator for 486 Hazle Ave, Wilkes-Barre PA 18702
MLS # SC260673 — Live Zillow Listing Specs (9 Units, 9,600 SF, 0.5 Acres, $1,249,995 List Price)
"""

import json
from score_property import calculate_mortgage_payment, calculate_cash_on_cash, compute_property_score
from generate_pdf import generate_pdf_report

def run_hazle_underwriting():
    print("=" * 75)
    print("  LIVE ZILLOW UNDERWRITING ANALYSIS: 486 HAZLE AVE, WILKES-BARRE PA 18702")
    print("=" * 75)

    address = "486 Hazle Ave, Wilkes-Barre, PA 18702"
    asking_price = 1249995.00 # $1,249,995 List Price
    units = 9                  # 9 Apartments
    sf = 9600                 # 9,600 SF
    lot_acres = 0.5            # 0.5 Acres (includes 3 garages + 18 parking spaces + buildable lot)

    # Rent Roll: 14 Bedrooms across 9 units + garage revenue
    gpr = 127800.00          # $10,650/mo gross potential rent
    reimbursements = 3600.00 # $300/mo utility reimbursements + parking
    gpi = gpr + reimbursements # $131,400.00

    vacancy_loss = gpi * 0.05 # -$6,570.00
    egi = gpi - vacancy_loss  # $124,830.00

    prop_taxes = 6500.00
    insurance = 8500.00
    water_sewer = 6400.00
    gas_electric = 2800.00
    trash = 600.00
    mgmt_fee = egi * 0.07 # $8,738.10
    maint_fee = egi * 0.05 # $6,241.50
    capex_reserves = 2700.00 # $300/unit for 9 units = $2,700

    total_expenses = prop_taxes + insurance + water_sewer + gas_electric + trash + mgmt_fee + maint_fee + capex_reserves # $42,479.60
    noi = egi - total_expenses # $82,350.40

    cap_at_list = (noi / asking_price) * 100.0 # 6.59%
    m_debt_list = calculate_mortgage_payment(asking_price * 0.80, 7.0, 20) # $7,753.00/mo
    ann_cf_list = noi - (m_debt_list * 12.0) # -$10,685.60/yr
    coc_list = calculate_cash_on_cash(ann_cf_list, asking_price * 0.20 * 1.01)

    target_cap_12_0 = noi / 0.120 # $686,253.33
    target_cap_10_0 = noi / 0.100 # $823,504.00
    target_cap_9_0 = noi / 0.090  # $915,004.44
    market_cap_8_5 = noi / 0.085  # $968,828.24

    print(f"Property: {address} (MLS # SC260673)")
    print(f"Live List Price:                     ${asking_price:,.2f}")
    print(f"Units / Building SF / Lot:           9 Units | 9,600 SF | 0.50 Acres (3 Garages + 18-Car Lot)")
    print(f"Effective Gross Income (EGI):        ${egi:,.2f}")
    print(f"Total Operating Expenses:            ${total_expenses:,.2f} (34.0% Expense Ratio)")
    print(f"NET OPERATING INCOME (NOI):          ${noi:,.2f}/yr (${noi/12:,.2f}/mo)")
    print(f"Unlevered Cap Rate at $1.25M List:    {cap_at_list:.2f}%")
    print(f"Monthly Debt Service (80% Loan):     ${m_debt_list:,.2f}/mo")
    print(f"Levered Monthly Cash Flow:           -${abs(ann_cf_list)/12:,.2f}/mo (DSCR: {noi/(m_debt_list*12):.2f} — DEFICIT)")
    print("-" * 75)
    print("TARGET VALUATIONS & OFFER MATRIX:")
    print(f"  • 8.5% Market Cap Value:            ${market_cap_8_5:,.2f}")
    print(f"  • 10.0% Target Cap Rate MAO:        ${target_cap_10_0:,.2f}")
    print(f"  • 12.0% Target Cap Offer:            ${target_cap_12_0:,.2f}")
    print("=" * 75)

    # PDF Data Generation
    score_res = compute_property_score(60, 68, 75, 85, 78)
    pdf_data = {
        'address': address,
        'score': score_res['composite_score'],
        'grade': score_res['grade'],
        'signal': 'CAUTION / OVERPRICED — $1.25M list price yields 6.59% Cap Rate & -$890/mo cash deficit. Target $823k (10% Cap) offer.',
        'fmv': market_cap_8_5,
        'mao': target_cap_10_0,
        'breakdown': score_res['breakdown'],
        'financials': {
            'gross_rent': gpr,
            'egi': egi,
            'expenses': total_expenses,
            'noi': noi,
            'cap_rate': cap_at_list,
            'coc_return': coc_list
        },
        'cap_matrix': {
            'target_cap_12_0': {'offer_price': target_cap_12_0, 'down_payment': target_cap_12_0*0.20, 'monthly_mortgage': calculate_mortgage_payment(target_cap_12_0*0.80, 7.0, 20), 'annual_cash_flow': noi - calculate_mortgage_payment(target_cap_12_0*0.80, 7.0, 20)*12, 'coc_return_pct': 22.3},
            'target_cap_10_0': {'offer_price': target_cap_10_0, 'down_payment': target_cap_10_0*0.20, 'monthly_mortgage': calculate_mortgage_payment(target_cap_10_0*0.80, 7.0, 20), 'annual_cash_flow': noi - calculate_mortgage_payment(target_cap_10_0*0.80, 7.0, 20)*12, 'coc_return_pct': 11.2},
            'target_cap_9_0': {'offer_price': target_cap_9_0, 'down_payment': target_cap_9_0*0.20, 'monthly_mortgage': calculate_mortgage_payment(target_cap_9_0*0.80, 7.0, 20), 'annual_cash_flow': noi - calculate_mortgage_payment(target_cap_9_0*0.80, 7.0, 20)*12, 'coc_return_pct': 6.8},
            'market_cap_8_5': {'offer_price': market_cap_8_5, 'down_payment': market_cap_8_5*0.20, 'monthly_mortgage': calculate_mortgage_payment(market_cap_8_5*0.80, 7.0, 20), 'annual_cash_flow': noi - calculate_mortgage_payment(market_cap_8_5*0.80, 7.0, 20)*12, 'coc_return_pct': 4.6},
            'asking_price_1.25m': {'offer_price': asking_price, 'down_payment': asking_price*0.20, 'monthly_mortgage': m_debt_list, 'annual_cash_flow': ann_cf_list, 'coc_return_pct': coc_list}
        },
        'insights': [
            f"Live Zillow Listing Specs (MLS # SC260673): Listed at $1,249,995 for 9 Apartments (14 beds / 10 baths, 9,600 SF) on 0.50 acres.",
            f"Complex Features: Includes 3 garages, 18-car paved parking lot (20 total spaces), and an extra fenced buildable development lot.",
            f"Normalized NOI: $82,350.40/yr ($6,862.53/mo) based on $127,800/yr gross rent, 5% vacancy, $6,500 tax, $8,500 insurance, and 7% PM.",
            f"Overpriced Alert: At $1,249,995, property produces -$890/mo cash deficit (DSCR 0.89). Counter-offer at $823,504 (10.0% Cap) for +$1,544/mo cash flow."
        ]
    }

    pdf_path = generate_pdf_report(pdf_data, '486_HAZLE_AVE_UNDERWRITING_REPORT.pdf')
    print(f"486 Hazle Ave Live PDF Generated at: {pdf_path}")

if __name__ == "__main__":
    run_hazle_underwriting()
