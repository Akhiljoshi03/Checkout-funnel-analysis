# Project 1 — Checkout Funnel Root-Cause Analysis
**Work streams demonstrated:** Analytics, Problem Solving
**Focus area:** Storefront Product (Customer Experience)

## What this is
A funnel analysis of the Cart → Address → Payment → Order-Confirmed flow,
segmented by device and coupon usage, that isolates a specific
16.7-percentage-point conversion drop in one segment (Android + coupon
users, starting a specific date), quantifies the revenue at risk, forms a
testable hypothesis about the cause, and lays out a validation + fix plan.

This is the kind of "why did a number move and what do we do about it"
exercise a PM does weekly — not just a chart, but a decision.

## Why this project for this JD
The JD's Analytics stream asks for exactly this: "dig deep into product
data to understand user behaviour, run root-cause analysis on friction
points... track KPIs for feature success." This project shows the full
loop — data → segment cut → hypothesis → validation plan → success metric
— rather than stopping at "here's a chart."

## How to read this project
1. Start with **`PRD_recommendations.md`** — the actual PM deliverable.
2. `analysis/generate_data.py` — reproducibly generates the sample dataset
   (synthetic, with a deliberately injected anomaly so the analysis has a
   real signal to find — see note on synthetic data below).
3. `analysis/funnel_analysis.py` — the analysis: overall funnel, segment
   cuts, before/after comparison, revenue-impact estimate, and chart
   generation.
4. `visuals/` — the three charts referenced in the PRD.
5. `data/checkout_funnel_daily.csv` — the underlying dataset.

## Run it yourself
```bash
cd analysis
python3 generate_data.py     # regenerates data/checkout_funnel_daily.csv
python3 funnel_analysis.py   # prints findings, regenerates visuals/
```

## Note on data
This uses a synthetically generated dataset (not real Myntra data) because
production analytics data isn't publicly available. The generator script
is included and commented so it's fully transparent what's real analysis
vs. what's simulated input — the value being demonstrated is the analysis
methodology and PM judgment, not the specific numbers.
