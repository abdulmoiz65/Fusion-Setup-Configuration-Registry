# Opportunity Marketplace Jobs Configurations Design Enforcement

Source: Opportunity Marketplace Jobs Configurations SKILL.md, adapted from the approved Gig Configuration create and copy contract.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve scope | Create only a new Job Configuration; do not edit, activate, deactivate, delete, or change an existing sequence. |
| 2 | Derive package | Use the fresh exported package rather than a hand-built archive. |
| 3 | Preserve package structure | Retain one metadata member, documented Jobs CSV members, headers and header order, existing rows, language rows, and valid parent-child associations. |
| 4 | Add candidate rows | Apply ora_defaulting_rules.md and persist its decision evidence before adding Recruiting Type rows. Add only the new root and dependent child rows. Generate new identifiers for the new parent context and every supplied child filter, including Recruiting Type; never copy, reuse, or leave those identifiers blank. |
| 5 | Preflight and preview | Validate archive identity, headers, row widths, uniqueness, parent-child relationships, and generate an immutable SHA-256 preview. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A Job Configuration create package is prepared | Error | | The package is not derived from a fresh export or does not retain exactly one ASM_SETUP_CSV_METADATA.xml member | Regenerate from a fresh task export | Yes |
| A Job Configuration create package is prepared | Error | | A required documented Jobs CSV member, header or header order, existing source row, language row, or valid parent-child association is changed or missing | Correct the candidate package while preserving the proven export structure | Yes |
| A new availability context is added | Error | | The package lacks one new unique 32-character uppercase hexadecimal ObjectCxtCode, contains a blank or reused child identifier, or has a child row that does not reference the new parent context | Generate required identifiers including ObjectCxtRecTypeCode when a Recruiting Type row is supplied, preserve parent-child associations, and regenerate the immutable preview | Yes |
| A location child row is added | Error | resolve_recruiting_location | Its `GeographyElement<N>IdentifierValue` and `GeographyElement<N>LanguageCode` fields do not match the proven country-to-leaf hierarchy for the resolved `GeographyName`, including use of a `CountryCode` as an element value or generic `en` as a language code | Use the proven hierarchy tuple from the fresh current-task contract; block if no tuple can be proven | Yes |
| A Job Configuration is copied | Error | derive_copy_identity_and_filters | Both omitted identity fields were not explicitly approved after displaying the mandatory-values proposal; supplied replacement code and name are incomplete; the source eligibility profile is copied; or a copied filter is unvalidated | Require approval of the proposed identity or both replacement values, require a selected active unused eligibility profile, and copy only validated business filters | Yes |
| A SequenceOrder is prepared for a new configuration | Error | | The value is copied from an existing configuration, supplied by the requester, or does not equal one greater than the highest current SequenceOrder | Derive the next sequence from the fresh export without changing existing configurations | Yes |
| A Job function row is prepared | Error | resolve_active_job_function | The supplied LOV display Meaning does not resolve exactly once or its resolved LookupCode is not used in the FSM child row | Correct the display value or package row using the resolved LookupCode | Yes |
| A Recruiting Type row is prepared | Error | resolve_recruiting_type | The supplied LOV display Meaning does not resolve exactly once or its resolved LookupCode is not used in the FSM child row | Correct the display value or package row using the resolved LookupCode | Yes |
| A Recruiting Type DefaultFlag is prepared | Error | derive_recruiting_type_default_flag | The candidate value differs from the system-derived result of ora_defaulting_rules.md, or its validation/preflight evidence is absent or inconsistent | Reapply the defaulting rule and persist its decision before preview. A valid fresh source with zero Recruiting Type rows is an approved bootstrap case, not a blocker solely for lacking a source DefaultFlag row; never ask the user for this field | Yes |
| Import preflight is requested | Error | | Archive identity, row widths, uniqueness, parent-child relationships, immutable preview, or SHA-256 fingerprint is missing or invalid | Correct the package and generate a new immutable preview | Yes |
| An import is requested | Error | | The preview does not show the required Field/Value business fields, includes Source or generated technical identifiers, or exact approval does not name the target environment, code, name, eligibility profile, task code, archive fingerprint, and import operation | Correct the preview, obtain exact approval, and submit only through core.data-loader | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| derive_copy_identity_and_filters | A Job Configuration is copied | Derived SiteCode and SiteName; copied business filters | ora_reference_lookups.md |
| resolve_active_job_function | A Job function child row is supplied | Exact display Meaning and its resolved JobFunctionCode | ora_reference_lookups.md |
| resolve_recruiting_type | A Recruiting Type child row is supplied | Exact display Meaning and its resolved RecruitingTypeCode | ora_reference_lookups.md |
| derive_recruiting_type_default_flag | A Recruiting Type child row is supplied | System-derived DefaultFlag and fresh-package decision evidence | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JC.GENERATE_PACKAGE | decision | 50 | design_enforcement | compliant->JC.PREVIEW_IMPORT;blocked->JC.RETURN_ISSUES | JC.DERIVE_REC_TYPE_DEFAULT | stop | A new Job Configuration passed identity validation and DefaultFlag derivation or its not-applicable check |
