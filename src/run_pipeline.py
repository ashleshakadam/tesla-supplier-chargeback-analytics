"""
Tesla SOS Supplier Chargeback Intelligence System
Run this file to execute the complete data pipeline.
Usage: python src/run_pipeline.py
"""

import subprocess
import sys

scripts = [
    "src/01_supplier_master.py",
    "src/02_shipment_events.py",
    "src/03_chargeback_logic.py",
    "src/04_scorecards.py",
]

for script in scripts:
    print(f"\n{'='*50}")
    print(f"Running {script}...")
    print('='*50)
    result = subprocess.run([sys.executable, script], check=True)

print("\n Pipeline complete. All CSVs saved to data/")
print(" Load supplier_scorecards.csv into Tableau to refresh the dashboard.")