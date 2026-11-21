# User stories and acceptance criteria
Format: *As a [user], I want [capability], so that [benefit].* Priority uses MoSCoW. Suggested Jira epics: **Order Capture**, **Approvals**, **Visibility & Reporting**.

## Epic: Order Capture
**US-01 (Must) - Capture order once**
As a customer service agent, I want to enter an order once, so that I do not have to re-key it in other systems.
- Given a new order is saved, when I submit it, then it appears in the warehouse and finance views without further entry.
- Given required fields are missing, when I submit, then the system blocks submission and highlights the fields.

**US-02 (Must) - Real-time stock check**
As a customer service agent, I want to see stock availability while entering an order, so that I can confirm delivery dates immediately.
- Given I add a product, when stock is below the ordered quantity, then a warning and the expected restock date are shown.
- Stock data is no more than 5 minutes old.

## Epic: Approvals
**US-03 (Must) - Auto-approval**
As an operations manager, I want low-value orders approved automatically, so that my team spends time only on exceptions.
- Given an order below the configured limit and a passed payment check, then its status becomes *Approved* without manual action.

**US-04 (Must) - Approval workflow with SLA**
As an approver, I want orders above the limit routed to me with a reminder, so that no order waits more than 4 hours.
- Given an order above the limit, then I receive a notification within 1 minute.
- Given the order is unapproved after 4 hours, then it escalates to the Operations Manager.

## Epic: Visibility & Reporting
**US-05 (Should) - Customer status updates**
As a customer, I want automatic confirmation and dispatch messages, so that I do not need to call to check my order.
- Given an order status changes to Confirmed or Dispatched, then the customer receives an email within 5 minutes.

**US-06 (Should) - Operations dashboard**
As an operations manager, I want a dashboard of order volume, backlog and cycle time, so that I can spot delays early.
- The dashboard shows today's orders, orders waiting > 24h, and average cycle time, refreshed at least hourly.

**US-07 (Must) - Audit trail**
As a finance manager, I want every order status change logged with user and time, so that I can audit disputes.
- Given any status change, then a record with user ID, timestamp, old and new status is stored and cannot be edited.
