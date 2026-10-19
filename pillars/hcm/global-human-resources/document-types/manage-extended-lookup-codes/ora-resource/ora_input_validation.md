# Manage Extended Lookup Codes Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Extended Lookup Codes.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, or delete | Block | Provide one supported operation | Every request |  |
| Read scope | Explicit filter or bounded full-list request | Block | Provide a filter or request the bounded collection | get | find_extended_lookup_codes |
| Existing code selector | Complete LookupType, LookupCode, ExtendedLookupCode, and explicit legislation scope | Block | Provide the complete scoped business key | get, edit, or delete | find_extended_lookup_codes |
| Translation selector | Complete parent scoped business key and Language | Block | Provide the exact target language | create, edit, or delete of a translation | find_extended_lookup_codes |
| Create values | Complete business key, display name, and a complete nonblank SourceSystemOwner and SourceSystemId pair; when the caller supplies neither source-key value, generate the deterministic FDOS pair from the resolved business key | Block | Provide or generate all mandatory create values before source construction | create |  |
| Edit changes | Exact current business key and at least one supported change | Block | Provide the target and intended change | edit | find_extended_lookup_codes |
| Delete acknowledgement | Fresh exact target and explicit irreversible-delete acknowledgement | Block | Resolve the target and acknowledge deletion | delete | find_extended_lookup_codes |
| Parent lookup | LookupType/LookupCode or their exact UI meanings, plus requested legislation scope | Block | Resolve the displayed values to one stored parent tuple | create or edit | resolve_extended_lookup_parent_scope |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An exact target does not resolve once after bounded paging and translation grouping | Missing | Correct the complete scoped business key | find_extended_lookup_codes |
| A create key matches an existing Extended Lookup Code | Invalid | Stop the duplicate create | find_extended_lookup_codes |
| The parent lookup is missing, disabled, ineffective, ambiguous, or territory-incompatible | Invalid | Correct the parent lookup or legislation scope | resolve_extended_lookup_parent_scope |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Complete business key | Reject blank LookupType, LookupCode, or ExtendedLookupCode | An exact operation is requested |  |
| Translation grouping | Group translated projections by runtime identity before deciding exact-match cardinality | A lookup returns translated rows | find_extended_lookup_codes |
| Parent stored code | Require one enabled current stored parent code; reject an unverified meaning | A parent lookup is supplied | resolve_extended_lookup_parent_scope |
| Display-meaning resolution | Resolve a supplied type or code that is not a stored value by exact `Meaning` in Common Lookups; require one match before using its stored value | A parent type or code is supplied as a UI display value | resolve_extended_lookup_parent_scope |
| Legislation consistency | Require the resolved parent LegislationCode; reject Global or another display value as a loader code | Legislation scope is supplied | resolve_extended_lookup_parent_scope |
| Supported fields | Reject unknown workbook columns, unsupported source shapes, and missing references | A mutation source is prepared |  |
| Runtime identity | Reject a caller-supplied or persisted `ExtendedLookupCodeId`; allow only the ID freshly resolved for one exact edit, delete, or translation source | An internal ID is proposed | find_extended_lookup_codes |
| Generated source-key mode | When the caller supplies neither source-key value, require SourceSystemOwner=FDOS and SourceSystemId=FDOS_XLOOK_ plus the first 32 uppercase SHA-256 hexadecimal characters of the UTF-8 compact JSON array [LookupType,LookupCode,LegislationCode-or-GLOBAL,ExtendedLookupCode] | A base create source is prepared without caller-supplied source keys |  |
| Explicit source-key mode | Require both source-key values, validate owner provenance, and preserve the pair unchanged; reject a partial or blank pair | A caller explicitly supplies either source-key field |  |
| Editable source contract | Require an XLSX generated from current Core Data Loader metadata; DAT conversion is internal and the workbook is the reviewed approval source | Any mutation source is prepared |  |
| Create source identity | Require every base create XLSX row and generated DAT METADATA/MERGE row to contain nonblank SourceSystemOwner and SourceSystemId values; reject a keyless MERGE even when the scoped business key is complete | A base create source is prepared |  |
| Native DAT contract | Require Core Data Loader to generate the live-validated `METADATA` header for `ExtendedLookupCode` or `ExtendedLookupCodeTranslation`; do not hand-author DAT or add `RestAction` | Any mutation source is converted internally |  |
| DAT record verb | Require the internal conversion to emit `MERGE` for create or edit and `DELETE` for delete | Any mutation source is converted internally |  |
| Minimal source | Retain the scoped business fields, requested DFF values, and the required validated source-key pair for a base create; omit unrelated DFF, GUID, and source-reference fields | A mutation source is prepared |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| XLOOK.VALIDATE | decision | 1 | validate_input | valid->XLOOK.DEPENDENCY;missing->XLOOK.ERROR;invalid->XLOOK.ERROR;unsupported->XLOOK.ERROR | none | stop | Every Extended Lookup Code request |
