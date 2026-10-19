# Manage SMS Configuration Reference Lookups

The supported parent-row FSM import contract does not require a live lookup. Public Oracle documentation is returned for provider-setup guidance and for failed or unknown outcomes; it does not replace the FSM import, process-status, or manual activation workflow.

## Public Oracle Documentation

| Topic | Public Oracle Document | Coverage |
|---|---|---|
| SMS campaign configuration | [Configure SMS for Campaigns](https://docs.oracle.com/en/cloud/saas/human-resources/fauat/configure-sms-for-campaigns.html) | Public setup guidance for SMS campaigns; it does not confirm a provider import, process outcome, activation state, or exactly-one-active verification |

## Documentation Rules

| Situation | What Happens |
|---|---|
| Provider setup guidance is requested | Return Configure SMS for Campaigns and state its coverage |
| Import fails, times out, or has an unknown outcome | Return Configure SMS for Campaigns with the process status and safe next action; do not treat the document as evidence of import completion |
| Activation is incomplete | Return Configure SMS for Campaigns with the manual activation handoff; do not rerun the provider import automatically |
