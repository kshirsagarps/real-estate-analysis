#!/usr/bin/env python3
"""
SQLite-Backed Persistent Memory & Caching Engine

Manages zip code caching (7-day TTL), market rule persistence, 
and deal history tracking for subagents.
"""

import sqlite3
import json
import os
import time
from typing import Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "memory", "realestate_memory.db")

class MemoryEngine:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Zip code / location query cache with TTL
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS zip_cache (
                    cache_key TEXT PRIMARY KEY,
                    data_json TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    ttl_seconds REAL NOT NULL
                )
            """)
            # Persistent market & county rules
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS market_rules (
                    location_key TEXT NOT NULL,
                    rule_name TEXT NOT NULL,
                    rule_value TEXT NOT NULL,
                    updated_at REAL NOT NULL,
                    PRIMARY KEY (location_key, rule_name)
                )
            """)
            # Deal history database
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS deal_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    address TEXT NOT NULL,
                    predicted_data TEXT NOT NULL,
                    actual_data TEXT,
                    property_score REAL,
                    created_at REAL NOT NULL
                )
            """)
            conn.commit()

    def set_cache(self, cache_key: str, data: Dict[str, Any], ttl_days: float = 7.0) -> None:
        ttl_seconds = ttl_days * 86400.0
        now = time.time()
        data_json = json.dumps(data)
        with self._get_connection() as conn:
            conn.cursor().execute("""
                INSERT OR REPLACE INTO zip_cache (cache_key, data_json, created_at, ttl_seconds)
                VALUES (?, ?, ?, ?)
            """, (cache_key, data_json, now, ttl_seconds))
            conn.commit()

    def get_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        now = time.time()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data_json, created_at, ttl_seconds FROM zip_cache WHERE cache_key = ?", (cache_key,))
            row = cursor.fetchone()
            if not row:
                return None
            if (now - row["created_at"]) > row["ttl_seconds"]:
                # Cache expired
                cursor.execute("DELETE FROM zip_cache WHERE cache_key = ?", (cache_key,))
                conn.commit()
                return None
            return json.loads(row["data_json"])

    def set_rule(self, location_key: str, rule_name: str, rule_value: Any) -> None:
        now = time.time()
        val_str = json.dumps(rule_value) if not isinstance(rule_value, str) else rule_value
        with self._get_connection() as conn:
            conn.cursor().execute("""
                INSERT OR REPLACE INTO market_rules (location_key, rule_name, rule_value, updated_at)
                VALUES (?, ?, ?, ?)
            """, (location_key.upper(), rule_name, val_str, now))
            conn.commit()

    def get_rules(self, location_key: str) -> Dict[str, Any]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT rule_name, rule_value FROM market_rules WHERE location_key = ?", (location_key.upper(),))
            rows = cursor.fetchall()
            result = {}
            for row in rows:
                try:
                    result[row["rule_name"]] = json.loads(row["rule_value"])
                except Exception:
                    result[row["rule_name"]] = row["rule_value"]
            return result

    def save_deal(self, address: str, predicted_data: Dict[str, Any], score: float) -> int:
        now = time.time()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO deal_history (address, predicted_data, property_score, created_at)
                VALUES (?, ?, ?, ?)
            """, (address, json.dumps(predicted_data), score, now))
            conn.commit()
            return cursor.lastrowid

if __name__ == "__main__":
    mem = MemoryEngine()
    mem.set_cache("78701", {"avg_rent": 2500, "market_cap": 5.8}, ttl_days=7)
    cached = mem.get_cache("78701")
    print("Memory Cache Test (78701):", cached)
    mem.set_rule("AUSTIN_TX", "tax_reassessment_factor", 0.85)
    print("Market Rules Test (AUSTIN_TX):", mem.get_rules("AUSTIN_TX"))
