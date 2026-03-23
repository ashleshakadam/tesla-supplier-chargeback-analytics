# Tesla SOS — Supplier Chargeback & Compliance Intelligence

An end-to-end supply chain analytics project that models supplier non-compliance, chargeback exposure, dispute outcomes, and regional performance using Python, SQL, and Tableau.

This project was designed as a decision-support system for a Supplier Operations Support (SOS) function. It combines chargeback rule logic, KPI modeling, dispute analysis, and executive reporting to surface high-risk suppliers, validate penalty programs, and improve operational accountability across North America and EMEA.

---

## Problem Statement

Supplier chargeback programs are often operationally noisy: non-compliance events are distributed across suppliers, regions, and violation types; dispute outcomes can obscure true root causes; and leadership frequently lacks a unified view of chargeback exposure, compliance trends, and supplier performance.

The objective of this project is to build an analytical system that answers four questions:

1. Which suppliers drive the largest share of chargeback exposure?
2. Where are compliance and OTIF performance deteriorating?
3. How effective is current dispute handling?
4. Which suppliers should be prioritized for operational intervention?

---

## Solution Overview

The project implements a lightweight analytics pipeline that:

- integrates supplier, purchase order, receiving, and violation data,
- applies chargeback logic to quantify penalty exposure,
- computes KPI layers for compliance, OTIF, disputes, and supplier risk,
- and presents the results through an executive Tableau dashboard.

The output is a business-facing analytics artifact that supports chargeback validation, supplier monitoring, and regional performance management.

---

## Repository Structure

```text
01_supplier_master.ipynb      # Supplier master preparation and reference data
02_po_receiving.ipynb         # PO / receiving integration and operational data prep
03_chargeback_logic.ipynb     # Chargeback rule logic and penalty attribution
04_kpi_analysis.ipynb         # KPI computation, trend analysis, and dashboard-ready outputs
README.md
