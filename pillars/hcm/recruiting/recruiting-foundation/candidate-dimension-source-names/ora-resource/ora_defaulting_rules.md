# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| SourceMedium | ORA_DIRECTSOURCE | Add Row direct source | No | |
| SourceMediumUrlValue | direct source | Add Row direct source | No | |
| SourceName and SourceDisplayName | Explicit requested Name | Add Row base SourceName and TL SourceName/SourceDisplayName | No | |
| Language and SourceLang | Verified requested/session language | New Add Row translation only | No | resolve_source_export |
| Sequence | Blank when omitted | Add Row without an explicit sequence | No | |
| ModuleId, Priority and UrlHeaderRegex | Blank | Add Row nullable fields not supplied by the supported request | No | |
| Existing fields | Preserve exported values | Retrieve, rename and every existing row during Add Row | No | resolve_source_export |

Direct-source defaults and nullable fields are grounded in the product sources in
reference lookups. Do not derive Name, URL or language. The UI computes the next
sequence, but a normal export can omit seeded rows; do not infer that sequence from
its maximum. Report a blank Sequence as Not populated in fresh export. That label
is presentation text, never an imported data value. Preview all applied defaults.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CDSN.APPLY_DEFAULTS | step | 40 | apply_default | preserved->CDSN.ENFORCE_DESIGN;blocked->CDSN.HANDLE_ISSUES | CDSN.RESOLVE_EXPORT | stop | Apply Add Row defaults only; preserve existing values otherwise |
