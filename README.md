Checkout Funnel Root-Cause Analysis
A data-driven root-cause analysis of an e-commerce checkout funnel (Cart → Address → Payment → Order-Confirmed). This project isolates a critical conversion drop-off, quantifies the revenue at risk, and outlines a strategic product intervention to resolve the friction point.

The Core Investigation
When top-line metrics drop, reporting the dip is only the first step. By segmenting funnel metrics across device types, date cohorts, and promotional behaviors, this analysis successfully isolates a specific 16.7-percentage-point conversion drop tied specifically to Android users attempting to apply coupons.

Rather than stopping at a chart, this project bridges data analytics and product strategy by forming a testable hypothesis about the user friction and laying out a clear validation and engineering fix plan.

Repository Structure
PRD_recommendations.md (Start Here) — The core Product Management deliverable. This document translates the data findings into actionable insights, detailing the root-cause hypothesis, validation steps, and proposed product fixes.

analysis/funnel_analysis.py — The analytical engine. It calculates overall funnel conversion, processes the segment cuts, compares before/after cohorts, estimates the overall revenue impact, and generates data visualizations.

analysis/generate_data.py — A reproducible script that generates the synthetic dataset. (An anomaly is deliberately injected into this script so the analysis has a real signal to isolate).

visuals/ — The output folder for the charts referenced in the PRD.

data/checkout_funnel_daily.csv — The underlying raw dataset.

Local Execution
To run the analysis and generate the visuals yourself, use the following terminal commands:

Bash
cd analysis
python3 generate_data.py    # Regenerates data/checkout_funnel_daily.csv
python3 funnel_analysis.py  # Prints findings to console and regenerates charts in visuals/
Note on Methodology
Because production e-commerce data is proprietary, this project utilizes a synthetically generated dataset. The generator script is included and heavily commented to maintain complete transparency regarding what is simulated input versus what is analytical output. The primary focus of this repository is to demonstrate rigorous analytical methodology, cohort
