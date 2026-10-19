# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Constrain scope | Use only IRC_OFFERS_DFF and the exact requested global, context, or context-sensitive target |
| 2 | Validate export-backed contract | Do not select sequences, columns, values, or CSV fields from inference |
| 3 | Preserve unrelated configuration | Change only requested rows and fields; retain metadata, translations, ordering, encoding, quoting, line endings, and unrelated members |
| 4 | Validate candidate and import instruction | Retain the exact candidate ZIP and target state; an original request that explicitly directs import authorizes that same-run candidate |
| 5 | Separate deployment | Reconcile import before separately approving a manual deployment path |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Blocker | resolve_dff_export_model | Target task is not IRC_OFFERS_DFF or requested identity is ambiguous | Stop rather than substitute a generic DFF task | No |
| Create or Update | Blocker | resolve_dff_export_model | Fresh export does not prove CSV fields, keys, row relationships, sequence availability, or storage-column availability | Use complete fresh-export evidence | No |
| Create | Blocker | resolve_dff_export_model | Exact technical identity already exists | Return ALREADY_EXISTS | No |
| Update | Blocker | resolve_dff_export_model | Exact technical identity is missing, duplicated, protected, or non-editable | Return NOT_FOUND, AMBIGUOUS_TARGET, or PROTECTED_DEFINITION | No |
| Value-set change | Blocker | resolve_value_set_authority | Value set is missing, ambiguous, incompatible, or only a display label | Require exact approved identifier and compatibility | No |
| Before Import | Blocker | | The original request does not explicitly direct import to the selected target environment, or the validated candidate is stale | Stop before upload; require a new import request or regenerate the candidate | No |
| Deploy or Offer-page visibility | Blocker | | Deployment route is unproven or TDS scope is not separately approved | Return MANUAL_INTERVENTION_REQUIRED | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_dff_export_model | Every configuration operation | Export-backed package contract and exact target identity | ora_reference_lookups.md |
| resolve_value_set_authority | A value set or LOV is supplied | Exact approved identifier and compatibility | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IRC_OFFER_DFF.ENFORCE_DESIGN | step | 60 | design_enforcement | enforced->IRC_OFFER_DFF.READINESS_GATE;blocked->IRC_OFFER_DFF.HANDLE_ISSUE | IRC_OFFER_DFF.APPLY_DEFAULTS | stop | Before package preparation, import, deployment, or verification |

## Constant text default update

From the fresh verified baseline, resolve exactly one global SegmentCode. Require
ReadOnlyFlag N and existing DefaultType CONSTANT. For the verified 100 Characters
value set, validate the supplied text length and controls under input validation.
Replace only that row's DefaultValue. Preserve DefaultType, value set, every other
field and every other archive member. If already equal, return NO_CHANGE without
an import. Do not convert another default mode as part of this one-field request.

## Context-sensitive character segment creation

Require one existing enabled context and a new SegmentCode within it. Require a
unique SegmentIdentifier, unused sequence within that context, and an explicitly
selected compatible column. A column used by any global segment is unavailable to
every context; a column used in the selected context is unavailable there. Reuse
across different non-global contexts is permitted by this ownership check. Report
the owning segment on a collision. Never silently substitute a column or move an
existing segment; a corrected column must be supplied or accepted by the user.

Use the exact exported ValueSetCode and compatible presentation authority described
in reference lookups. Append only one row to ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_SEGMENT.csv using
the baseline's original headers and field order. Set the DFF/application parent keys
to IRC_OFFERS_DFF/821 and the context parent key to the exact selected ContextCode.
Set SegmentCode, SegmentIdentifier, ColumnName, SequenceNumber and ValueSetCode to
the resolved inputs. Apply only the new-row defaults from defaulting rules. Do not
clone a peer's identity, defaults, business behavior or audit fields. Preserve all
existing rows and metadata, and do not create or change the value set itself.

## Candidate preservation and Task Hook

Prepare a new candidate path; never overwrite the baseline or an existing preview.
Validate the final archive through the shared setup-data/reference validators and
core Data Loader's normal validation and Task Hook before approval and upload.

| Operation | Required comparison against the exact completed baseline |
|---|---|
| Both | Valid CRCs; same member names/order/comment and archive metadata; byte-identical unrelated members; unchanged CSV headers, encoding, quoting and line endings; exact task/environment/DFF identity |
| Constant default | Same rows, keys and order; exactly one requested DefaultValue cell changes and every other field remains unchanged; preserve bytes outside that cell |
| Context segment | Original segment CSV bytes remain an unchanged prefix; exactly one appended row with the resolved inputs and documented defaults; all other members byte-identical |

Parse CSV with its quoting rules, including quoted multiline values; do not use
line-based replacement. Check the final candidate, not just the planned delta.
Bind findings and before/after values to its SHA-256 in the Task Hook immutable
preview. Internal validate_import uses existing artifacts only and never repeats
export, calls the loader recursively or submits a load. A changed candidate requires
fresh validation and approval under the core Data Loader workflow.

After import, inspect the detailed FSM outcome and fresh-export the definition.
Confirm requested values and preservation of every pre-existing business field;
server-maintained audit timestamps may differ. Import does not deploy the flexfield
or change Transaction Design Studio visibility.
