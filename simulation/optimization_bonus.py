"""
Bonus Optimization
------------------
Optimize bonus value (0.5–2.0 EUR) to maximize CO₂ saved per € spent.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from co2_simulation import simulate, N_TOTAL

bonus_range = np.arange(0.5, 2.01, 0.05)
results = []

for b in bonus_range:
    res = simulate(deposit=1.0, bonus=b, n_total=N_TOTAL)
    res["bonus_eur"] = b
    results.append(res)

df = pd.DataFrame(results)
df.to_csv("bonus_optimization.csv", index=False)

# Find best bonus
best = df.loc[df["co2_per_euro"].idxmax()]
print("Best bonus setting:\n", best)

# Plot
plt.plot(df["bonus_eur"], df["co2_per_euro"], marker="o")
plt.xlabel("Bonus (€)")
plt.ylabel("CO₂ saved per €")
plt.title("Optimization: Bonus vs CO₂ per €")
plt.savefig("bonus_optimization.png", bbox_inches="tight")
