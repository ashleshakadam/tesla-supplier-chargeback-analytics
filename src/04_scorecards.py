"""
Tesla SOS — Supplier Chargeback Intelligence System
Stage 4: Build supplier scorecards, risk scores, and Tableau export tables
Outputs:
  data/supplier_scorecards.csv
  data/monthly_trends.csv
  data/dispute_summary.csv
  data/regional_summary.csv
"""

import pandas as pd
import numpy as np
import os


def build_scorecard(df_events, df_suppliers):
    grp = df_events.groupby("supplier_id")

    total_shipments    = grp.size().rename("total_shipments")
    total_violations   = grp["has_violation"].sum().rename("total_violations")
    chargebacks_issued = grp["chargeback_issued"].sum().rename("chargebacks_issued")
    false_positives    = grp["is_false_positive"].sum().rename("false_positives_suppressed")
    total_penalty      = grp["final_penalty_usd"].sum().rename("total_penalty_usd")
    disputes_raised    = grp["dispute_raised"].sum().rename("disputes_raised")

    df_events["on_time_in_full"] = ~(
        (df_events["violation_type"] == "OTIF_MISS") &
        df_events["chargeback_issued"]
    )
    df_events["asn_ok"] = (
        ~df_events["violation_type"].isin(["ASN_LATE", "ASN_MISSING"])
        | df_events["is_false_positive"]
    )

    otif_rate = grp["on_time_in_full"].mean().rename("otif_rate")
    asn_rate  = grp["asn_ok"].mean().rename("asn_accuracy_rate")

    scorecard = pd.concat([
        total_shipments, total_violations, chargebacks_issued,
        false_positives, total_penalty, disputes_raised,
        otif_rate, asn_rate
    ], axis=1).reset_index()

    scorecard = scorecard.merge(
        df_suppliers[[
            "supplier_id", "supplier_name", "tier", "part_category",
            "region", "primary_plant", "contract_value_usd", "risk_profile"
        ]],
        on="supplier_id"
    )

    scorecard["compliance_rate"]    = round(1 - (scorecard["chargebacks_issued"] / scorecard["total_shipments"]), 4)
    scorecard["fp_suppression_rate"]= round(scorecard["false_positives_suppressed"] / scorecard["total_violations"].clip(lower=1), 4)
    scorecard["otif_rate"]          = round(scorecard["otif_rate"], 4)
    scorecard["asn_accuracy_rate"]  = round(scorecard["asn_accuracy_rate"], 4)
    scorecard["total_penalty_usd"]  = round(scorecard["total_penalty_usd"], 2)

    def pct_rank(s):
        return s.rank(pct=True) * 100

    scorecard["risk_score"] = round(
        pct_rank(1 - scorecard["compliance_rate"])    * 0.40 +
        pct_rank(1 - scorecard["otif_rate"])           * 0.30 +
        pct_rank(1 - scorecard["asn_accuracy_rate"])   * 0.20 +
        pct_rank(1 - scorecard["fp_suppression_rate"]) * 0.10,
        1
    )

    scorecard["risk_tier"] = pd.cut(
        scorecard["risk_score"],
        bins=[-1, 25, 50, 75, 101],
        labels=["Green — Low Risk", "Amber — Watch",
                "Orange — At Risk", "Red — Critical"]
    )

    return scorecard


def build_monthly_trends(df_events):
    return df_events.groupby(["ship_month", "violation_type"]).agg(
        shipments       =("shipment_id",       "count"),
        chargebacks     =("chargeback_issued",  "sum"),
        penalty_usd     =("final_penalty_usd",  "sum"),
        false_positives =("is_false_positive",  "sum")
    ).reset_index()


def build_dispute_summary(df_events):
    return (
        df_events[df_events["dispute_raised"]]
        .groupby(["region", "violation_type", "dispute_status"])
        .agg(count=("shipment_id", "count"), total_penalty=("final_penalty_usd", "sum"))
        .reset_index()
    )


def build_regional_summary(scorecard):
    return scorecard.groupby("region").agg(
        suppliers          =("supplier_id",      "count"),
        avg_compliance     =("compliance_rate",   "mean"),
        avg_otif           =("otif_rate",         "mean"),
        total_penalty_usd  =("total_penalty_usd", "sum"),
        critical_suppliers =("risk_tier", lambda x: (x == "Red — Critical").sum())
    ).reset_index()


if __name__ == "__main__":
    print("Stage 4 — Building scorecards and export tables...")

    df_events    = pd.read_csv("data/shipment_events.csv")
    df_suppliers = pd.read_csv("data/supplier_master.csv")

    scorecard       = build_scorecard(df_events, df_suppliers)
    monthly_trends  = build_monthly_trends(df_events)
    dispute_summary = build_dispute_summary(df_events)
    regional_summary= build_regional_summary(scorecard)

    os.makedirs("data", exist_ok=True)
    scorecard.to_csv("data/supplier_scorecards.csv",  index=False)
    monthly_trends.to_csv("data/monthly_trends.csv",  index=False)
    dispute_summary.to_csv("data/dispute_summary.csv",index=False)
    regional_summary.to_csv("data/regional_summary.csv", index=False)

    print(f"  Scorecards          : {scorecard.shape}")
    print(f"  Monthly trends      : {monthly_trends.shape}")
    print(f"  Dispute summary     : {dispute_summary.shape}")
    print(f"  Regional summary    : {regional_summary.shape}")
    print(f"\n  === FINAL NUMBERS ===")
    print(f"  Suppliers analyzed  : {len(scorecard)}")
    print(f"  Shipment events     : {len(df_events):,}")
    print(f"  Violations detected : {int(df_events['has_violation'].sum()):,}")
    print(f"  False positives     : {int(df_events['is_false_positive'].sum()):,}")
    print(f"  Chargebacks issued  : {int(df_events['chargeback_issued'].sum()):,}")
    print(f"  Penalty recovered   : ${df_events['final_penalty_usd'].sum():,.0f}")
    print(f"  Disputes tracked    : {int(df_events['dispute_raised'].sum()):,}")
    print(f"  Critical suppliers  : {(scorecard['risk_tier']=='Red — Critical').sum()}")
    print(f"\n  All files saved to data/")