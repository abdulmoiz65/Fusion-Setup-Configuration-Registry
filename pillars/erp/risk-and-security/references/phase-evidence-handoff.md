# Phase Evidence Handoff

## Purpose

Use this internal, child-local record to retain completed same-environment
evidence when the durable project workflow later invokes that same child again.
It is evidence only: the router and durable workflow select, sequence, pause,
and resume child workflows. It is not a consultant artifact or a Run Book.

Save it under the producing child’s existing current artifact directory, for
example:

```text
project/{project_id}/artifacts/pillars/erp/risk-and-security/{functional-area}/{task}/current/phase-evidence-handoff.md
```

## Required record

Record only redacted references and timings:

| Field | Record |
| --- | --- |
| Producing child | The child skill ID and local phase that produced the evidence |
| Environment | The verified target environment |
| Evidence lifecycle | `read-only complete`, `decision pending`, `approved preflight`, `completed`, or `blocked` |
| Completed evidence | Artifact references for the completed same-environment reads and their inputs |
| Next local requirement | The next dependent read, approval, verification, or consultant decision for this child |
| Timing | Phase start/end, Core-operation elapsed time, and workflow elapsed time |

Do not store credentials, tokens, raw request bodies, internal identifiers, or
consultant-visible wording in this record.

## Reuse rules

The durable workflow may provide this evidence to the same child only when the
project, target environment, child, and referenced inputs still match. The
child may reuse completed read-only evidence only through its immediate
continuation or approval path. Replace the record and repeat the affected
preflight when the environment or source input changes, the consultant requests
a restart, a previous mutation changes the relevant state, or the next live
action requires its declared fresh verification.

An evidence handoff never selects the next child, bypasses an approval,
mutation preflight, post-change verification, or required child ordering. While
a child has a pending consultant decision, the durable workflow must keep that
child active and return only that child’s decision table.
