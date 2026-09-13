# PRD: Fixing the Android + Coupon Payment-Step Leak
**Checkout Funnel Root-Cause Analysis — Storefront / Customer Experience**

Author: [Your Name] · Focus Area: Storefront Product (Customer Experience)
Status: Draft for review · Related work stream: Analytics + Problem Solving

---

## 1. Problem Statement
Over a 30-day window, the overall Cart → Order-Confirmed funnel converts at
**64.0%**, with the single biggest leak at the Address → Payment step
(81.1% → 68.8%, a 12.3pp drop across all users).

Segmenting by device and coupon usage isolates something more specific:
**Android users who apply a coupon convert from Address to Payment at only
74.3% on average — the worst segment by a wide margin** — and a day-by-day
trend shows this wasn't always true. Conversion for this segment held
steady around **86%** through Aug 1–9, then fell to **~69%** from Aug 10
onward, a **16.7 percentage-point drop with no equivalent movement in any
other segment**.

That pattern (segment-specific, date-bound, isolated to one platform) is a
strong regression signature — not organic user behavior drift.

## 2. Why This Matters (Impact)
| Metric | Value |
|---|---|
| Affected segment | Android + coupon-applied sessions |
| Conversion drop | 16.7 pp (86.0% → 69.3%) |
| Estimated lost orders/day | ~214 |
| Estimated daily revenue at risk (AOV ₹1,450) | ~₹3.1 lakh |
| Estimated revenue at risk over 20 days | ~₹62 lakh |

*(AOV and exact rupee figures are illustrative — the methodology is what a
reviewer should evaluate; swap in real AOV for the true number.)*

## 3. Hypothesis
The timing and specificity (Android-only, coupon-only) point toward a
**coupon re-validation failure at the payment gateway step on Android** —
e.g., a client-side SDK update or a server-side promo-validation service
change shipped around Aug 10 that silently fails re-validation when the
user reaches the payment screen with a coupon already applied in cart,
causing a subset of users to hit an error state or unresponsive "Pay Now"
button and abandon.

This is a *hypothesis to validate*, not a confirmed root cause — see
Section 5.

## 4. Recommendation
1. **Immediate (this week):** Pull payment-step error logs and client crash
   reports filtered to Android + coupon-applied, Aug 10 onward. Confirm
   whether error rate / latency spiked on that date.
2. **Fast validation:** Ship a feature-flagged fix path (fall back to
   re-fetching the coupon validation on payment-page load instead of trusting
   cached cart state) to 10% of affected traffic; measure lift in
   Address→Payment conversion within 48 hours.
3. **Fix:** If confirmed, work with Engineering to patch the coupon
   revalidation call and add a payment-step monitoring alert keyed on
   segment-level conversion (device x coupon), not just aggregate funnel
   conversion — this is exactly the kind of localized regression that
   aggregate dashboards hide.
4. **Guardrail:** Add this segment cut (device x promo-applied) as a
   standing dashboard tile so a 15+ pp swing triggers an automatic Slack
   alert to the Storefront pod.

## 5. What I'd Validate Before Committing Engineering Time
- Confirm no confound: was there an Android app release on/around Aug 10?
  (Check release notes / Play Store rollout logs.)
- Confirm the drop isn't a tracking artifact (e.g., a new SDK version
  double-firing or dropping `payment_step` events for a subset of devices).
- Cross-check with customer support ticket volume/CSAT for the same window
  — a real payment failure should show up as an uptick in "payment not
  going through" tickets from Android users.

## 6. Success Metric
Address → Payment conversion for Android + coupon-applied sessions returns
to the **~85–86% baseline** within one week of the fix shipping, with no
regression in other segments.

---
## Appendix: Methodology
- Dataset: 30 days of daily, segment-level funnel counts (device x
  coupon-applied) — see `data/checkout_funnel_daily.csv`.
- Note: this dataset is **synthetically generated** (see
  `analysis/generate_data.py`) to demonstrate the analysis approach, with a
  deliberate anomaly injected so the root-cause workflow can be shown
  end-to-end. In a real setting this would be pulled from the events
  warehouse (e.g., via SQL against a checkout events table).
- Analysis code: `analysis/funnel_analysis.py` — reproducible, no manual
  steps.
- Charts: `visuals/01_overall_funnel.png`, `02_segment_conversion.png`,
  `03_android_coupon_trend.png`.
