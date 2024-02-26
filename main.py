# main.py

import subprocess

# Step 1: Run scrape_currency_data.py
print("Running scrape_currency_data.py...")
subprocess.run(["python", "scrape_currency_data.py"], check=True)

# Step 2: Run technical_analysis.py
print("\nRunning technical_analysis.py...")
subprocess.run(["python", "technical_analysis.py"], check=True)

# Step 3: Run decision.py
print("\nRunning decision.py...")
subprocess.run(["python", "decision.py"], check=True)

print("\nAll scripts executed successfully.")
