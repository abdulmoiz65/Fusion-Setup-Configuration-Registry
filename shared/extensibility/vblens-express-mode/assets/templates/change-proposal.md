# Express Mode change proposal

This proposal is the authoritative Assess-to-Implement handoff. Include every
implementation fact needed by a later turn; do not rely on hidden reasoning or
an uncited feasibility conclusion.

## Implementation plan

Keep this detailed plan in the internal handoff. Show it to the user only when
technical file details are requested.

| Action | Exact repository-relative file | Planned content |
| --- | --- | --- |
| Create / Update |  |  |
| Create when page preparation is required | `extension1/sources/ui/<owner>/applications/<application>/flows/<flow>/pages/<page>-page-x.json` | Standard VB Studio page overlay and primary deployment target |
| Create when page preparation is required | `extension1/sources/ui/<owner>/applications/<application>/flows/<flow>/pages/<page>-page-x.js` | Standard empty customer page module |

- Directory impact: create missing layout/module directories or reuse existing
  directories.
- Rule/module relationship: identify the Business Rules import when a module is
  required; otherwise state that no import is added.
- Validation after editing: exact static validator inputs and scenario checks.
- Deployment handoff: Build a fresh `.vx`, deploy it once, and derive the
  snapshot URL without opening it.
- Deployment target kind: `Extension page artifact` or `Redwood route`.
- Deployment target value: exact repository-relative page file and the complete
  supplied `/fscmUI/redwood/...` URL, including query parameters and fragment.
- Deployment target evidence: record how page source, app-info, or the supplied
  URL proves the target. Create the page-preparation pair only when deployed
  source proves the exact owner/application/flow/page; otherwise use the
  complete supplied URL and do not invent a page overlay. Never drop business
  parameters when both a page artifact and supplied URL are available.

Compact user-facing projection example:

```text
Implementation plan
- Apply the selected rule behavior.

How to test
- Positive: <applicable case and expected result>.
- Negative: <applicable case and expected result>.

- I'll apply and validate the change, then give you a <page name> link so you
  can verify it.
- After you finish testing, `COMMIT` will create the reviewed commit.
```

## Proposal identity

- Proposal ID:
- Status: awaiting approval / approved / invalidated / implemented
- User request:
- Complete supplied target URL:
- Deployment target kind and exact value:
- Deployment target evidence:
- Evidence manifest and deployed versions:
- Repository HEAD and relevant source fingerprints:

## Business behavior

- Current behavior:
- Proposed behavior:
- User-visible result:
- Supported/setup-dependent/unresolved conclusion:
- Material evidence supporting that conclusion:


## Repository context

- Express artifact: Business Rules / Advanced Expression / Page Properties
- Working branch, internal:
- Starting commit:
- Integration base:
- Target page:
- Extension topology:
- Read/write policy:
- Available verification depth:
- Exact owner and layout:
- Oracle counterpart citation:

## Proposed Express configuration

- Identifier:
- Label:
- Status and order:
- Condition:
- Actions:
- Messages:
- Referenced fields:
- Advanced Expressions:
- Complete inline expression or complete commented module code:
- Page Properties and FA counterpart:
- Read-and-preserve artifacts:

## Detailed intended file changes

| File | Change | Reason |
| --- | --- | --- |
|  |  |  |

## Prerequisites and risks

- Blocking unresolved facts:
- Non-blocking runtime verification:
- Facts that would invalidate this proposal:

## Verification plan

- Static checks:
- Project-tooling checks:
- Scenario checks:
- Audit/build checks:
- Runtime checks:

## How to test

- Positive test cases and expected results:
- Negative test cases and expected results:
- Relevant regression cases and expected results:
- Test steps or commands, when technical details were requested:

## Scenario contract

- Blank/null:
- Invalid or nonnumeric:
- Unchanged:
- Below boundary:
- At boundary:
- Above boundary:
- Setup missing or duplicate, when applicable:

## Approval

- Change approved by:
- Approval context:
- Approval scope: implementation / validation / fresh Build / one-shot Fusion
  Deploy
- Approval phrase: `IMPLEMENT`
- Git approval: only a later message beginning with `COMMIT` authorizes commit.
