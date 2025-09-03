"""
Sensitivity Analysis
--------------------
Sweep over deposit (€0.5–2.0) and bonus (% of AOV),
record return rates, CO₂ saved, and costs.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from co2_simulation import simulate, N_TOTAL

deposits = [0.5, 1.0, 2.0]
bonus_percents = [0.0, 0.05, 0.10, 0.15]

records = []
for d in deposits:
    for bp in bonus_percents:
        bonus_eur = bp * 83.33
        res = simulate(deposit=d, bonus=bonus_eur, n_total=N_TOTAL)
        records.append(res)

df = pd.DataFrame(records)
df.to_csv("sensitivity_results.csv", index=False)

# Plot: CO₂ saved vs Total cost
plt.scatter(df["total_cost_eur"], df["co2_saved_tonnes"], c=df["deposit"], cmap="viridis", s=100)
plt.xlabel("Total Cost (€)")
plt.ylabel("CO₂ Saved (tonnes)")
plt.title("Sensitivity: Deposit & Bonus Impact")
plt.colorbar(label="Deposit (€)")
plt.savefig("sensitivity_plot.png", bbox_inches="tight")
print("Saved results to sensitivity_results.csv and sensitivity_plot.png")
