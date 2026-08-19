# EVALS Evaluation Framework

The **EVALS framework** provides automated unit, financial math, and performance evaluations for the Real Estate Research Engine.

## Evaluation Test Modules

1. **`test_underwriting_math.py`**:
   - Verifies mathematical contracts for $\text{NOI}$, $\text{Cap Rate}$, $\text{Cash-on-Cash return}$, and $\text{Maximum Allowable Offer (MAO)}$.
2. **`test_t12_parser.py`**:
   - Validates line-item financial extraction (GPR, Vacancy, EGI, Operating Expenses, NOI) against benchmark T12 datasets.
3. **`test_scoring_engine.py`**:
   - Ensures weighted score bounds ($0\text{--}100$), clamping of out-of-range subscores, and correct letter grade ($A+$ to $F$) assignments.
4. **`test_memory_engine.py`**:
   - Tests SQLite cache setting/retrieval, 7-day TTL expiration logic, and persistent market rule lookups.

## How to Run EVALS

Run the automated test runner script:
```bash
python3 evals/run_evals.py
```
Or via the Antigravity command:
```text
/realestate eval
```
Or directly via `pytest`:
```bash
pytest evals/ -v
```
