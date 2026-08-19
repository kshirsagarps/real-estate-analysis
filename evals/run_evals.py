#!/usr/bin/env python3
"""
EVALS Test Suite Runner

Runs pytest evaluation suites across underwriting math, T12 parsing, 
scoring engine bounds, and memory engine persistence. Outputs formatted scorecard.
"""

import sys
import subprocess
import os

def run_all_evals():
    print("=" * 60)
    print("  RUNNING AI REAL ESTATE ENGINE EVALUATION SUITE (EVALS)")
    print("=" * 60)
    
    evals_dir = os.path.dirname(__file__)
    cmd = [sys.executable, "-m", "pytest", evals_dir, "-v", "--tb=short"]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    print("=" * 60)
    if result.returncode == 0:
        print("  EVALS RESULT: PASSED ALL BENCHMARK TESTS ✅")
    else:
        print("  EVALS RESULT: FAILED ONE OR MORE BENCHMARKS ❌")
    print("=" * 60)
    
    sys.exit(result.returncode)

if __name__ == "__main__":
    run_all_evals()
