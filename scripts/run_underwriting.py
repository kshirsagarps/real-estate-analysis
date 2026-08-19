#!/usr/bin/env python3
"""
Underwriting Execution Script for 273-275 New Hancock Street, Wilkes-Barre PA
"""

import json
from score_property import (
    compute_property_score,
    calculate_noi,
    calculate_cap_rate,
    calculate_cash_on_cash,
    calculate_mortgage_payment,
    generate_cap_rate_offer_matrix
)
from memory_engine import MemoryEngine
from generate_pdf import generate_pdf_report

def run_underwriting():
    # Unit Rent Roll Breakdown based on Attached Leases & User Input
    units = {
        'Unit 1 (3 Bed / 2 Bath)': 1484.0, # MLS
        'Unit 2 (2 Bed / 1 Bath)': 1300.0, # Attached Lease (Reyvana McKnight)
        'Unit 3 (2 Bed / 1 Bath)': 1250.0, # MLS
        'Unit 4 (1 Bed / 1 Bath)': 1025.0, # Attached Lease (Josephine Ramirez)
        'Unit 5 (1 Bed / 1 Bath)': 1100.0  # User specified vacant unit rent
    }

    monthly_gpr = sum(units.values()) # $6,159/mo
    annual_gpr = monthly_gpr * 12.0   # $73,908/yr
    vacancy_loss = annual_gpr * 0.05  # $3,695.40 (5%)
    egi = annual_gpr - vacancy_loss   # $70,212.60 / yr

    # Operating Expenses with 2.5% Property Management
    real_estate_taxes = 2676.38       # MLS
    insurance = 4215.00               # Actual Policy Declaration
    sewer = 880.00                    # MLS
    garbage = 350.00                  # MLS
    property_mgmt = egi * 0.025       # 2.5% PM fee = $1,755.32
    maintenance_reserves = egi * 0.05 # 5% maintenance = $3,510.63

    total_expenses = real_estate_taxes + insurance + sewer + garbage + property_mgmt + maintenance_reserves # $13,387.33
    noi = calculate_noi(egi, total_expenses) # $56,825.27

    price = 500000.0
    actual_cap_rate = calculate_cap_rate(noi, price) # 11.37%

    # Financing: 20% Down ($100k), 80% Loan ($400k), 20 Years @ 7.0%
    down_payment = price * 0.20 # $100,000
    loan_amount = price * 0.80  # $400,000
    monthly_mortgage = calculate_mortgage_payment(loan_amount, interest_rate_pct=7.0, loan_years=20) # $3,101.20 / mo
    annual_debt_service = monthly_mortgage * 12.0 # $37,214.40 / yr
    net_cash_flow = noi - annual_debt_service     # $19,610.87 / yr ($1,634.24 / mo)
    initial_investment = down_payment + (price * 0.01) # $105,000 (Down + 1% closing)
    coc_return = calculate_cash_on_cash(net_cash_flow, initial_investment) # 18.68%

    # Cap Rate Offer Matrix (8.0% to 12.0%) with 20% Down & 20yr @ 7% Loan
    cap_matrix = generate_cap_rate_offer_matrix(
        noi, start_cap=8.0, end_cap=12.0, step=0.5,
        down_payment_pct=20.0, interest_rate_pct=7.0, loan_years=20
    )

    # Score
    score_res = compute_property_score(90, 96, 68, 88, 78)

    # Memory Engine DB
    mem = MemoryEngine()
    deal_id = mem.save_deal('273-275 New Hancock Street, Wilkes Barre, PA 18702', {
        'gpr': annual_gpr, 'egi': egi, 'noi': noi, 'cap_rate': actual_cap_rate, 'price': price,
        'loan_terms': {'down_pct': 20, 'interest_rate': 7.0, 'years': 20, 'monthly_payment': monthly_mortgage},
        'cash_flow': net_cash_flow, 'coc_return': coc_return
    }, score=score_res['composite_score'])

    # Build PDF Data
    pdf_data = {
        'address': '273-275 New Hancock Street, Wilkes-Barre, PA 18702',
        'score': score_res['composite_score'],
        'grade': score_res['grade'],
        'signal': score_res['signal'],
        'fmv': cap_matrix['8.0%']['offer_price'],
        'mao': cap_matrix['10.0%']['offer_price'],
        'breakdown': score_res['breakdown'],
        'financials': {
            'gross_rent': annual_gpr,
            'egi': egi,
            'expenses': total_expenses,
            'noi': noi,
            'cap_rate': actual_cap_rate,
            'coc_return': coc_return
        },
        'cap_matrix': cap_matrix,
        'insights': [
            'Financing Structure: 20% Down Payment ($100,000), 20-Year Loan at 7.0% Interest Rate ($3,101.20/mo P&I).',
            'Property Management Audit: PM fee set to 2.5% ($1,755.32/yr), yielding total operating expenses of $13,387.33 (19.1% Expense Ratio).',
            'Higher Net Operating Income: Actual NOI is $56,825.27/yr, producing an 11.37% Cap Rate at the $500,000 list price.',
            'Net Levered Cash Flow: $19,610.87/yr ($1,634.24/mo net profit in pocket after paying all mortgage debt).',
            'Exceptional Cash-on-Cash Return: 18.68% CoC return on total cash invested ($105,000 down + closing costs).'
        ]
    }

    pdf_path = generate_pdf_report(pdf_data, '273_NEW_HANCOCK_FINANCING_REPORT.pdf')
    print(f"FINANCING MODEL COMPLETE: Deal ID {deal_id} saved. PDF: {pdf_path}")

if __name__ == "__main__":
    run_underwriting()
