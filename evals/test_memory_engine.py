#!/usr/bin/env python3
"""
EVALS Test Suite: SQLite Memory & Cache Engine
"""

import sys
import os
import time
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts"))

from memory_engine import MemoryEngine

def test_cache_set_get():
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        mem = MemoryEngine(db_path=tmp.name)
        mem.set_cache("TEST_ZIP", {"rent": 2200}, ttl_days=1.0)
        data = mem.get_cache("TEST_ZIP")
        assert data is not None
        assert data["rent"] == 2200

def test_cache_expiration():
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        mem = MemoryEngine(db_path=tmp.name)
        # Set cache with negative TTL (expired immediately)
        mem.set_cache("EXPIRED_KEY", {"val": 123}, ttl_days=-1.0)
        data = mem.get_cache("EXPIRED_KEY")
        assert data is None

def test_rules_persistence():
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        mem = MemoryEngine(db_path=tmp.name)
        mem.set_rule("AUSTIN_TX", "tax_rate", 0.018)
        rules = mem.get_rules("AUSTIN_TX")
        assert "tax_rate" in rules
        assert rules["tax_rate"] == 0.018
