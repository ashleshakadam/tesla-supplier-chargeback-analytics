"""
Tesla SOS — Supplier Chargeback Intelligence System
Stage 3: Apply chargeback logic, false positive suppression, dispute tracking
Output: data/shipment_events.csv (updated with 6 new columns)
"""

import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

# Conditions under which a chargeback is suppressed — supplier not at fault
FP_RULES = {
    "ASN_LATE":      "EDI_System_Delay",
    "ASN_MISSING":   "Supplier_Portal_Outage",
    "PKG_DEVIATION": "Pre_Approved_Alternate",
    "QTY_MISMATCH":  "Transit_Damage",
    "OTIF_MISS":     "Weather_Force_Majeure",
    "LABEL_ERROR":   "Label_Reprinted_Before_Scan",
    "PO_VIOLATION":  "Tesla_Emergency_Reroute",
    "SHORTSHIP":     "Authorized_Split_Shipment",
}

# Low-risk suppliers get more benefit of the doubt
FP_PROB = {
    "Low":    0.25,
    "Medium": 0.20,
    "High":   0.12,
}


def detect_false_positive(row):
    if not row["has_violation"]:
        return False, None
    fp_prob = FP_PROB[row["risk_profile"]]
    if random.random() < fp_prob:
        return True, FP_RULES[row["violation_type"]]
    return False, None


def assign_dispute(row):
    if not row["chargeback_issued"]:
        return False, "N/A", row["penalty_usd"]
    if random.random() < 0.28:
        status = random.choices(
            ["Upheld", "Reversed", "Partial_Credit", "Pending"],
            weights=[0.52, 0.22, 0.16, 0.10]
        )[0]
        if status == "Reversed":
            adjusted = 0.0
        elif status == "Partial_Credit":
            adjusted = round(row["penalty_usd"] * 0.50, 2)
        else:
            adjusted = row["penalty_usd"]
        return True, status, adjusted
    return False, "N/A", row["penalty_usd"]


if __name__ == "__main__":
    print("Stage 3 — Applying chargeback logic...")
    df = pd.read_csv("data/shipment_events.csv")

    # False positive detection
    fp_results = df.apply(detect_false_positive, axis=1)
    df["is_false_positive"]     = [r[0] for r in fp_results]
    df["fp_suppression_reason"] = [r[1] for r in fp_results]
    df["chargeback_issued"]     = df["has_violation"] & ~df["is_false_positive"]
    df.loc[df["is_false_positive"], "penalty_usd"] = 0.0

    # Dispute tracking
    dispute_results = df.apply(assign_dispute, axis=1)
    df["dispute_raised"]    = [r[0] for r in dispute_results]
    df["dispute_status"]    = [r[1] for r in dispute_results]
    df["final_penalty_usd"] = [r[2] for r in dispute_results]

    df.to_csv("data/shipment_events.csv", index=False)

    total_violations  = df["has_violation"].sum()
    total_fp          = df["is_false_positive"].sum()
    total_chargebacks = df["chargeback_issued"].sum()
    total_penalty     = df["final_penalty_usd"].sum()

    print(f"  Total violations    : {total_violations:,}")
    print(f"  False positives     : {total_fp:,}  ({total_fp/total_violations:.1%} suppressed)")
    print(f"  Chargebacks issued  : {total_chargebacks:,}")
    print(f"  Disputes tracked    : {df['dispute_raised'].sum():,}")
    print(f"  Final penalty value : ${total_penalty:,.0f}")
    print(f"  Columns             : {df.shape[1]}")
    print("  Saved to data/shipment_events.csv")