---
name: realestate
description: AI real estate research engine for property analysis, underwriting, comps, rental yield, T12 parsing, scoring (0-100), and PDF report generation.
---

# Real Estate Research & Underwriting Engine

This skill provides an AI real estate research engine powered by 5 parallel subagents, a composite 0-100 property scoring model, T12 financial statement parsing, SQLite memory caching, and ReportLab PDF report generation.

## Available Commands

### 1. `/realestate analyze <address>`
Runs a full 5-subagent parallel analysis across:
- **Comps Agent**: Comparable sales, price/sqft, fair market value.
- **Rental Agent**: Rent yield, NOI, Cap Rate, Cash-on-Cash return.
- **Neighborhood Agent**: Schools, safety, walkability, growth trajectory.
- **Investment Agent**: Buy & Hold, BRRRR, Fix & Flip, MAO threshold.
- **Market Agent**: Inventory months, DOM, supply/demand balance.

Generates an interactive **Markdown Artifact** + downloadable **PDF Report**.

### 2. `/realestate quick <address>`
Provides a 60-second terminal/chat property snapshot.

### 3. `/realestate comps <address>`
Retrieves comparable sales and price per sqft data.

### 4. `/realestate rental <address>`
Generates rental income and cash flow projections.

### 5. `/realestate underwrite <address> [--t12 path/to/t12.json]`
Parses T12 statements, extracts true NOI, factors post-sale property taxes and insurance quotes, and computes Maximum Allowable Offer ($\text{MAO}$).

### 6. `/realestate report-pdf`
Compiles current property analysis into a publication-ready PDF report (`PROPERTY-REPORT.pdf`).

### 7. `/realestate eval`
Runs the automated **EVALS test suite** (`python3 evals/run_evals.py`) to verify underwriting formulas, T12 parsing accuracy, and scoring bounds.

---

## Scoring Methodology (0–100)

$$\text{Score} = (0.25 \times \text{Comps}) + (0.20 \times \text{Income}) + (0.20 \times \text{Neighborhood}) + (0.20 \times \text{Upside}) + (0.15 \times \text{Market})$$

| Score Range | Grade | Signal |
| :--- | :--- | :--- |
| **85 – 100** | **A+** | **Strong Buy** |
| **70 – 84** | **A** | **Buy** |
| **55 – 69** | **B** | **Hold/Watch** |
| **40 – 54** | **C** | **Caution** |
| **25 – 39** | **D** | **Pass** |
| **0 – 24** | **F** | **Avoid** |
