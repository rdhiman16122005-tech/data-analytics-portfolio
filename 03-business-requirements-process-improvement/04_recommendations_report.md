# Recommendations report

## Summary
Manual re-keying, email-based stock checks and approvals are the main causes of slow order processing.
Moving to a single order-capture flow with automated stock checks, rule-based approval and customer notifications is
expected to meet objectives O1-O4 in the BRD (targets are assumptions to be validated).

## Recommendations
| # | Recommendation | Addresses | Effort | Benefit |
|---|---|---|---|---|
| 1 | Capture each order once and integrate with warehouse and finance systems | BR-01, BR-08 | High | Removes errors and rework |
| 2 | Real-time stock check at order entry | BR-02 | Medium | Faster, accurate promises to customers |
| 3 | Auto-approve low-value orders, route the rest with an SLA | BR-03 | Low | Cuts approval waiting time |
| 4 | Automated customer status messages | BR-04 | Low | Fewer "where is my order?" contacts |
| 5 | Operations dashboard for cycle time and backlog | BR-05 | Medium | Continuous improvement |

## Roadmap
1. **Phase 1 (quick wins):** auto-approval rules, status notifications, approval SLA reminders.
2. **Phase 2:** real-time stock integration and single order capture.
3. **Phase 3:** operations dashboard and KPI reporting.

## Measuring success
Track the KPIs in the BRD monthly in Excel or Power BI and compare with the baseline before go-live.
