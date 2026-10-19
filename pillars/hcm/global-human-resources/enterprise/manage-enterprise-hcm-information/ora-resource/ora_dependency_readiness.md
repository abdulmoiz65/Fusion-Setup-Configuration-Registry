# Manage Enterprise HCM Information Dependency Readiness

## Purpose

Defines the conditional Enterprise parent and EFF context references used by
Manage Enterprise HCM Information. The task resolves existing context only for
the requested operation and never invents a parent, classification, or segment.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Enterprise parent | Resolve one effective Enterprise and its current values |
| 2 | Delete history | Resolve the current row against complete Enterprise history for delete |
| 3 | Enterprise classification | Resolve the ENTERPRISE classification envelope when an OrgInformation row is requested |
| 4 | Enterprise EFF context | Resolve the requested context and segment against the current describe contract |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| enterprise_parent | Effective Enterprise parent | Conditional | Enterprise HCM information is read or changed | Lookup | Enterprise resource | find_enterprise | Establishes the exact parent and effective row | Provide one precise Enterprise selector and effective date when required | OrganizationId and current effective values |
| enterprise_delete_history | Complete Enterprise history | Conditional | Date-effective delete | Lookup | hcmDateEffectiveObjectHistory | resolve_enterprise_delete_history | Protects the first date-effective row | Confirm the displayed eligible current row | Selected row effective range and internal eligibility |
| enterprise_classification | ENTERPRISE classification envelope | Conditional | An OrgInformation EFF row is requested | Lookup | Returned enterpriseEFF envelope | resolve_enterprise_classification | Keeps OrgInformation data under the correct classification parent | Do not supply or guess a classification identifier | OrgUnitClassificationId, CategoryCode ENTERPRISE, and effective values |
| enterprise_eff_context | Enterprise EFF context and segment | Conditional | A context or business segment is requested | Lookup | Current Enterprise polymorphic describe and returned context child | resolve_enterprise_context | Prevents a segment from being placed in the wrong context or row | Provide the requested context or business segment | Context contract, OrgInformationId, effective range, SequenceNumber, and current values |

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
| ENT.DEPENDENCIES | decision | 8 | resolve_dependency | ready->ENT.DEFAULTS;not_required->ENT.DEFAULTS;needs_input->ENT.ERROR;unresolved->ENT.ERROR | ENT.VALUESET | stop | After Enterprise, delete-history, and requested EFF lookups and before defaulting |
