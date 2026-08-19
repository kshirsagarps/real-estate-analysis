# Market Agent (`market_agent`)

The **Market Agent** analyzes local macro market trends, inventory balance, and buyer/seller leverage dynamics.

## Responsibilities & Scope
1. **Months of Supply (MOS)**:
   - $<3\text{ months}$: Strong Seller's Market.
   - $3\text{--}6\text{ months}$: Balanced Market.
   - $>6\text{ months}$: Buyer's Market.
2. **Days on Market (DOM)**: Average time listings remain active before contract.
3. **List-to-Sale Price Ratio**: Percentage of asking price achieved at closing.
4. **Price Cut Frequency**: Percentage of active listings offering price drops.
5. **Outputs**:
   - Market regime classification (**Buyer**, **Balanced**, **Seller**).
   - Market velocity metrics.
   - Category Score for **Market Conditions (0-100)**.

## Model & Performance
- **Model**: `Gemini Flash` (rapid macro data lookup & trend extraction).
- **Execution Mode**: Concurrent parallel execution.
