# AI Real Estate Research Engine & Financial Underwriter

An autonomous **AI Real Estate Research Engine** built for Gemini and Antigravity. It features **5 parallel subagents**, a **0–100 composite property scoring model**, **T12 financial statement parsing**, **SQLite persistent market memory**, **publication-ready PDF report generation**, and an **automated EVALS evaluation suite**.

---

## Features Overview

- **5 Parallel Specialized Subagents**:
  - [`comps_agent`](agents/comps_agent/README.md): Comparable sales & Fair Market Value.
  - [`rental_agent`](agents/rental_agent/README.md): Income yield, NOI, Cap Rate, and Cash-on-Cash underwriting.
  - [`neighborhood_agent`](agents/neighborhood_agent/README.md): School ratings, safety, walkability, and demographics.
  - [`invest_agent`](agents/invest_agent/README.md): Buy & Hold, BRRRR, Fix & Flip, and Maximum Allowable Offer ($\text{MAO}$).
  - [`market_agent`](agents/market_agent/README.md): Local inventory, Days on Market (DOM), supply/demand dynamics.
- **T12 Operating Statement Parser**: Extracts true NOI and line-item operating expenses (`scripts/parse_t12.py`).
- **Composite Property Score (0–100)**: Letter grades ($A+$ to $F$) and investment recommendation signals (`scripts/score_property.py`).
- **SQLite Persistent Caching & Memory**: Caches zip code queries (7-day TTL) and retains county tax/insurance rules (`scripts/memory_engine.py`).
- **Publication-Ready PDF Reports**: Generates professional 6-page PDF property analysis reports (`scripts/generate_pdf.py`).
- **Automated EVALS Suite**: Test suite verifying underwriting math, parsing accuracy, and scoring bounds (`evals/run_evals.py`).

---

## Directory Structure

```
real-estate-analysis/
├── .gemini/
│   └── skills/
│       └── realestate/
│           ├── SKILL.md                 # Primary skill definition & routing
│           └── README.md                # Skill documentation
├── agents/                              # 5 Specialized Subagents & Guides
│   ├── comps_agent/                     # Comps Agent & README
│   ├── rental_agent/                    # Rental Underwriter & README
│   ├── neighborhood_agent/              # Neighborhood Analyst & README
│   ├── invest_agent/                    # Investment Strategist & README
│   └── market_agent/                    # Market Analyst & README
├── scripts/                             # Core Python Underwriting & Memory Scripts
│   ├── score_property.py                # 0-100 Scoring & Grade Engine
│   ├── parse_t12.py                     # Financial Statement & T12 Parser
│   ├── memory_engine.py                 # SQLite Memory & 7-Day Caching
│   ├── calibrate.py                     # Prediction vs Actual Calibration
│   └── generate_pdf.py                  # ReportLab PDF Report Generator
├── evals/                               # Automated Benchmark Evaluation Suite
│   ├── test_underwriting_math.py        # Financial math tests
│   ├── test_t12_parser.py               # T12 parser accuracy tests
│   ├── test_scoring_engine.py           # Property score tests
│   ├── test_memory_engine.py            # SQLite cache & memory tests
│   ├── run_evals.py                     # Master test suite runner
│   └── README.md                        # EVALS documentation
├── requirements.txt                     # Project Python dependencies
└── README.md                            # Master project documentation
```

---

## Quick Start & Commands

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Run Automated EVALS Suite
```bash
python3 evals/run_evals.py
```

### 3. Usage in Antigravity Chat
- `/realestate analyze <address>` — Full 5-agent parallel property analysis & PDF generation.
- `/realestate quick <address>` — 60-second property snapshot.
- `/realestate underwrite <address> --t12 path/to/t12.json` — Deep financial audit with T12 parsing.
- `/realestate report-pdf` — Build PDF report.
- `/realestate eval` — Run evaluation benchmark suite.

---

## Subagent & Component Documentation
For detailed guides on each subagent and subsystem, see:
- 📖 [Comps Agent User Guide](agents/comps_agent/README.md)
- 📖 [Rental Agent User Guide](agents/rental_agent/README.md)
- 📖 [Neighborhood Agent User Guide](agents/neighborhood_agent/README.md)
- 📖 [Investment Agent User Guide](agents/invest_agent/README.md)
- 📖 [Market Agent User Guide](agents/market_agent/README.md)
- 📖 [EVALS Framework Guide](evals/README.md)
- 📖 [Real Estate Skill Guide](.gemini/skills/realestate/README.md)
