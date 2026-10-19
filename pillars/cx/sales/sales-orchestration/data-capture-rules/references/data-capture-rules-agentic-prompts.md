# Data Capture Rule Agentic Authoring Prompt Examples

## Purpose

Use these examples when a user asks what they can enter in the Fusion Data
Capture Rules UI's embedded agentic authoring experience. The prompts ask the
product agent to propose a Data Capture Rule definition for the user to review.

These are UI prompt examples only. They do not authorize the FSCR skill to
create, update, activate, archive, or otherwise modify a Data Capture Rule
through BOSS, REST, Data Loader, or another integration.

## Prompt Emission Rules

- Use business context supplied by the user when it is available.
- When context is missing, choose realistic synthetic values for the sales
  scenario, source interactions, and opportunity attributes.
- Emit every prompt as standalone, copy-ready text. Never emit a prompt that
  requires the user to replace a placeholder, blank, generic stand-in, or
  bracketed value.
- Keep synthetic scenarios free of real customer names, tenant details, and
  confidential configuration.
- Put each emitted prompt in its own fenced text block. Any explanation that
  values are synthetic belongs outside the prompt.
- Even when the user requests a reusable template, return one or more fully
  populated examples and offer to generate another concrete scenario instead
  of emitting placeholders.
- Keep prompt guidance at the UI-text level. Do not turn it into a Data Capture
  Rule blueprint, API payload, project artifact, or live operation.

## Sample Prompts

1. Capture BANT details for enterprise software opportunities from customer
   emails, discovery-call notes, and meeting summaries. Capture the confirmed
   budget, decision authority, business need, purchasing timeline, buying
   process, and deal risks. Keep Budget Amount, Decision Level, Close Date, Win
   Probability, and Comments current when the source interaction provides new
   evidence.
2. Capture customer pain points, business requirements, solution fit, expected
   deal value, target close date, and competitive information for cloud
   financial management opportunities. Keep Expected Revenue, Close Date,
   Opportunity Type, Status, Win Probability, and Comments aligned with the
   latest customer interactions.
3. Capture forecasting changes for subscription-renewal opportunities from
   seller call notes and customer emails. Detect revised purchasing dates,
   changes in expected revenue, confidence signals, risks, and next-step
   commitments. Keep Close Date, Expected Revenue, Forecast Category, Win
   Probability, Status, and Comments current.
4. Capture competitive signals for cybersecurity software opportunities from
   discovery calls, demonstrations, and follow-up emails. Record the named
   competitors, customer evaluation criteria, solution strengths, objections,
   commercial concerns, and decision timing. Keep Win Probability, Close Date,
   Status, and Comments aligned with the latest evidence.
5. Capture executive sponsorship and decision-process information for
   industrial equipment opportunities from meeting summaries and account-team
   notes. Record the economic buyer, technical approvers, procurement contacts,
   available budget, approval sequence, target purchase date, and unresolved
   risks. Keep Decision Level, Budget Amount, Close Date, and Comments current.

## Source

- Oracle Fusion Cloud Sales, *Before You Start*, Data Capture section:
  https://docs.oracle.com/en/cloud/saas/sales/gsaso/befoer-you-start.html#Data-Capture
- Source accessed: 2026-08-10.
