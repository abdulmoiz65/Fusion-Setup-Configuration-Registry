# BOSS Algorithm Publication API

This reference records the request sequence implemented by
`scripts/execute.py`. It is internal implementation guidance: consultant-facing
messages remain limited to the business preview, approval, outcome, and next
action.

## Resources

```text
Provided-algorithm discovery
/api/boss/data/objects/ora/riskMgmtRisk/advancedControlsCore/v1/providedAlgorithms

Shared Algorithm Context
/api/boss/data/objects/ora/riskMgmtRisk/advancedControlsCore/v1/algorithmContexts

Access Algorithm Context
/api/boss/data/objects/ora/riskMgmtRisk/accessControls/v1/accessAlgorithmContexts

Transaction Algorithm Context
/api/boss/data/objects/ora/riskMgmtRisk/transactionControls/v1/transactionAlgorithmContexts

Effective-state verification
/api/boss/extraction/queries/ora/riskMgmtRisk/advancedControlsCore/v1/allAlgorithms
```

## Read and publication sequence

1. Discover only provided algorithms through one `GET providedAlgorithms`
   collection stream. Its process predicate contains every confirmed active
   Level 2 value, with `$limit=100` and `$sortBy=id:asc`. Locally retain only
   exact allow-listed reference codes and active Level 2 associations. This
   endpoint is read-only; no workflow step writes `providedAlgorithms`.
2. Read shared contexts plus the applicable typed contexts in grouped `id IN
   (...)` collection requests of at most 100 IDs. A `PUBLISHED` provided/base
   record, shared parent context, or typed child context is already published and
   is excluded from further publication changes. A missing unpublished context
   is created with `EXPORT_FILE`; an existing unpublished context retains its
   configured result action.
3. Read `providedAccessAlgorithms` or `providedTransactionAlgorithms` only for
   candidates whose corresponding customer context is absent. These source rows
   provide the fields needed to create that missing typed context.
4. After the business preview has been explicitly approved, issue the resource
   batches in this order, emitting and executing one Core mutation manifest at
   a time:

   - `POST accessAlgorithmContexts/$bulk` creates missing Access contexts,
     preserving the provided Access settings.
   - `POST transactionAlgorithmContexts/$bulk` creates missing Transaction
     contexts with `modeType: PUBLISHED` and `resultType: EXPORT_FILE`, or
     updates an existing eligible Transaction context with `modeType:
     PUBLISHED` only.
   - Reread the affected Access contexts and shared parent contexts. Then
     `POST algorithmContexts/$bulk` updates the Access parent contexts. For a
     newly created Access context, this request includes `modeType: PUBLISHED`
     and `resultType: EXPORT_FILE`; for an existing Access context, it includes
     `modeType: PUBLISHED` only.

   Existing-context updates include the current per-row `$context.etag`.
   The Access reread occurs after the preceding writes so the parent update uses
   a fresh change identifier and verifies that the context is still eligible to
   receive the required result action. Every batch response must contain one successful (2xx) result
   for each submitted item. Stop after any failed batch response; never retry a
   live write automatically.
5. Verify only the changed IDs through `allAlgorithms`, in grouped `id IN (...)`
   reads of at most 100 IDs. Every target must be `PUBLISHED`. A newly created
   context must also be `EXPORT_FILE`; an existing-context update accepts its
   preserved result action. If a grouped read omits an expected ID, reread that
   ID once. This verification does not discover or select user-defined
   algorithms and never repeats a bulk write.

## Read-only published inventory

The explicit published-inventory mode is separate from activation discovery and
publication. It paginates `allAlgorithms` using `$limit=100`, `$offset`, and a
stable `id:asc` order, then retains only rows whose `modeType` is `PUBLISHED`.
It is read-only, does not use the reference-code allow-list or active-process handoff,
and never prepares a mutation request.

The workflow never writes `providedAlgorithms`. Its `modeType` is not a
supported mutable field in the current business-object metadata, and effective
publication is established by the typed customer contexts above.

Do not overwrite an existing result action, including `REVIEW` or `ISSUE`. An
already published source is out of scope for mutation. A mismatch, missing
current context, failed bulk item, or failed effective-state verification is an
exception that requires a new preview and fresh approval before any later
write.
