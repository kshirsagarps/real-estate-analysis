#!/usr/bin/env python3
"""
Outcome Calibration & Accuracy Tracking Script

Compares initial AI property predictions against actual deal performance, 
calculating variance percentage and updating market memory.
"""

from typing import Dict, Any
from memory_engine import MemoryEngine

def calibrate_deal(deal_id: int, actual_data: Dict[str, Any], memory_engine: MemoryEngine = None) -> Dict[str, Any]:
    if memory_engine is None:
        memory_engine = MemoryEngine()

    # Query deal from DB
    with memory_engine._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, address, predicted_data FROM deal_history WHERE id = ?", (deal_id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Deal ID {deal_id} not found in database.")

        import json
        predicted = json.loads(row["predicted_data"])
        address = row["address"]

        variances = {}
        for key in ["rent", "price", "rehab", "expenses"]:
            if key in predicted and key in actual_data:
                pred_val = float(predicted[key])
                act_val = float(actual_data[key])
                if pred_val > 0:
                    diff_pct = round(((act_val - pred_val) / pred_val) * 100, 2)
                    variances[key] = {
                        "predicted": pred_val,
                        "actual": act_val,
                        "variance_pct": diff_pct
                    }

        # Update actuals in DB
        cursor.execute("UPDATE deal_history SET actual_data = ? WHERE id = ?", (json.dumps(actual_data), deal_id))
        conn.commit()

        return {
            "deal_id": deal_id,
            "address": address,
            "variances": variances
        }

if __name__ == "__main__":
    mem = MemoryEngine()
    deal_id = mem.save_deal("123 Main St, Austin TX", {"rent": 2500, "price": 450000}, score=78.5)
    print(f"Created deal {deal_id}")
    cal_res = calibrate_deal(deal_id, {"rent": 2400, "price": 445000}, memory_engine=mem)
    print("Calibration Output:")
    import json
    print(json.dumps(cal_res, indent=2))
