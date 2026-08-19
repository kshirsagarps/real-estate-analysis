#!/usr/bin/env python3
"""
Master EVALS Test Suite Runner

Runs pytest evaluation suites across underwriting math, T12 parsing, 
comp eligibility funnel, similarity scoring, valuation dispersion, 
fact reconciliation, 4-tier provenance, stress testing, and offer price bands.
"""

import sys
import subprocess
import os

def run_all_evals():
    print("=" * 70)
    print("  RUNNING INDUSTRIAL-GRADE REAL ESTATE EVALUATION SUITE (EVALS)")
    print("=" * 70)
    
    evals_dir = os.path.dirname(__file__)
    cmd = [sys.executable, "-m", "pytest", evals_dir, "-v", "--tb=short"]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    print("=" * 70)
    if result.returncode == 0:
        print("  EVALS RESULT: PASSED ALL BENCHMARK TESTS ✅")
    else:
        print("  EVALS RESULT: FAILED ONE OR MORE BENCHMARKS ❌")
    print("=" * 70)
    
    sys.exit(result.returncode)

if __name__ == "__main__":
    run_all_evals()
