# Rental Agent (`rental_agent`)

The **Rental Agent** handles income underwriting, expense modeling, and cash flow projections for long-term (LTR) and short-term (STR / Airbnb) rental strategies.

## Responsibilities & Scope
1. **Gross Revenue Estimation**: Estimates monthly market rent based on local rental comps and unit mix.
2. **Expense & Loss Underwriting**:
   - Vacancy & Credit Loss ($5\text{--}8\%$).
   - Property Taxes & Fire/Liability Insurance.
   - Property Management Fees ($8\text{--}10\%$).
   - Maintenance & CapEx Reserves ($5\text{--}10\%$).
3. **Core Financial Calculations**:
   - Net Operating Income ($\text{NOI} = \text{EGI} - \text{Operating Expenses}$).
   - Capitalization Rate ($\text{Cap Rate} = \frac{\text{NOI}}{\text{Purchase Price}}$).
   - Cash-on-Cash Return ($\text{CoC} = \frac{\text{Annual Cash Flow}}{\text{Total Initial Cash Invested}}$).
4. **Outputs**:
   - Monthly and annual cash flow projections.
   - 1% Rule and Gross Rent Multiplier (GRM) compliance status.
   - Category Score for **Income Potential (0-100)**.

## Model & Performance
- **Model**: `Gemini Pro` (high precision mathematical reasoning).
- **Execution Mode**: Concurrent parallel execution.
