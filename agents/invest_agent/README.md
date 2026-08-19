# Investment Agent (`invest_agent`)

The **Investment Agent** evaluates value-add upside, rehab estimates, and multi-scenario exit strategies (BRRRR, Fix-and-Flip, Buy & Hold).

## Responsibilities & Scope
1. **Rehab & CapEx Budgeting**: Estimates light, medium, or heavy rehabilitation costs ($\text{Light: \$15-25/sqft}$, $\text{Medium: \$30-50/sqft}$, $\text{Heavy: \$60+/sqft}$).
2. **After Repair Value (ARV)**: Projects property value post-renovation.
3. **Strategy Scenarios**:
   - **Buy & Hold**: Long-term equity build, debt paydown, and appreciation.
   - **BRRRR**: Refinance cash-out potential ($75\text{--}80\%\text{ LTV}$) to recycle capital.
   - **Fix & Flip**: Net profit after rehab, holding costs, and closing/realtor fees ($70\%\text{ Rule}$).
4. **Maximum Allowable Offer ($\text{MAO}$)**:
   $$\text{MAO} = (\text{ARV} \times 0.70) - \text{Rehab Costs}$$
5. **Outputs**:
   - Strategy recommendation matrix.
   - Calculated MAO threshold.
   - Category Score for **Investment Upside (0-100)**.

## Model & Performance
- **Model**: `Gemini Pro` (complex financial modeling & multi-scenario optimization).
- **Execution Mode**: Concurrent parallel execution.
