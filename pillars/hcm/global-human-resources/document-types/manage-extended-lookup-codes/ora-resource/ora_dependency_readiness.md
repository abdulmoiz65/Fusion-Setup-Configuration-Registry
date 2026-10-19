# Manage Extended Lookup Codes Dependency Readiness

## Purpose

Defines the conditional parent and target references used by Manage Extended
Lookup Codes. The task resolves existing setup only when applicable and never
creates a missing parent lookup implicitly.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Extended lookup-code identity | Resolve the current target or confirm that the proposed create identity is available |
| 2 | Parent lookup scope | Resolve one enabled current parent lookup in the selected scope |
| 3 | Create source identity | For a base create, establish one complete validated caller-owned or deterministic FDOS source-key pair |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| extended_lookup_identity | Existing extended lookup code or create-availability evidence | Conditional | Read, edit, delete, or create duplicate check | Lookup | Extended Lookup Codes resource | find_extended_lookup_codes | Prevents an ambiguous target or duplicate create | Provide one exact lookup type, code, and applicable scope | Resolved lookup-code identity and current values |
| parent_lookup_scope | Enabled parent lookup | Conditional | Create, edit, or delete requires parent scope | Lookup | Current parent lookup configuration | resolve_extended_lookup_parent_scope | Keeps the child code within one exact enabled parent scope | Provide one exact parent lookup and scope | Parent lookup identity and scope |
| source_key_identity | Unique base-create loader identity | Yes | A base ExtendedLookupCode create is prepared | Satisfied | Complete validated caller pair, or deterministic FDOS generation from the resolved business key |  | Prevents Fusion from rejecting the MERGE because no unique record reference is present | Supply both source-key values or allow the FDOS pair to be generated and shown in preview | SourceSystemOwner and SourceSystemId |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every applicable dependency has exact authoritative evidence | No |
| Lookup | A documented resolver can resolve an applicable dependency | Read-only lookup only |
| Verify | Existing evidence must be confirmed without creating setup | No |
| Not Applicable | A dependency condition is false | No |
| Needs Input | A required selector or scope value is missing | No |
| Unresolved | Resolution returns no match, multiple matches, unavailable evidence, or an incompatible value | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| XLOOK.DEPENDENCY | decision | 2 | resolve_dependency | ready->XLOOK.READ;not_required->XLOOK.READ;needs_input->XLOOK.ERROR;unresolved->XLOOK.ERROR | XLOOK.VALIDATE | stop | After input validation and before task-local reference lookups |
