"""
CO₂ Simulation for Sustainable Footwear Packaging
------------------------------------------------
Base model to estimate return rates, CO₂ savings, and costs
based on incentive mechanisms (deposit, bonus).
"""

import numpy as np
import pandas as pd

# Default parameters (industry-averaged)
N_TOTAL = 228_000_000  # annual packaging units
AOV = 83.33  # average order value (€)
CO2_REUSE = 0.19  # kg per reusable package
CO2_RECYCLE = 0.15  # kg per recyclable package
PROCESSING_COST = 0.20  # € per returned package

# Behavioral model coefficients (logit-based)
BASELINE_RATE = 0.333
BETA_D, BETA_B, BETA_F = 0.5, 0.2, -0.3
FRICTION = 1.0
ALPHA = np.log(BASELINE_RATE / (1 - BASELINE_RATE)) - (BETA_F * FRICTION)

def simulate(deposit=1.0, bonus=0.5, n_total=N_TOTAL):
    """Simulate packaging return system for given deposit/bonus."""
    bonus_pct = bonus / AOV
    logit = ALPHA + BETA_D * deposit + BETA_B * bonus_pct - BETA_F * FRICTION
    return_prob = 1 / (1 + np.exp(-logit))
    returned = n_total * return_prob

    reuse_prob = 0.6 + 0.10 * bonus_pct - 0.05 * FRICTION
    reuse_prob = np.clip(reuse_prob, 0, 1)

    reuse_count = returned * reuse_prob
    recycle_count = returned - reuse_count

    co2_saved = (reuse_count * CO2_REUSE + recycle_count * CO2_RECYCLE) / 1000
    bonus_payout = reuse_count * bonus
    processing = returned * PROCESSING_COST
    total_cost = bonus_payout + processing

    return {
        "deposit": deposit,
        "bonus": bonus,
        "return_rate": return_prob,
        "returned_units": returned,
        "reuse_units": reuse_count,
        "recycle_units": recycle_count,
        "co2_saved_tonnes": co2_saved,
        "total_cost_eur": total_cost,
        "co2_per_euro": co2_saved / total_cost if total_cost > 0 else 0
    }

if __name__ == "__main__":
    res = simulate(deposit=1.0, bonus=0.5)
    print("Simulation Results:", res)
