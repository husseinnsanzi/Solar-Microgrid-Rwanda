"""
Solar-Battery Microgrid Simulation for a Rural Health Center in Rwanda
Author: Hussein NSANZIMFURA

Hourly energy-balance model:
  - Builds the health-center load profile
  - Models 7 kWp solar generation (worst-month sizing basis)
  - Simulates a 40 kWh lithium battery, tracking state of charge
  - Runs an economic comparison against a diesel generator

Runs in Google Colab or any Python environment with numpy + matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt

hours = np.arange(24)

# ---------------------------------------------------------------
# 1. LOAD PROFILE (kW per hour, 00:00 -> 23:00)
# ---------------------------------------------------------------
load_kW = np.array([
    0.5, 0.5, 0.5, 0.5, 0.5, 0.5,   # night base load
    0.8, 1.0, 1.2, 1.3, 1.4, 1.3,   # morning ramp-up
    1.0, 1.2, 1.3, 1.2, 1.0, 0.9,   # afternoon
    1.0, 1.0, 0.9, 0.7, 0.6, 0.5    # evening wind-down
])
daily_energy = load_kW.sum()
print("Total daily load =", round(daily_energy, 1), "kWh")
print("Peak load        =", load_kW.max(), "kW")

# ---------------------------------------------------------------
# 2. SOLAR GENERATION
# ---------------------------------------------------------------
pv_size_kWp = 7.0     # array size
PR          = 0.75    # performance ratio (real-world losses)
PSH_worst   = 4.06    # worst-month peak sun hours (PVGIS, Nyagatare)

pv_daily_energy = pv_size_kWp * PSH_worst * PR
print("PV daily energy  =", round(pv_daily_energy, 1), "kWh")

solar_shape = np.array([
    0, 0, 0, 0, 0, 0,
    0.1, 0.3, 0.6, 0.8, 0.95, 1.0,
    1.0, 0.95, 0.8, 0.6, 0.3, 0.1,
    0, 0, 0, 0, 0, 0
])
solar_kW = solar_shape / solar_shape.sum() * pv_daily_energy

# ---------------------------------------------------------------
# 3. BATTERY SIMULATION (energy balance)
# ---------------------------------------------------------------
battery_capacity = 40.0            # kWh, lithium
DoD    = 0.8                       # usable depth of discharge
usable = battery_capacity * DoD    # kWh actually usable
eff    = 0.95                      # round-trip efficiency

soc          = np.zeros(24)
grid_deficit = np.zeros(24)
soc_prev     = usable * 0.5        # start half full

for h in range(24):
    net = solar_kW[h] - load_kW[h]
    if net >= 0:
        soc_now = min(soc_prev + net * eff, usable)
    else:
        soc_now = soc_prev + net
        if soc_now < 0:
            grid_deficit[h] = -soc_now
            soc_now = 0
    soc[h] = soc_now
    soc_prev = soc_now

print("Minimum SOC      =", round(soc.min(), 1), "kWh")
print("Total unmet load =", round(grid_deficit.sum(), 2), "kWh")

# ---------------------------------------------------------------
# 4. PLOTS
# ---------------------------------------------------------------
plt.figure(figsize=(9, 4))
plt.bar(hours, load_kW, color="steelblue")
plt.xlabel("Hour of day"); plt.ylabel("Load (kW)")
plt.title("Rural Health Center - Daily Load Profile")
plt.xticks(hours); plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout(); plt.savefig("load_profile.png", dpi=130); plt.show()

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(hours, load_kW, color="steelblue", alpha=0.7, label="Load (kW)")
ax1.plot(hours, solar_kW, color="orange", marker="o", linewidth=2, label="Solar (kW)")
ax1.set_xlabel("Hour of day"); ax1.set_ylabel("Power (kW)"); ax1.set_xticks(hours)
ax2 = ax1.twinx()
ax2.plot(hours, soc, color="green", marker="s", linewidth=2, label="Battery SOC (kWh)")
ax2.set_ylabel("Battery charge (kWh)")
l1, lab1 = ax1.get_legend_handles_labels()
l2, lab2 = ax2.get_legend_handles_labels()
ax1.legend(l1 + l2, lab1 + lab2, loc="upper center", ncol=3)
plt.title("Solar-Battery Microgrid - 24 Hour Performance")
plt.tight_layout(); plt.savefig("combined_performance.png", dpi=130); plt.show()

# ---------------------------------------------------------------
# 5. ECONOMIC ANALYSIS
# ---------------------------------------------------------------
price_pv_per_kWp   = 900
price_batt_per_kWh = 400
price_inverter     = 1500
price_bos          = 2000

capex = (pv_size_kWp * price_pv_per_kWp + battery_capacity * price_batt_per_kWh
         + price_inverter + price_bos)

project_life  = 25
batt_replace  = 2 * (battery_capacity * price_batt_per_kWh)
om_total      = 0.02 * capex * project_life
lifetime_cost = capex + batt_replace + om_total
lifetime_energy = daily_energy * 365 * project_life
lcoe = lifetime_cost / lifetime_energy

# Diesel comparison
diesel_price_per_L = 1.60
fuel_per_kWh       = 0.35
genset_cost        = 4000
annual_energy      = daily_energy * 365
fuel_cost_life     = annual_energy * fuel_per_kWh * diesel_price_per_L * project_life
genset_cost_life   = (project_life // 5) * genset_cost
genset_om_life     = 500 * project_life
diesel_lifetime    = fuel_cost_life + genset_cost_life + genset_om_life
diesel_lcoe        = diesel_lifetime / lifetime_energy

print("\n--- Economics ---")
print("Total CAPEX          : $", round(capex))
print("Solar LCOE           : $", round(lcoe, 3), "/kWh")
print("Diesel LCOE          : $", round(diesel_lcoe, 3), "/kWh")
print("Savings over 25 years: $", round(diesel_lifetime - lifetime_cost))

plt.figure(figsize=(7, 5))
plt.bar(["Solar-Battery", "Diesel Generator"], [lifetime_cost, diesel_lifetime],
        color=["green", "gray"])
plt.ylabel("Lifetime cost (USD)")
plt.title("25-Year Cost: Solar-Battery vs Diesel")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout(); plt.savefig("cost_comparison.png", dpi=130); plt.show()
