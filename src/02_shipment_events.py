"""
Tesla SOS — Supplier Chargeback Intelligence System
Stage 2: Generate shipment events with violation flags
Output: data/shipment_events.csv
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

np.random.seed(42)
random.seed(42)

N_EVENTS   = 8000
START_DATE = datetime(2024, 1, 1)
END_DATE   = datetime(2025, 3, 31)

VIOLATION_TYPES = [
    "ASN_LATE", "ASN_MISSING", "PKG_DEVIATION",
    "QTY_MISMATCH", "OTIF_MISS", "LABEL_ERROR",
    "PO_VIOLATION", "SHORTSHIP"
]

PENALTY_RULES = {
    "ASN_LATE":      ("flat", 150,  800),
    "ASN_MISSING":   ("flat", 400, 2000),
    "PKG_DEVIATION": ("flat", 200, 1500),
    "QTY_MISMATCH":  ("pct",  0.03, 0.08),
    "OTIF_MISS":     ("pct",  0.02, 0.05),
    "LABEL_ERROR":   ("flat", 100,  600),
    "PO_VIOLATION":  ("flat", 300, 2500),
    "SHORTSHIP":     ("pct",  0.05, 0.12),
}

VIOLATION_PROB = {
    "Low":    0.06,
    "Medium": 0.15,
    "High":   0.30,
}


def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def calculate_penalty(violation_type, po_value):
    rule = PENALTY_RULES[violation_type]
    if rule[0] == "flat":
        return round(random.uniform(rule[1], rule[2]), 2)
    else:
        return round(po_value * random.uniform(rule[1], rule[2]), 2)


def generate_events(df_suppliers):
    events = []
    for _ in range(N_EVENTS):
        supplier       = df_suppliers.sample(1).iloc[0]
        ship_date      = random_date(START_DATE, END_DATE)
        po_value       = random.randint(8_000, 450_000)
        qty_ordered    = random.randint(50, 5000)
        violation_prob = VIOLATION_PROB[supplier["risk_profile"]]
        has_violation  = random.random() < violation_prob

        violation_type = None
        penalty_usd    = 0.0

        if has_violation:
            violation_type = random.choice(VIOLATION_TYPES)
            penalty_usd    = calculate_penalty(violation_type, po_value)

        events.append({
            "shipment_id":    f"SHP-{random.randint(100000, 999999)}",
            "supplier_id":    supplier["supplier_id"],
            "supplier_name":  supplier["supplier_name"],
            "region":         supplier["region"],
            "primary_plant":  supplier["primary_plant"],
            "tier":           supplier["tier"],
            "part_category":  supplier["part_category"],
            "risk_profile":   supplier["risk_profile"],
            "ship_date":      ship_date.strftime("%Y-%m-%d"),
            "ship_month":     ship_date.strftime("%Y-%m"),
            "ship_quarter":   f"Q{(ship_date.month-1)//3+1} {ship_date.year}",
            "po_value_usd":   po_value,
            "qty_ordered":    qty_ordered,
            "has_violation":  has_violation,
            "violation_type": violation_type if has_violation else "NONE",
            "penalty_usd":    penalty_usd,
        })
    return pd.DataFrame(events)


if __name__ == "__main__":
    print("Stage 2 — Generating shipment events...")
    df_suppliers = pd.read_csv("data/supplier_master.csv")
    df_events    = generate_events(df_suppliers)

    os.makedirs("data", exist_ok=True)
    df_events.to_csv("data/shipment_events.csv", index=False)

    total_violations = df_events["has_violation"].sum()
    total_penalty    = df_events["penalty_usd"].sum()

    print(f"  Shipment events     : {len(df_events):,}")
    print(f"  Total violations    : {total_violations:,}")
    print(f"  Violation rate      : {total_violations/len(df_events):.1%}")
    print(f"  Total penalty value : ${total_penalty:,.0f}")
    print(f"  Violation breakdown :\n{df_events[df_events['has_violation']]['violation_type'].value_counts().to_string()}")
    print("  Saved to data/shipment_events.csv")