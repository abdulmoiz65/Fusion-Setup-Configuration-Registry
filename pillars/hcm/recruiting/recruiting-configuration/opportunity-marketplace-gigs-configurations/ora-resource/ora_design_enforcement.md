# Opportunity Marketplace Gigs Configurations Design Enforcement

Source: Opportunity Marketplace Gigs Configurations SKILL.md and FSCR — Opportunity Marketplace Gigs Configuration.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve scope | Create only a new Gig Configuration; do not edit, activate, deactivate, delete, or change an existing sequence. |
| 2 | Derive package | Use the fresh exported package rather than a hand-built archive. |
| 3 | Preserve package structure | Retain one metadata member, documented CSV members, headers, member order, existing rows, language rows, and valid parent-child associations. |
| 4 | Add candidate rows | Add only the new root and dependent child rows. Generate new identifiers for the new parent context and every supplied child filter; never copy, reuse, or leave those identifiers blank. |
| 5 | Preflight and tabular preview | Validate archive identity, headers, row widths, uniqueness, parent-child relationships, generate an immutable SHA-256 preview, and present every candidate row in clear tables. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A Gig Configuration create package is prepared | Error | | The package is not derived from a fresh export or does not retain exactly one ASM_SETUP_CSV_METADATA.xml member | Regenerate from a fresh task export | Yes |
| A Gig Configuration create package is prepared | Error | | A required documented CSV member, header, member order, existing source row, language row, or valid parent-child association is changed or missing | Correct the candidate package while preserving the proven export structure | Yes |
| A new availability context is added | Error | | The package lacks one new unique 32-character uppercase hexadecimal `ObjectCxtCode`, contains a blank or reused child identifier, or has a child row that does not reference the new parent context | Generate the required identifiers, preserve the parent-child associations, and regenerate the immutable preview | Yes |
| A location child row is added | Error | resolve_recruiting_location | Its `GeographyElement<N>IdentifierValue` and `GeographyElement<N>LanguageCode` fields do not match the proven country-to-leaf hierarchy for the resolved `GeographyName`, including use of a `CountryCode` as an element value or generic `en` as a language code | Use the proven hierarchy tuple from the fresh current-task contract; block if no tuple can be proven | Yes |
| A Gig Configuration is copied | Error | derive_copy_identity_and_filters | Both omitted identity fields were not explicitly approved after displaying the required missing-identity proposal; supplied replacement code and name are incomplete; the source eligibility profile is copied; or a copied filter is unvalidated | State that Configuration code, Configuration name, and eligibility profile are mandatory. Display `Since Configuration code and Configuration name values are not provided. Configuration code, Configuration name, and eligibility profile are mandatory to create a Gig configuration. I am proposing the following values: <source_code>_copy and <source_name>_copy.` Require approval of the proposal or both replacement values, require a user-supplied active unused eligibility profile, and copy only validated business filters | Yes |
| A SequenceOrder is prepared for a new configuration | Error | | The value is copied from an existing configuration, supplied by the requester, or does not equal one greater than the highest current SequenceOrder | Derive the next sequence from the fresh export without changing existing configurations | Yes |
| Import preflight is requested | Error | | Archive identity, row widths, uniqueness, parent-child relationships, immutable preview, or SHA-256 fingerprint is missing or invalid | Correct the package and generate a new immutable preview | Yes |
| An import preview is requested | Error | | The end user has not been shown the required `Field`/`Value` confirmation table containing Location, Job family, Organization, and Job function, or the translation, availability-context, and child-filter candidate rows using business values | Render the single confirmation table and complete business-value candidate rows before requesting approval; retain technical identifiers for internal validation only | Yes |
| An import is requested | Error | | A tabular candidate preview is missing, or exact approval does not name the target environment, code, name, eligibility profile, task code, archive fingerprint, and import operation | Present the candidate rows in tables, obtain exact approval, and submit only through core.data-loader | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| derive_copy_identity_and_filters | A Gig Configuration is copied | Confirmed or supplied SiteCode and SiteName; copied business filters | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GC.GENERATE_PACKAGE | decision | 50 | design_enforcement | compliant->GC.PREVIEW_IMPORT;blocked->GC.RETURN_ISSUES | GC.VALIDATE_IDENTITY | stop | A new Gig Configuration passed identity validation |
