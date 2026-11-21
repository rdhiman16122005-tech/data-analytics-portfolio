# Process flows: AS-IS vs TO-BE

## AS-IS (current process)
```mermaid
flowchart TD
    A[Customer order by email / phone] --> B[Agent re-keys order into spreadsheet]
    B --> C[Agent emails warehouse to check stock]
    C --> D{Stock available?}
    D -- No --> E[Agent emails customer, order waits]
    D -- Yes --> F[Order sent to manager for approval by email]
    F --> G[Manager approves, often next day]
    G --> H[Agent re-keys order into legacy system]
    H --> I[Warehouse picks and packs]
    I --> J[Dispatch, agent updates customer manually]
```

## TO-BE (proposed process)
```mermaid
flowchart TD
    A[Customer order via web form / agent screen] --> B[Order captured once in order system]
    B --> C[Automatic real-time stock check]
    C --> D{Stock available?}
    D -- No --> E[Automatic backorder notice with ETA]
    D -- Yes --> F{Order value under limit?}
    F -- Yes --> G[Auto-approve]
    F -- No --> H[Routed to approver with 4h SLA alert]
    G --> I[Pick list sent to warehouse automatically]
    H --> I
    I --> J[Dispatch and automatic customer status update]
```

## Bottleneck analysis
| Bottleneck | Cause | Impact | Fix in TO-BE |
|---|---|---|---|
| Manual re-keying (2x) | Disconnected tools | Errors, wasted time | Single capture, system integration |
| Stock check by email | No shared inventory view | Delay of hours | Real-time stock lookup |
| Approval by email | No routing or SLA | Orders wait overnight | Auto-approval rules + workflow with SLA |
| Manual customer updates | No notifications | Calls and complaints | Automated status messages |
