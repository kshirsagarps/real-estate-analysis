# Real Estate Skill User Guide

The **`realestate` skill** transforms Antigravity into an autonomous real estate research engine.

## Key Features
- **Parallel Multi-Agent Subsystems**: Invokes 5 specialized subagents (`comps_agent`, `rental_agent`, `neighborhood_agent`, `invest_agent`, `market_agent`).
- **T12 & Financial Underwriting**: Parses Trailing 12-Month operating statements via `scripts/parse_t12.py`.
- **0–100 Weighted Property Score**: Evaluates properties across 5 weighted dimensions via `scripts/score_property.py`.
- **Persistent Caching & Memory**: Uses SQLite (`scripts/memory_engine.py`) to cache zip code research (7-day TTL) and retain local market tax/insurance rules.
- **PDF Report Generator**: Uses `scripts/generate_pdf.py` to build professional PDF property reports.

## Command Reference
- `/realestate analyze <address>`
- `/realestate quick <address>`
- `/realestate comps <address>`
- `/realestate rental <address>`
- `/realestate underwrite <address>`
- `/realestate report-pdf`
- `/realestate eval`

## Architecture Integration
This skill executes scripts via standard Python 3.8+ runtimes and delegates tasks to subagents defined in `agents/`.
