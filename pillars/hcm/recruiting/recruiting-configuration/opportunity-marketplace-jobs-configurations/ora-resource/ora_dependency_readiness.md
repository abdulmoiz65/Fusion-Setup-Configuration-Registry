# Opportunity Marketplace Jobs Configurations Dependency Readiness

Source: Opportunity Marketplace Jobs Configurations SKILL.md, adapted from the approved Gig Configuration create and copy contract.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Current Job Configuration export | Export the current task package before reference or identity validation. |
| 2 | Reference values | Resolve the eligibility profile or list unused profiles for selection, then resolve every supplied availability-context value, including Recruiting Types. |
| 3 | Current configuration identity | Check the retained code and eligibility profile, then derive the next sequence from the fresh export. |
| 4 | Candidate package | Derive the candidate archive from the fresh export, preserve its proven structure, and generate new availability-context identifiers for every new context and supplied child filter. |
| 5 | Immutable preview and approval | Complete preflight and obtain exact approval before core.data-loader import. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| current_job_configuration_export | Current Job Configuration FSM export | Yes | Creating a Job Configuration | Verify | Fresh export for task ORA_IRC_MP_SITE_CONFIGURATION | verify_fresh_job_configuration_export | Supplies current codes, assigned profiles, used sequences, metadata, exact member order, and parent-child references | Export current task data; do not use a stale or hand-built package | Current rows, package members, metadata member, parent-child references |
| copy_source_configuration | Source Job Configuration, user-supplied eligibility profile, and confirmed or supplied identity | Yes | Copying a Job Configuration | Verify and lookup | Fresh export source row, supplied EligibilityName, and optional SiteCode and SiteName | derive_copy_identity_and_filters | Copy creation must display the mandatory-values proposal when both fields are omitted and obtain approval, or use both requester-supplied values, without reusing source eligibility or technical identifiers | Approve `<source_code>_copy` and `<source_name>_copy`, or provide both replacement values; select an active unused eligibility profile | Confirmed or supplied SiteCode and SiteName; supplied EligibilityName; copied business filters |
| active_eligibility_profile | Active unused Opportunity Marketplace eligibility profile | Yes | Creating or copying a Job Configuration | Lookup | Supplied EligibilityName or fresh export assignment inventory | resolve_active_opp_marketplace_eligibility_profile | A configuration is segmented by its eligibility profile and that profile cannot already be assigned | Provide an active unused Opportunity Marketplace eligibility-profile name; if omitted or already used, select from the unused profiles list | EligibilityName |
| unused_eligibility_profile_inventory | Active unused Opportunity Marketplace eligibility profiles | Conditional | EligibilityName is omitted or already assigned in the fresh Job export | Lookup | Fresh Job export and target environment | list_active_unused_opp_marketplace_eligibility_profiles | The user needs an eligible profile selection before package generation | Select one profile from the returned list | Active unused EligibilityName options |
| availability_context_references | Optional location, organization, job family, job function, and Recruiting Type | Conditional | One or more availability-context values are supplied | Lookup | Supplied availability-context value and fresh task export | | All supplied filters must resolve exactly before package generation. A location also needs a proven geography-element hierarchy tuple. | Correct each value that has no exact eligible match or is ambiguous; stop when location hierarchy serialization cannot be proven. | Validated availability-context values and, for locations, element value/language pairs |
| new_availability_context_identifiers | New parent and child availability-context identifiers | Conditional | A new availability context or child filter row is added | Generate and verify | Secure 16-byte random values encoded as 32 uppercase hexadecimal characters | generate_new_job_availability_context_identifiers | The FSM import requires nonblank IDs, while copied IDs can conflict with target-pod records | Do not supply, copy, or reuse identifiers; generate one per new record | New ObjectCxtCode and applicable distinct child codes, including ObjectCxtRecTypeCode |
| unique_configuration_identity | Unique SiteCode and EligibilityName; derived SequenceOrder | Yes | Before package generation | Verify | Retained request values and fresh export | derive_next_job_configuration_sequence | The new configuration must not conflict with current rows, and its sequence must follow the current maximum | Provide a unique code and unused eligibility profile; the workflow derives the sequence | Retained SiteCode, EligibilityName, derived SequenceOrder |
| immutable_preview_approval | Immutable preview and explicit import approval | Yes | Before core.data-loader import | Blocked | Validated candidate archive and explicit approval | | Only the approved archive may be imported | Show only the required Field/Value preview with environment, operation, task, code, name, type, sequence, eligibility profile, location, job family, organization, job function, and Recruiting Type; omit Source, technical identifiers, and translation, availability-context, or child-filter candidate rows. Then obtain approval for the fingerprinted archive | Approved archive fingerprint and approval record |

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
| JC.EXPORT_CURRENT | decision | 20 | resolve_dependency | exported->JC.VALIDATE_REFERENCES;unavailable->JC.RETURN_ISSUES | JC.VALIDATE_REQUEST | stop | A new Job Configuration passed input validation |
