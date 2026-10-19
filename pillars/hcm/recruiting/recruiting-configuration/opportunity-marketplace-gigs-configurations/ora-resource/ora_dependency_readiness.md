# Opportunity Marketplace Gigs Configurations Dependency Readiness

Source: Opportunity Marketplace Gigs Configurations SKILL.md and FSCR — Opportunity Marketplace Gigs Configuration.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Current Gig Configuration export | Export the current task package before reference or identity validation. |
| 2 | Reference values | Resolve the eligibility profile or list unused profiles for selection, then resolve every supplied availability-context value. |
| 3 | Current configuration identity | Check the retained code and eligibility profile, then derive the next sequence from the fresh export. |
| 4 | Candidate package | Derive the candidate archive from the fresh export, preserve its proven structure, and generate new availability-context identifiers for every new context and supplied child filter. |
| 5 | Immutable tabular preview and approval | Complete preflight, present all candidate rows in clear tables, and obtain exact approval before core.data-loader import. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| current_gig_configuration_export | Current Gig Configuration FSM export | Yes | Creating a Gig Configuration | Verify | Fresh export for task ORA_IRC_MP_SITE_GIG_CONFIGURATION | verify_fresh_gig_configuration_export | Supplies current codes, assigned profiles, metadata, member order, and parent-child references | Export current task data; do not use a stale or hand-built package | Current rows, package members, metadata member, parent-child references |
| copy_source_configuration | Source Gig Configuration, user-supplied eligibility profile, and confirmed or supplied identity | Yes | Copying a Gig Configuration | Verify and lookup | Fresh export source row, supplied EligibilityName, and optional SiteCode and SiteName | derive_copy_identity_and_filters | Copy creation must state that Configuration code, Configuration name, and eligibility profile are mandatory, display the missing-identity proposal, and obtain approval of the derived `_copy` identity when both fields are omitted, or use both requester-supplied values, without reusing source eligibility or technical identifiers | Display `Since Configuration code and Configuration name values are not provided. Configuration code, Configuration name, and eligibility profile are mandatory to create a Gig configuration. I am proposing the following values: <source_code>_copy and <source_name>_copy.` Approve those values or provide both replacements; provide an active unused eligibility profile | Confirmed or supplied SiteCode and SiteName; supplied EligibilityName; copied business filters |
| active_eligibility_profile | Active unused Opportunity Marketplace eligibility profile | Yes | A selected EligibilityName is supplied | Lookup | Supplied or user-selected EligibilityName | resolve_active_opp_marketplace_eligibility_profile | A configuration is segmented by its eligibility profile and that profile cannot already be assigned | Provide or select an active unused Opportunity Marketplace eligibility-profile name | EligibilityName |
| unused_eligibility_profile_inventory | Active unused Opportunity Marketplace eligibility profiles | Conditional | EligibilityName is omitted or already assigned in the fresh Gig export | Lookup | Fresh Gig export and target environment | list_active_unused_opp_marketplace_eligibility_profiles | The user needs an eligible profile selection before package generation | Select one profile from the returned list | Active unused EligibilityName options |
| availability_context_references | Optional location, organization, job family, and job function | Conditional | One or more availability-context values are supplied | Lookup | Supplied availability-context value and fresh task export | | All supplied filters must resolve exactly before package generation. A location also needs a proven geography-element hierarchy tuple. | Correct each value that has no exact eligible match or is ambiguous; stop when location hierarchy serialization cannot be proven. | Validated availability-context values and, for locations, element value/language pairs |
| new_availability_context_identifiers | New parent and child availability-context identifiers | Conditional | A new availability context or child filter row is added | Generate and verify | Secure 16-byte random values encoded as 32 uppercase hexadecimal characters | generate_new_gig_availability_context_identifiers | The FSM import requires nonblank IDs, while copied IDs can conflict with target-pod records | Do not supply, copy, or reuse identifiers; generate one per new record | New `ObjectCxtCode` and applicable distinct child codes |
| unique_configuration_identity | Unique SiteCode and EligibilityName; derived SequenceOrder | Yes | Before package generation | Verify | Retained request values and fresh export | derive_next_gig_configuration_sequence | The new configuration must not conflict with current rows, and its sequence must follow the current maximum | Provide a unique code and unused eligibility profile; the workflow derives the sequence | Retained SiteCode, EligibilityName, derived SequenceOrder |
| immutable_preview_approval | Immutable tabular preview and explicit import approval | Yes | Before core.data-loader import | Blocked | Validated candidate archive and explicit approval | | Only the unchanged archive shown to the user may be imported | Present the root, translation, availability-context, and child-filter candidate rows in clear tables, including generated identifiers; then obtain approval that names the environment, code, name, eligibility profile, task code, archive fingerprint, and import operation | Tabular candidate preview, archive fingerprint, and approval record |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | A required supplied value and its required evidence are available | Yes |
| Lookup | A documented read-only reference must be resolved | Yes |
| Verify | A fresh export or candidate archive must be checked | Yes |
| Blocked | A required value, fresh export, preflight result, or exact approval is missing | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GC.EXPORT_CURRENT | decision | 20 | resolve_dependency | exported->GC.VALIDATE_REFERENCES;unavailable->GC.RETURN_ISSUES | GC.VALIDATE_REQUEST | stop | A new Gig Configuration passed input validation |
