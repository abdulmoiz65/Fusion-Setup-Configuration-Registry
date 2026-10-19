# Planning FBDI Design Policy

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every prompt, CSV or ZIP | High | | Request/output exceeds the supported-file table in SKILL.md, or no supported file remains | Apply the single SKILL.md boundary during intake and package preparation. Reject unsupported prompt entities; retain supported mixed-ZIP members in a new archive and disclose exclusions. | New filtered archive only; never alter the source |
| Every prompt, CSV or ZIP | High | | Requested or prepared collection mode is not Net Change, or the Net Change FYI is missing | Use SKILL.md's Net Change default and FYI. Reject an explicit Targeted or other mode request as unsupported; do not silently change it or ask for mode approval. Preserve Core upload/initiation approval | Add a missing FYI before preview; never switch an explicitly requested unsupported mode |
| A previously attempted archive is requested again | High | | Prior result is uncertain or no explicit reload approval exists | Reconcile status through Core when requested; never automatically replay a load | Only through Core's explicit retry/reload workflow |

## Task Nodes

Evaluate the prepared member manifest and exclusion evidence against SKILL.md.
This is an evidence check, not a second scope-script execution or ZIP rewrite.
Template/content validation is owned by ora_input_validation.md.

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CHECK_SUPPORTED_ENTITIES | decision | 10 | design_enforcement | supported->VALIDATE_FBDI_ARCHIVE;unsupported->RETURN_ISSUES | none | stop | Core Task Hook evaluates the selected Planning package |
