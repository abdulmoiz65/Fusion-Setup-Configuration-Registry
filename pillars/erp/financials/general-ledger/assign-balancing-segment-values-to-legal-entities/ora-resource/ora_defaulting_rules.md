# Assign Balancing Segment Values to Legal Entities Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| `GL_LEDGER.Name` | Exact ledger name from the resolved parent row | Create or explicit update | Yes when a supplied value disagrees; the scoped parent is authoritative | resolve_legal_entity_parent_row |
| `ORA_GL_JOURNAL_CONFIG_DETAIL.ObjectTypeCode` | `LEGAL_ENTITY` from the exact same-scope parent contract | The populated package or validated fallback evidence proves the parent role | Yes; block if the current parent role differs | resolve_legal_entity_parent_row |
| `ORA_GL_JOURNAL_CONFIG_DETAIL.SetupStepCode` | `NONE` from the exact same-scope parent contract | The populated package or validated fallback evidence proves this role value | Yes; block if the current parent value differs | resolve_legal_entity_parent_row |
| `ORA_GL_JOURNAL_CONFIG_DETAIL.LedgerName` | Preserve the exact parent export value, including a proven blank | Create or explicit update | Yes; never replace a valid blank with a display name | resolve_legal_entity_parent_row |
| `ORA_GL_JOURNAL_CONFIG_DETAIL.LegalEntityIdentifier` | Exact canonical parent identifier | Create or explicit update | Yes when supplied value disagrees | resolve_legal_entity_parent_row |
| `LegalEntityIdentifier` | Same exact canonical identifier as the parent | Create or explicit update | Yes when supplied value disagrees | resolve_legal_entity_parent_row |
| `FlexValueSetCode` | Exact scoped ledger BalSegValueSetCode, then REST-validated | Create or explicit update | Yes when a supplied value disagrees with the ledger-derived code | derive_scoped_balancing_value_set |
| `FlexSegmentValue` | Exact user-requested value after validation | Create or explicit update | No; never default, trim, or substitute | verify_balancing_value_exact |
| `StartDate` | Intentional blank | User omits start date and the current row contract permits blank | No; never default to current date | derive_assignment_row_contract |
| `EndDate` | Intentional blank | User omits end date and the current row contract permits blank | No; never derive an arbitrary horizon | derive_assignment_row_contract |
| `StartDate` and `EndDate` | User date serialized in the exact export-derived CSV date format | User supplies a valid date | No; format only, do not change the date | derive_assignment_row_contract |
| Audit fields | Leave service-owned fields blank for create; preserve exact current values for an explicit update without treating them as business defaults | Create or explicit update | Yes; do not copy audit values from another row or user input | derive_assignment_row_contract |
| `LegalEntityNameTrans` | Preserve existing exact value on update; use a proven same-role blank on create | Selected carrier and current business-state evidence support the disposition | Yes; do not synthesize a translated display name | derive_assignment_row_contract |

## Population Classes

| Class | Rule |
|---|---|
| User supplied | Legal entity choice, FlexSegmentValue, optional business dates, and an optional value-set cross-check remain business intent |
| Resolver derived | Ledger name, canonical legal-entity identifier, balancing ValueSetCode, value-set metadata, and value eligibility come only from exact current receipts |
| Carrier derived | Physical header order, field types, date serialization, and manifest graph come from the exact current populated carrier or the current same-task template fallback carrier |
| Current-state derived | Parent identity, parent readiness, existing legal-entity assignments, and direct-ledger ownership come from the populated carrier or the validated current fallback business-state evidence; never from the template alone |
| Intentional blank | Omitted dates, proven blank parent LedgerName, and proven blank LegalEntityNameTrans remain blank |
| Service owned | LastUpdateDate, LastUpdatedBy, LastUpdateLogin, CreationDate, and CreatedBy are never fabricated or copied from an unrelated row |

## Member and Field Population

| Member | Population Behavior |
|---|---|
| `ORA_LEGAL_ENTITY_BAL_SEG_VAL_DEF.csv` | Add one row per approved new semantic key or update only the explicitly requested dates of one exact existing row; preserve the actual 16-column header and all unrelated rows |
| `ORA_GL_JOURNAL_CONFIG_DETAIL.csv` | Parent dependency only. Preserve the member unchanged in populated mode. In template fallback mode, add only manifest-required parent closure rows whose complete values are proven by current parent evidence and reviewed same-release same-role constants; otherwise block |
| `GL_LEDGER_SEG_VAL_ASSIGNMENT.csv` | Preserve unchanged; this task does not assign values directly to a ledger |
| Remaining CSV members | Preserve exact rows, headers, aliases, and header-only state in populated mode. In template fallback mode, preserve template members and add only manifest-required dependency closure proven equal to current Fusion state |
| `ASM_SETUP_CSV_METADATA.xml` | Preserve the selected current populated or template export graph; never hand-author, reorder, or copy from another task or release |

## Disposition Rules

| Existing State | Requested State | Result |
|---|---|---|
| No exact assignment | Valid eligible exact assignment | Create one child row |
| One exact assignment with identical dates | Same assignment and no explicit change | No-op; report current state and do not submit an empty import |
| One exact assignment | Explicit supported date change | Update only the exact current row after preview and approval |
| One exact assignment to a different legal entity or direct ledger in the same accounting context | Create or implicit reassignment | Block; deletion or reassignment requires a separate accountable design and posted-use checks |
| Multiple exact assignment rows | Any request | Block as ambiguous or inconsistent state; do not choose a row |

## Pre-Import Default Evidence

| Evidence | Required Proof |
|---|---|
| Parent technical fields | Exact current populated ORA_GL_JOURNAL_CONFIG_DETAIL.csv parent row, or validated fallback parent evidence plus reviewed same-release same-role static-field proof |
| Child physical fields | Current populated or template ORA_LEGAL_ENTITY_BAL_SEG_VAL_DEF.csv header and matching ASM field graph |
| Value-set constraints | Exact scoped ledger BalSegValueSetCode receipt plus exact current REST receipt for ValueSetId and MaximumLength |
| Value eligibility | Exact current child-value REST receipt for enabled state and effectivity |
| Existing assignment state | Current populated assignment members, or current fallback evidence that covers both legal-entity and direct-ledger ownership; the template is never absence proof |
| Blanks and service-owned fields | Current same-release same-role contract; a failed import is not an evidence source and previous populated data may prove only static role behavior, not current ownership |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ABSV.DEFAULTS | step | 40 | apply_default | applied->ABSV.ENFORCE;blocked->ABSV.RETURN_ISSUES | ABSV.LOOKUPS | stop | Exact resolver and export receipts are available |
