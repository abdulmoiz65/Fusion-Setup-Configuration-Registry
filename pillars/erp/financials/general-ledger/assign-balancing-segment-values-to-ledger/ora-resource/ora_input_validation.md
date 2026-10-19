# Assign Balancing Segment Values to Ledger Input Validation

Validate the task-local FSM package before preview. These checks cover only the direct ledger assignment object GL_LEDGER_SEG_VAL_ASSIGNMENT; do not use the Enterprise Data Model as evidence that an undocumented FSM code is accepted.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Ledger-only Company Value preview | LedgerName; SegmentValue is absent from the active request | Do not block a preview; render exactly two tables: eligible direct-ledger selections, then existing or blocked values with direct-assignment dates and legal-entity state | Resolve the ledger balancing-segment context, then run the candidate-value resolver | A user supplies ledger context without a Company Value | list_eligible_balancing_segment_values |
| Assignment target intent | A target that resolves exactly as a Ledger, with no explicit Legal Entity target | Stop before package generation | Resolve the stated target as a ledger. Treat it as a direct ledger assignment when it resolves exactly and no Legal Entity is named; when a Legal Entity is explicitly requested but unnamed, ask for its exact name and route to that task | A Company Value and target name are supplied | resolve_ledger_id_by_exact_name |
| Target ledger for a supplied Company Value | LedgerName | Stop before value validation or package generation | Ask for the exact target ledger, then resolve its balancing value set and assess the supplied Company Value in that ledger context | SegmentValue is supplied without LedgerName |  |
| Direct ledger assignment identity | LedgerName, SegmentTypeCode, SegmentValue (UI label: Company Value) | Block package generation | Provide the intended ledger and company value; derive technical ledger context through the task-local lookups | Every new or changed GL_LEDGER_SEG_VAL_ASSIGNMENT row | resolve_ledger_balancing_segment_context |
| Eligible nonlegal-entity value evidence | Exact enabled balancing-segment value in the resolved value set and no legal-entity assignment for that value | Block package generation | Confirm the value through the documented read-only value-set LOV and obtain current legal-entity-assignment evidence | Every direct ledger assignment row | verify_balancing_segment_value_exists |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| LedgerName is supplied without SegmentValue in the active request | Ready for preview only | Submit the paired primary-ledger-scoped exports for direct ledger and legal-entity assignments, then return exactly two tables. The eligible table contains only values with no direct assignment in any period and no legal-entity assignment. The existing or blocked table contains every other candidate with direct-assignment periods, legal-entity eligibility, and reason. Do not offer a legal-entity-assigned value for direct ledger selection. Do not use a value or dates from prior conversation, export data, or project state; do not generate an import package. | list_eligible_balancing_segment_values |
| SegmentValue and a target name are supplied with no Legal Entity signal | Resolve direct-ledger intent | Resolve the target through the exact ledger lookup. If it resolves exactly as a ledger, continue with the direct-ledger workflow; do not require a repeated word such as "ledger" after the name. | resolve_ledger_id_by_exact_name |
| A Legal Entity is explicitly named or the request says to assign to a Legal Entity | Blocked for this task | Route to Assign Balancing Segment Values to Legal Entities; do not treat the Legal Entity as an ignorable detail or start the direct-ledger export. |  |
| SegmentValue is supplied without LedgerName in the active request | Blocked | Ask only for the exact target ledger. After it is supplied, resolve the ledger context and validate that Company Value against the resulting value set and assignment evidence. |  |
| LedgerName resolves as SECONDARY and no owning primary ledger is supplied | Blocked | Ask for the exact owning primary ledger name. Do not submit the secondary LedgerId as a primary-ledger export scope, guess a parent, or run an unscoped export. | resolve_primary_ledger_export_scope |
| LedgerName resolves to zero or multiple current ledger rows | Blocked | Supply an exact ledger name from a fresh task export; never select a similarly named ledger | resolve_ledger_balancing_segment_context |
| The proposed value is absent, inactive, ineffective, assigned to a legal entity, or lacks assignment evidence | Blocked | Resolve it in the exact ledger value set, then assign and verify legal-entity values separately or provide evidence that it is unassigned | verify_balancing_segment_value_exists |
| The proposed value is already directly assigned to the target ledger for an overlapping effective period | Blocked | Return the existing assignment as a duplicate; do not generate or import another row | list_current_ledger_assignments |
| Existing task export has no GL_LEDGER_SEG_VAL_ASSIGNMENT data member | Ready with evidence gap | Use the export only for package shape and ledger metadata; obtain the scoped dependent value evidence before authoring new rows | inspect_assignment_task_package |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| SegmentTypeCode is present and preserved from supported metadata or exact same-scope export evidence | Block if blank or invented | Every assignment row | inspect_assignment_task_package |
| SegmentValue is nonblank, no longer than 25 characters, and resolves as enabled/effective in the exact ledger value set | Block if blank, longer than the Enterprise Data Model limit, inactive, or not found | Every assignment row | verify_balancing_segment_value_exists |
| Value-definition attributes are not collected as assignment inputs | Do not ask for Summary, Allow Posting, Allow Budgeting, hierarchy, or equivalent value-maintenance fields; obtain only enabled, effective, non-summary status from the exact value-set lookup | Every direct ledger assignment | verify_balancing_segment_value_exists |
| SegmentValue, StartDate, and EndDate originate in the active request | Block assignment processing if any is taken from an earlier conversation, project run record, or exported assignment row | Every assignment row |  |
| LedgerName identifies exactly one ledger and its balancing-segment metadata is complete | Block if ambiguous or incomplete | Every assignment row | resolve_ledger_balancing_segment_context |
| A ledger resolves as SECONDARY | Require the exact owning primary LedgerName before the scoped export; use the verified primary numeric LedgerId only as PRIMARY_LEDGER_ID | Every preview or assignment request for a secondary ledger | resolve_primary_ledger_export_scope |
| StartDate and EndDate are valid dates; EndDate is not before StartDate | Block the invalid row | When either date is supplied |  |
| StartDate and EndDate are optional active-request inputs | Preserve intentional blanks as open-ended effective dates; do not request dates unless the user wants to control the effective period | Every assignment row |  |
| LegalEntityIdentifier is blank for a direct ledger assignment | Block and route legal-entity-specific values to the separate legal-entity assignment task | Every GL_LEDGER_SEG_VAL_ASSIGNMENT row |  |
| Company Value is selected from the ledger-specific value list, not free-typed or copied from the Legal Entity Company Value Assignments reference grid | Block unsupported selection | Every assignment row | verify_balancing_segment_value_exists |
| SegmentValueTypeCode is not hand-authored | Block a manually invented value; preserve exact export behavior only when it is evidenced | Every assignment row | inspect_assignment_task_package |
| GL_LEDGER.Name and GL_SECONDARY_LEDGER.Name parent keys match the resolved ledger context | Block if either parent key is missing or inconsistent | Every assignment row in the task’s scoped export contract | inspect_assignment_task_package |
| Final-ZIP CSV physical serialization and archive safety are valid | Parse every changed CSV member and require the exact export-derived header, physical record count, and expected field count; reject literal escape-text record boundaries, malformed quoting, absolute or traversal paths, duplicate members, and unexpected executable content | Every final import ZIP before approval | inspect_assignment_task_package |
| Audit, request, record, object-version, and process fields are absent from the create payload | Remove them before package generation | Every new row |  |
| AttributeCategory and Attribute1 through Attribute15 are blank unless an explicitly requested deployed DFF context supplies each value | Block unsupported DFF population | When any DFF field is populated |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BSVL-010-VALIDATE-INPUT | step | 10 | validate_input | valid->BSVL-020-RESOLVE-REFERENCES;invalid->BSVL-070-RETURN-ISSUES | none | stop | Every ledger context |
