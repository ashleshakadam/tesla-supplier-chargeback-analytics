# SOS Supplier Chargeback Intelligence System

## Business Problem:
Supplier non-compliance and chargeback disputes cause revenue leakage and operational inefficiencies.

## Solution:
Built an end-to-end chargeback analytics system tracking supplier performance, compliance, disputes, and penalties.
Tableau Public: https://public.tableau.com/newWorkbook/dda1abd7-82d9-4afd-8041-96250f4861b9#1

### Impact:
• Identified high-risk suppliers contributing to ~40% of penalties  
• Reduced false-positive disputes via validation logic  
• Enabled regional and supplier-level accountability

### Tech Stack:
• SQL: Chargeback logic, joins, aggregations
• Python: Data simulation, preprocessing
• Tableau: KPI dashboards
• Data Model: Supplier, PO, Receiving, Violations

### Key Logic Built:
• Chargeback detection (ASN mismatch, packaging, quantity issues)
• Dispute validation logic
• KPI calculations (OTIF, Compliance %, Dispute Rate)

### Pipeline Flow:
Raw Data → Cleaned → Chargeback Logic → KPI Layer → Dashboard

## Key numbers:
- 8,000 shipment events simulated across 15 months
- 8 violation types: ASN errors, packaging deviations, OTIF misses, quantity mismatches
- False positive suppression engine — 20% of flagged events correctly suppressed
- Composite risk score per supplier using OTIF, ASN accuracy and compliance rate
- 4 Tableau-ready datasets powering 5 dashboard views

## How to run:
pip install pandas numpy jupyter
jupyter notebook
Run notebooks in order: 01 → 02 → 03 → 04

## Files:
data/supplier_master.csv       — 120 suppliers
data/shipment_events.csv       — 8,000 events with chargeback flags
data/supplier_scorecards.csv   — KPI rollup per supplier
data/monthly_trends.csv        — violation trends by month
data/dispute_summary.csv       — dispute resolution tracking
data/regional_summary.csv      — NA vs EMEA comparison
