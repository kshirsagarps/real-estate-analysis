#!/usr/bin/env python3
"""
Trailing 12-Month (T12) Operating Statement Financial Parser

Extracts Gross Rent, Vacancy/Loss to Lease, Operating Expenses,
and true Net Operating Income (NOI) from structured financial data.
"""

import json
from typing import Dict, Any

class T12Parser:
    def __init__(self):
        pass

    def parse_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses T12 dictionary data and computes normalized financial summary.
        """
        gross_potential_rent = float(data.get("gross_potential_rent", 0.0))
        vacancy_loss = float(data.get("vacancy_loss", 0.0))
        other_income = float(data.get("other_income", 0.0))

        effective_gross_income = gross_potential_rent - abs(vacancy_loss) + other_income

        # Operating expenses breakdown
        taxes = float(data.get("property_taxes", 0.0))
        insurance = float(data.get("insurance", 0.0))
        utilities = float(data.get("utilities", 0.0))
        management = float(data.get("management_fees", 0.0))
        repairs_maint = float(data.get("repairs_maintenance", 0.0))
        admin_other = float(data.get("admin_other", 0.0))

        total_expenses = taxes + insurance + utilities + management + repairs_maint + admin_other

        noi = effective_gross_income - total_expenses
        expense_ratio = (total_expenses / effective_gross_income * 100) if effective_gross_income > 0 else 0.0

        return {
            "gross_potential_rent": round(gross_potential_rent, 2),
            "vacancy_loss": round(abs(vacancy_loss), 2),
            "other_income": round(other_income, 2),
            "effective_gross_income": round(effective_gross_income, 2),
            "expenses": {
                "property_taxes": round(taxes, 2),
                "insurance": round(insurance, 2),
                "utilities": round(utilities, 2),
                "management_fees": round(management, 2),
                "repairs_maintenance": round(repairs_maint, 2),
                "admin_other": round(admin_other, 2),
                "total_operating_expenses": round(total_expenses, 2)
            },
            "net_operating_income": round(noi, 2),
            "expense_ratio_pct": round(expense_ratio, 2)
        }

    def parse_json_str(self, json_str: str) -> Dict[str, Any]:
        """Parse JSON string format T12."""
        data = json.loads(json_str)
        return self.parse_dict(data)

if __name__ == "__main__":
    sample_t12 = {
        "gross_potential_rent": 120000.0,
        "vacancy_loss": 6000.0,
        "other_income": 2000.0,
        "property_taxes": 14000.0,
        "insurance": 4500.0,
        "utilities": 8000.0,
        "management_fees": 9120.0,
        "repairs_maintenance": 7500.0,
        "admin_other": 1800.0
    }
    parser = T12Parser()
    res = parser.parse_dict(sample_t12)
    print("Parsed T12 Summary:")
    print(json.dumps(res, indent=2))
