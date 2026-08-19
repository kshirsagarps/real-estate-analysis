# Candidate Comp Discovery Agent (`comps_agent`)

The **Candidate Comp Discovery Agent** is a specialized subagent responsible for discovering, retrieving, and formatting candidate comparable property sales (comps).

> [!IMPORTANT]
> **Explicit AI vs. Deterministic Boundary**: This AI subagent **ONLY DISCOVERS** candidate comps. It does NOT decide final Fair Market Value (FMV). All candidate comps are passed directly to `scripts/comp_engine.py` for deterministic eligibility filtering, similarity scoring (0-100), outlier exclusion, time adjustments, and weighted trimmed-mean FMV calculation.

## Architectural Flow
```text
AI Comps Agent (DISCOVER) 
      ↓
Fact Reconciler (VERIFY & RESOLVE) 
      ↓
Provenance Layer (VALIDATE SOURCE & TIER) 
      ↓
Deterministic Comp Engine (FILTER, SCORE & TIME-ADJUST) 
      ↓
Deterministic Valuation Engine (CALCULATE FMV & DISPERSION)
```

## Responsibilities & Scope
1. **Candidate Discovery**: Searches public records and listing services for multi-family property sales.
2. **Fact Extraction**: Extracts sale price, sale date, building square footage, unit count, bedroom/bathroom mix, distance, and property condition notes.
3. **Data Handoff**: Hands structured candidate JSON to `comp_engine.py`.

## Model & Performance
- **Model**: `Gemini Flash` (rapid web retrieval & candidate comp discovery).
- **Execution Mode**: Concurrent background execution.
