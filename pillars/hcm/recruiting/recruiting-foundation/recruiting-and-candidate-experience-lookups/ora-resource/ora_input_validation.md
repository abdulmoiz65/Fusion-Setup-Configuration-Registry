# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Business outcome | Desired Recruiting outcome, affected process or audience, intended timing, and requested policy or terminology change | Return a business-language issue | Ask only for the missing business decision | Every request | |
| Requested operation | List or read lookup types, list or read codes, create/update/delete a type or code, read translations, explicit CSV export, or explicit FSM CSV import | Return a business-language issue | Resolve the technical operation internally and clarify only a genuine ambiguity | Every request | |
| Lookup type identity | One exact LookupType or an unambiguous business request that resolves to one approved current type | Block exact read or mutation | Ask for the technical identifier only when multiple valid Recruiting matches remain | Exact type, code, translation, or mutation | resolve_recruiting_common_lookup_type |
| Lookup code identity | One exact LookupCode selected from current provider results | Block exact code read, translation read, update, or delete | Resolve current codes internally; clarify only when multiple valid matches remain | Exact code operation | resolve_recruiting_lookup_code |
| Target environment | Exact Fusion environment | Block mutation preview or import | Ask for the environment immediately before mutation preparation | Type/code mutation or FSM import | |
| Requested field delta | Only fields established as mutable by current documented Common Lookup response metadata | Block mutation preview | Explain supported current fields and request the minimal business change | Create or update | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| LookupType starts with one approved prefix | In scope | Continue through the Common Lookup view | classify_recruiting_lookup_type |
| LookupType matches no approved prefix | Blocked | Report the ownership-mapping gap and require refreshed approved evidence | classify_recruiting_lookup_type |
| A list contains both owned and non-owned types | Filtered | Retain only exact types matching the approved prefix baseline before any detailed read | classify_recruiting_lookup_type |
| Current response metadata does not establish a requested field or capability | Blocked | Return the evidence gap without inferring behavior | resolve_recruiting_common_lookup_type |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Common view only | Route every read and mutation through the Common Lookup view of `core.fusion-api.apps-common.lookups` | Every lookup operation | |
| Ownership prefix | Require case-sensitive `starts with` matching against `ORA_JA`, `ORA_IRC`, `ORA_OM`, `IRC_HCO`, or `ORA_LI` | Every lookup type | classify_recruiting_lookup_type |
| Response-grounded output | Return only documented fields actually present, including type/code meanings, descriptions, enabled state, dates, tag, and display sequence when returned | Read | |
| Module claims | Do not claim ModuleId filtering, API ownership discovery, returned ModuleId, CustomizationLevel, RestAccessSecured, or module display name unless current documented metadata explicitly establishes it | Every operation | |
| Translation boundary | Retrieve translations only when requested and treat them as read-only | Translation request | read_lookup_code_translations |
| Parent exact pre-read | Freshly read the exact current parent before every parent update/delete and before every code operation | Parent mutation or code operation | resolve_recruiting_common_lookup_type |
| Code exact pre-read | Freshly read the exact current code before every code update or delete | Code update or delete | resolve_recruiting_lookup_code |
| Parent create absence | Confirm the exact proposed LookupType is absent before approval | Create lookup type | resolve_recruiting_common_lookup_type |
| Code create absence | Confirm the exact proposed LookupCode is absent under the exact current parent before approval | Create lookup code | resolve_recruiting_lookup_code |
| Preservation | Preserve LookupType, LookupCode, approved ownership basis, seed identity when available, protected fields, and every unrequested field | Update or delete | resolve_recruiting_lookup_code |
| De-duplication | De-duplicate only by exact LookupType and, for child results, exact LookupCode | Listing | |
| Bulk boundary | Use task CSV export or FSM CSV import only when explicitly requested, catalog-supported, validated, and approved | Export or import | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RCL.VALIDATE | decision | 1 | validate_input | list_types->RCL.LIST_TYPES;exact_type->RCL.CLASSIFY_SCOPE;codes->RCL.CLASSIFY_SCOPE;translations->RCL.CLASSIFY_SCOPE;create_type->RCL.CLASSIFY_SCOPE;update_type->RCL.CLASSIFY_SCOPE;delete_type->RCL.CLASSIFY_SCOPE;create_code->RCL.CLASSIFY_SCOPE;update_code->RCL.CLASSIFY_SCOPE;delete_code->RCL.CLASSIFY_SCOPE;post_change->RCL.VERIFY_RESOURCE;issues->RCL.INPUT_ISSUES | none | stop | Every Recruiting and Candidate Experience Lookups request |
