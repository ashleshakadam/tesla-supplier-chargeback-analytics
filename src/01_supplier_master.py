"""
Tesla SOS — Supplier Chargeback Intelligence System
Stage 1: Generate supplier master data
Output: data/supplier_master.csv
"""

import pandas as pd
import numpy as np
import random
import os

np.random.seed(42)
random.seed(42)

REGIONS        = ["NA-West", "NA-East", "NA-Central", "EMEA-Europe", "APAC-China"]
REGION_WEIGHTS = [0.28, 0.22, 0.18, 0.20, 0.12]

TIERS        = ["Tier 1", "Tier 2", "Tier 3"]
TIER_WEIGHTS = [0.50, 0.35, 0.15]

PART_CATEGORIES = [
    "Battery Systems", "Powertrain", "Electronics",
    "Interior", "Chassis & Frame", "Thermal Management",
    "Fasteners", "Exterior Panels"
]

RISK_PROFILES   = ["Low", "Medium", "High"]
RISK_WEIGHTS    = [0.40, 0.40, 0.20]

PLANTS = {
    "NA-West":     "Giga Fremont",
    "NA-East":     "Giga New York",
    "NA-Central":  "Giga Texas",
    "EMEA-Europe": "Giga Berlin",
    "APAC-China":  "Giga Shanghai",
}


def generate_suppliers():
    rows = []
    for i in range(1, 121):
        region = np.random.choice(REGIONS, p=REGION_WEIGHTS)
        tier   = np.random.choice(TIERS,   p=TIER_WEIGHTS)
        rows.append({
            "supplier_id":        f"SUPP_{str(i).zfill(3)}",
            "supplier_name":      f"Supplier_{str(i).zfill(3)}",
            "region":             region,
            "primary_plant":      PLANTS[region],
            "tier":               tier,
            "part_category":      np.random.choice(PART_CATEGORIES),
            "risk_profile":       np.random.choice(RISK_PROFILES, p=RISK_WEIGHTS),
            "contract_value_usd": random.randint(500_000, 50_000_000),
            "active_parts":       random.randint(5, 180),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print("Stage 1 — Generating supplier master...")
    df = generate_suppliers()

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/supplier_master.csv", index=False)

    print(f"  Suppliers generated : {len(df)}")
    print(f"  Tier distribution   :\n{df['tier'].value_counts().to_string()}")
    print(f"  Region distribution :\n{df['region'].value_counts().to_string()}")
    print(f"  Risk distribution   :\n{df['risk_profile'].value_counts().to_string()}")
    print(f"  Nulls               : {df.isnull().sum().sum()}")
    print("  Saved to data/supplier_master.csv")