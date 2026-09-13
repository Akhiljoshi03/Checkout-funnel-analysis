"""
Synthetic but realistic checkout funnel dataset generator.
Simulates 30 days of session-level funnel data for a fashion e-commerce app
(Cart -> Address -> Payment -> Order Confirmed), segmented by device and
discount-coupon usage, with an intentional drop-off anomaly on the Payment
step for 'coupon-applied' Android users starting Aug 10 (mirrors a real
Myntra-style bug class: coupon re-validation failing silently at the
payment gateway step).

This script is included so the dataset is fully reproducible / auditable —
a reviewer can regenerate data/checkout_funnel_daily.csv from scratch.
"""
import numpy as np
import pandas as pd

np.random.seed(42)
days = pd.date_range("2026-08-01", periods=30, freq="D")
rows = []
session_id = 100000

for day in days:
    for device in ["Android", "iOS", "Web"]:
        for coupon in [True, False]:
            base_sessions = {"Android": 4200, "iOS": 2600, "Web": 1400}[device]
            weekend_boost = 1.25 if day.dayofweek >= 5 else 1.0
            sessions = int(base_sessions * weekend_boost * np.random.uniform(0.9, 1.1))
            if coupon:
                sessions = int(sessions * 0.35)  # ~35% of sessions apply a coupon

            cart = sessions
            address_rate = np.random.uniform(0.78, 0.85)
            address = int(cart * address_rate)

            payment_rate = np.random.uniform(0.82, 0.90)
            # Injected anomaly: Android + coupon sees an extra 14-19pp drop
            # starting Aug 10 (simulating a coupon re-validation bug at payment)
            if device == "Android" and coupon and day >= pd.Timestamp("2026-08-10"):
                payment_rate -= np.random.uniform(0.14, 0.19)
                payment_rate = max(payment_rate, 0.35)
            payment = int(address * payment_rate)

            confirm_rate = np.random.uniform(0.90, 0.96)
            confirmed = int(payment * confirm_rate)

            session_id += 1
            rows.append([day.date().isoformat(), session_id, device, coupon,
                         cart, address, payment, confirmed])

df = pd.DataFrame(rows, columns=[
    "date", "session_id", "device", "coupon_applied",
    "cart_step", "address_step", "payment_step", "order_confirmed"
])
out_path = "/home/claude/myntra-pm-portfolio/01-checkout-funnel-analytics/data/checkout_funnel_daily.csv"
df.to_csv(out_path, index=False)
print(f"Wrote {len(df)} rows to {out_path}")
