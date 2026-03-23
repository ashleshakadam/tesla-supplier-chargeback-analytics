# SOS Supplier Chargeback Intelligence System

Tableau Public: https://public.tableau.com/newWorkbook/dda1abd7-82d9-4afd-8041-96250f4861b9#1

## What this is
An end-to-end supplier chargeback program built in Python — covering
logic design, false positive suppression, dispute tracking, and supplier
risk scoring across 120 suppliers in NA and EMEA.

## Key numbers
- 8,000 shipment events simulated across 15 months
- 8 violation types: ASN errors, packaging deviations, OTIF misses, quantity mismatches
- False positive suppression engine — 20% of flagged events correctly suppressed
- Composite risk score per supplier using OTIF, ASN accuracy and compliance rate
- 4 Tableau-ready datasets powering 5 dashboard views

## How to run
pip install pandas numpy jupyter
jupyter notebook
Run notebooks in order: 01 → 02 → 03 → 04

## Files
data/supplier_master.csv       — 120 suppliers
data/shipment_events.csv       — 8,000 events with chargeback flags
data/supplier_scorecards.csv   — KPI rollup per supplier
data/monthly_trends.csv        — violation trends by month
data/dispute_summary.csv       — dispute resolution tracking
data/regional_summary.csv      — NA vs EMEA comparison