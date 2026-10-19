# Reservation Priority for Sales Orders Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A requested Reservation Priority attribute, ordering, or FSM package row is invalid | Stop and request a package that conforms to the lookup and export-derived field contract. |
| A generated sorting-rule RuleCode already exists in the fresh exported baseline | Stop before package preparation and ask whether to update the existing rule or choose an explicit distinct rule name. |
| A created sorting rule has no matching US source-language row in ORA_TRANSLATION_FOR_PREFERENCE_RULE.csv | Stop before package preparation and add the generated or supplied RuleName and Description with Language and SourceLang set to US. |
| A sorting rule entry uses Priority as a choice position or has an invalid SortingOrder | Stop before package preparation and rebuild the AttributePriorityJson entries with Priority 1 and one-based SortingOrder values. |
| A sorting rule contains more than three distinct attributes | Stop before package preparation and ask the user to reduce the rule to three distinct AttributeCodes or fewer. Multiple entries with the same AttributeCode and different values count as one attribute. |
| A required default-sort or rule-details read fails or is incomplete | Stop before package preparation; persist a sanitized transport/environment, auth/authz, or Fusion API diagnostic. Do not infer live Reservation Priority state or substitute a stale response. |
| A rule is marked active or default without an explicit user request | Stop before package preparation and reset the unrequested state to N. |
| An explicitly default rule leaves another Reservation Priority rule marked default | Stop before package preparation and set every other RESERVATION_PRIORITY default row to N. |
| An FSM import package is not export-derived or environments are on different releases | Stop and request a source export/template or same-release target environment. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Invalid FSM field contract | The package has an attribute absent from `ORA_FOM_RESERVE_PRIORITY_ATTR`, an invalid ordering, an unsupported attribute-row field combination, or invalid task metadata | Correct the package from the exported task baseline before preview. |
| Duplicate generated sorting rule | A generated `PRIORITIZE_<ATTRIBUTE_LOOKUP_CODE>` or `PRIORITIZE_<ORDERED_ATTRIBUTE_LOOKUP_CODES>` already exists and the user did not explicitly request an update | Obtain an update instruction or an explicit distinct rule name; do not append a duplicate row. |
| Generated RuleCode exceeds 30 characters | A generated RuleCode is longer than the Fusion field limit | Rebuild it with the deterministic abbreviated-and-hashed length-safe format, then check the result against the fresh baseline before package preparation. |
| Missing rule translation | A created RuleCode has no matching US source-language translation row, or its RuleName, Description, Language, or SourceLang does not match the rule contract | Add or correct the one US source-language row while preserving unrelated translations. |
| Invalid sorting rule entry ordering | An AttributePriorityJson entry has Priority other than 1 or an ordering position outside one-based SortingOrder | Rebuild the rule entries with numeric Priority 1 and consecutive SortingOrder values beginning at 1. |
| Exceeded sorting rule attribute limit | A rule contains more than three distinct AttributeCodes | Do not generate the package; reduce the rule to at most three distinct attributes. Multiple entries with the same AttributeCode and different values count as one attribute. |
| Live Reservation Priority state unavailable | The required `omReservationPriorities` defaultSortingOrder or ruleDetails GET is unsuccessful, incomplete, or cannot be reconciled with the fresh export | Stop before package preparation and persist the classified sanitized diagnostic; do not import. |
| Unrequested rule state | A created or updated rule uses IsActive Y or IsDefault Y without explicit user instruction | Reset the unrequested state to N before preview. |
| Conflicting default rules | An explicitly default rule leaves zero or more than one RESERVATION_PRIORITY row with IsDefault Y | Set the selected rule to Y and every other Reservation Priority rule to N; validate exactly one default before preview. |
| Incompatible FSM migration | The source and target instances are on different releases or the package is not export-derived | Use compatible source and target instances and rebuild the package from the official task export. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation or migration blocker | The invalid field or migration requirement and that no Fusion import was attempted. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The FSM package or environment compatibility check fails | Upload, initiate, retry, or substitute an FSM import. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RESERVATION_PRIORITY.FSM_IMPORT_PREVIEW | step | 25 | execution_gate | preview_ready->RESERVATION_PRIORITY.VALIDATE_FSM_MIGRATION;preview_or_approval_missing->RETURN_ISSUES | RESERVATION_PRIORITY.RESOLVE_CUSTOMER | stop | After the immutable FSM package passes field validation and attribute lookup resolution, and before a Fusion import. |
| RETURN_SUCCESS | terminal | 40 | terminal | none | RESERVATION_PRIORITY.VALIDATE_FSM_MIGRATION | continue | The FSM package and migration compatibility checks passed. |
| RETURN_ISSUES | terminal | 50 | terminal | none | none | continue | The FSM package field contract, preview, approval, or migration compatibility check fails. |
