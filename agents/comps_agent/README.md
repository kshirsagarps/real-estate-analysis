# Comps Agent (`comps_agent`)

The **Comps Agent** is a specialized subagent responsible for evaluating comparable property sales (comps) and estimating Fair Market Value (FMV).

## Responsibilities & Scope
1. **Search Radius**: Identifies sold properties within $0.5\text{--}2.0\text{ miles}$ of the subject property.
2. **Adjustment Heuristics**:
   - $\pm 10\%$ for bedroom/bathroom discrepancies.
   - Adjusts for total square footage ($\text{Price/sq. ft.}$ normalization).
   - Adjusts for property age, lot size, pool/garage amenities, and condition.
3. **Outputs**:
   - Average and median price per square foot.
   - Top 3–5 comparable property listings with sale dates and prices.
   - Estimated Fair Market Value (FMV) range.
   - Category Score for **Value & Comps (0-100)**.

## Model & Performance
- **Model**: `Gemini Flash` (fast web retrieval & search summarization).
- **Execution Mode**: Concurrent parallel execution alongside 4 peer agents.
