# Solar-Battery Microgrid for a Rural Health Center in Rwanda

An independent engineering project that designs and simulates a standalone solar-battery
microgrid capable of reliably powering a rural health center in Rwanda — and proves it
costs roughly **half as much as a diesel generator** over 25 years.

**Author:** Hussein NSANZIMFURA · Electrical Power Engineer · Kigali, Rwanda

---

## Problem

Many rural health centers in Rwanda lack a reliable grid connection and depend on costly,
unreliable diesel generators. Yet they run critical loads — vaccine refrigerators, lab
equipment, delivery-room lighting — that cannot lose power. This project asks: can a
solar-battery system supply such a facility reliably and affordably?

## Approach

The design followed five stages:

1. **Load assessment** — built an hourly demand profile for a typical health center.
2. **Solar resource** — pulled 19 years (2005–2023) of irradiation data from PVGIS for a
   site near Nyagatare; used the worst month (4.06 peak sun hours) as the sizing basis.
3. **Sizing** — sized the PV array, battery and inverter with standard off-grid formulas.
4. **Simulation** — an hourly energy-balance model in Python tracking battery state of charge.
5. **Economics** — levelized cost of energy vs. a diesel generator over 25 years.

## Final Design

| Component      | Specification            |
|----------------|--------------------------|
| Design load    | 20 kWh/day               |
| Solar array    | 7 kWp (13 × 550 W)       |
| Battery        | 40 kWh lithium (LiFePO₄) |
| Inverter       | 6 kW hybrid              |
| System voltage | 48 V DC                  |

## Key Results

- **Reliability:** 0 kWh unmet load — supplies the facility every hour, even in the worst
  solar month. Minimum battery state of charge: 12.3 kWh.
- **Cost:** solar LCOE **$0.364/kWh** vs. diesel **$0.727/kWh**.
- **Savings:** ≈ **$70,600** over 25 years compared with diesel.

![Combined performance](figures/combined_performance.png)

*24-hour system performance: solar generation, load, and battery state of charge.*

## Repository Contents

- `report/` — full project report (design, methodology, results, economics)
- `simulation/` — Python simulation code (runs in Google Colab, no install needed)
- `figures/` — all result graphs
- `data/` — PVGIS solar irradiation data used for sizing

## How to Run the Simulation

Open `simulation/microgrid_simulation.py` in [Google Colab](https://colab.research.google.com/drive/1W1galnXHn1LDsn8cAq_HUHb0Z3JeQ0lb?authuser=2#scrollTo=olIsurwlalDO )
or any Python environment with `numpy` and `matplotlib`, and run it top to bottom. It
reproduces the load profile, solar generation, battery simulation, and cost comparison.

## Tools

Python (NumPy, Matplotlib) · PVGIS · Google Colab

---

*This project was undertaken independently to explore a practical solution to rural
health-facility electrification in Rwanda.*
