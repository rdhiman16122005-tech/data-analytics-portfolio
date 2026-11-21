# Business Requirements Document (BRD)
**Project:** Order Processing Improvement - *RetailCo (fictional)*
**Prepared by:** Riya Dhiman | **Version:** 1.0 | **Status:** Draft for stakeholder review

## 1. Business problem
Customer orders are processed through several disconnected steps (email, spreadsheets and a legacy order system).
Orders are re-keyed by hand, stock is checked manually and approvals wait in inboxes. This causes slow dispatch, errors
and customer complaints.

## 2. Objectives (SMART)
| # | Objective | Measure |
|---|---|---|
| O1 | Reduce average order-to-dispatch time | From 48h to under 24h *(assumption)* |
| O2 | Reduce order-entry errors | From 6% to under 2% of orders *(assumption)* |
| O3 | Increase orders processed per agent per day | +30% *(assumption)* |
| O4 | Improve on-time delivery | From 85% to 95% *(assumption)* |

## 3. Scope
**In scope:** order capture, payment check, stock check, approval, picking/packing hand-off, order status updates to customers.
**Out of scope:** product sourcing, returns processing, finance system replacement.

## 4. Stakeholders
| Stakeholder | Role | Interest | Influence |
|---|---|---|---|
| Operations Manager | Sponsor | Faster, cheaper fulfilment | High |
| Customer Service Team | Users | Fewer complaints, visible order status | Medium |
| Warehouse Supervisor | Users | Accurate pick lists | Medium |
| Finance Manager | Approver | Correct invoicing and payment checks | Medium |
| IT Team | Delivery | Integration, security, support | High |
| Customers | End users | Fast, accurate delivery | High |

## 5. Business requirements
| ID | Requirement | Priority |
|---|---|---|
| BR-01 | Orders are captured once and flow automatically to all downstream steps (no re-keying) | Must |
| BR-02 | System checks stock availability in real time at order entry | Must |
| BR-03 | Orders under a set value are auto-approved, others route to an approver with a 4-hour SLA | Must |
| BR-04 | Customers receive automatic order confirmation and status updates | Should |
| BR-05 | Managers can view a dashboard of order volume, backlog and cycle time | Should |
| BR-06 | Audit trail of every order status change | Must |
| BR-07 | Role-based access to order data | Must |
| BR-08 | Integration with the existing payment and warehouse systems | Must |

## 6. Non-functional requirements
Performance (order entry < 3 seconds), availability (99.5% in business hours), security (GDPR-compliant handling of customer data), usability (new agents productive within one day of training).

## 7. KPIs
Order cycle time - Order error rate - Orders per agent per day - On-time delivery % - Customer complaints per 1,000 orders.

## 8. Assumptions, constraints, risks
| Type | Item | Mitigation |
|---|---|---|
| Assumption | Warehouse system exposes an API | Confirm with IT in discovery |
| Constraint | Budget and timeline set by the sponsor | Phase delivery (MVP first) |
| Risk | Staff resistance to change | Early involvement, training, super-users |
| Risk | Data migration errors | Parallel run and reconciliation |

## 9. Acceptance and sign-off
Requirements are accepted when UAT passes against the acceptance criteria in `03_user_stories.md` and sign-off is given by the Operations Manager and Finance Manager.
