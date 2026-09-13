"""
Checkout Funnel Root-Cause Analysis
------------------------------------
Goal: identify WHERE and WHY conversion is leaking in the Cart -> Address ->
Payment -> Order Confirmed funnel, segmented by device and coupon usage,
and quantify the revenue impact of the worst-performing segment.

This mirrors the 'Analytics' work stream in the JD: dig into product data,
run root-cause analysis on friction points, and tie findings to KPIs.
"""
import pandas as pd
import matplotlib.pyplot as plt

DATA = "/home/claude/myntra-pm-portfolio/01-checkout-funnel-analytics/data/checkout_funnel_daily.csv"
OUT = "/home/claude/myntra-pm-portfolio/01-checkout-funnel-analytics/visuals"

df = pd.read_csv(DATA, parse_dates=["date"])

# ---- 1. Overall funnel conversion (last 30 days) ----
overall = df[["cart_step", "address_step", "payment_step", "order_confirmed"]].sum()
overall_rates = (overall / overall["cart_step"] * 100).round(1)
print("=== Overall funnel conversion (Cart = 100%) ===")
print(overall_rates, "\n")

# ---- 2. Step-over-step drop-off by device x coupon segment ----
df["addr_to_pay_rate"] = df["payment_step"] / df["address_step"]
seg = df.groupby(["device", "coupon_applied"])["addr_to_pay_rate"].mean().round(3) * 100
print("=== Address -> Payment conversion by segment (avg, %) ===")
print(seg.sort_values(), "\n")

# ---- 3. Isolate the worst segment: Android + coupon, before vs after Aug 10 ----
mask = (df["device"] == "Android") & (df["coupon_applied"] == True)
android_coupon = df[mask].copy()
android_coupon["period"] = android_coupon["date"].apply(
    lambda d: "Before Aug 10" if d < pd.Timestamp("2026-08-10") else "From Aug 10"
)
before_after = android_coupon.groupby("period")["addr_to_pay_rate"].mean().round(3) * 100
print("=== Android + Coupon: Address->Payment rate, before vs after Aug 10 ===")
print(before_after, "\n")

drop_pp = before_after["Before Aug 10"] - before_after["From Aug 10"]
print(f"Anomaly size: {drop_pp:.1f} percentage-point drop, isolated to Android + coupon-applied sessions.\n")

# ---- 4. Revenue impact estimate ----
AOV = 1450  # assumed average order value (INR) for illustration
lost_sessions_per_day = android_coupon[android_coupon["date"] >= "2026-08-10"].apply(
    lambda r: r["address_step"] * (drop_pp / 100), axis=1
).mean()
daily_revenue_loss = lost_sessions_per_day * AOV
print(f"Estimated lost orders/day in this segment: {lost_sessions_per_day:.0f}")
print(f"Estimated daily revenue at risk: Rs. {daily_revenue_loss:,.0f}")
print(f"Estimated revenue at risk over 20 affected days: Rs. {daily_revenue_loss*20:,.0f}\n")

# ---- Chart 1: Overall funnel ----
fig, ax = plt.subplots(figsize=(7, 4.5))
steps = ["Cart", "Address", "Payment", "Confirmed"]
vals = overall_rates.values
ax.bar(steps, vals, color=["#E23744", "#F2994A", "#F2C94C", "#27AE60"])
for i, v in enumerate(vals):
    ax.text(i, v + 1.5, f"{v}%", ha="center", fontweight="bold")
ax.set_ylim(0, 110)
ax.set_ylabel("% of Cart sessions reaching this step")
ax.set_title("Overall Checkout Funnel (Aug 2026, 30-day window)")
plt.tight_layout()
plt.savefig(f"{OUT}/01_overall_funnel.png", dpi=150)
plt.close()

# ---- Chart 2: Address->Payment rate by segment ----
seg_df = seg.reset_index()
seg_df["label"] = seg_df["device"] + " | " + seg_df["coupon_applied"].map({True: "Coupon", False: "No Coupon"})
seg_df = seg_df.sort_values("addr_to_pay_rate")
fig, ax = plt.subplots(figsize=(8, 4.5))
colors = ["#E23744" if "Android | Coupon" in l else "#BDBDBD" for l in seg_df["label"]]
ax.barh(seg_df["label"], seg_df["addr_to_pay_rate"], color=colors)
ax.set_xlabel("Address -> Payment conversion (%)")
ax.set_title("Payment-step conversion by device x coupon segment")
plt.tight_layout()
plt.savefig(f"{OUT}/02_segment_conversion.png", dpi=150)
plt.close()

# ---- Chart 3: Android+Coupon trend over time, showing the break point ----
daily_trend = android_coupon.groupby("date")["addr_to_pay_rate"].mean() * 100
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(daily_trend.index, daily_trend.values, marker="o", color="#E23744")
ax.axvline(pd.Timestamp("2026-08-10"), color="black", linestyle="--", linewidth=1)
ax.text(pd.Timestamp("2026-08-10"), daily_trend.min() - 3, "Aug 10\n(coupon re-validation\nregression suspected)",
        fontsize=8, ha="center")
ax.set_ylabel("Address -> Payment conversion (%)")
ax.set_title("Android + Coupon segment: daily payment-step conversion")
plt.tight_layout()
plt.savefig(f"{OUT}/03_android_coupon_trend.png", dpi=150)
plt.close()

print("Charts saved to", OUT)
