# Supplier Chargeback Analytics

## Overview
A supply chain analytics project that models supplier non-compliance, chargeback exposure, and recoverable cost leakage using integrated operational data.

The project is structured around the type of workflow a manufacturing or logistics analytics team would use to validate chargeback logic, prioritize supplier risk, and support cross-functional reviews.

## Business Problem
Supplier non-compliance can create measurable downstream cost through delivery misses, receiving mismatches, quality issues, and process rework. In many organizations, the underlying evidence is scattered across ERP, manufacturing, and warehouse systems, making recovery inconsistent and labor-intensive.

The challenge is not only identifying chargeback candidates, but also building a defensible analytical framework that ties operational events to financial impact.

## Solution
This project integrates SAP receiving data, MES defect signals, and WMS process records to construct a supplier performance and chargeback analytics layer.

It supports:
- supplier-level non-compliance monitoring
- chargeback candidate identification
- dispute-ready evidence trails
- KPI dashboards for supplier reviews and operational escalation

<img width="1367" height="734" alt="image" src="https://github.com/user-attachments/assets/d0a58a9e-8ae3-4f71-9c37-fa00ed0a96b1" />

#### Tableau URL: https://public.tableau.com/app/profile/ashlesha.sanjay.kadam/viz/TeslaSOS-SupplierChargebackComplianceIntelligence/TeslaSOS-SupplierChargebackComplianceIntelligence2

## Architecture
The repository combines data preparation, analytical logic, and dashboard outputs:

- `data/` stores source tables and prepared inputs
- `notebooks/` contains staged analysis for supplier master logic, PO-receiving integration, chargeback logic, and KPI analysis
- `src/` contains reusable business logic and transformations
- `tableau/` contains dashboard assets or references

## Methodology

### Data Integration
Merged supplier, purchase order, receiving, warehouse, and defect records into a unified analytical model.

### Chargeback Logic
Defined rule-based logic to identify recoverable events tied to non-compliance patterns.

### Performance Analytics
Calculated KPIs across suppliers, parts, and fulfillment events to surface recurring loss drivers.

### Dashboarding
Developed Tableau views to support operational reviews, exception analysis, and prioritization.

## Results
Representative outcomes from this analytical design include:
- clear identification of high-risk suppliers and repeat failure modes
- improved ability to connect operational exceptions to financial recovery logic
- a repeatable framework for supplier chargeback review and escalation

## Tech Stack
SQL, Python, Tableau

## Repository Structure
```text
tesla-supplier-chargeback-analytics/
├── data/
├── notebooks/
├── src/
├── tableau/
└── README.md
```

## How to Use
	1.	prepare source datasets in the data/ directory
	2.	execute notebook or script logic in sequence
	3.	generate curated outputs for dashboard consumption
	4.	publish or review KPI summaries in Tableau

## Future Improvements
	•	productionize the pipeline with scheduled refreshes
	•	add supplier segmentation and risk scoring
	•	incorporate dispute status and recovery realization tracking
	•	formalize dimensional modeling for scale

## Author
Ashlesha Kadam
