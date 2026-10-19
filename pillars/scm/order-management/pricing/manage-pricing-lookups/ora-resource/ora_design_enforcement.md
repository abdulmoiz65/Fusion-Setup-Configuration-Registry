# Manage Pricing Lookups Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm business need | Confirm that modifying a lookup is critical to the stated business requirement. |
| 2 | Assess Pricing impact | Confirm the proposed lookup change has a known effect on Pricing logic, or obtain Oracle guidance before proceeding. |
| 3 | Confirm identity | Use only the exact lookup type and code resolved from the approved requirement and applicable Oracle source. |
| 4 | Bind follow-on setup | Where another setup task consumes the value, record the resolved lookup identity in that task's configuration. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A predefined lookup is modified | Blocking | resolve_pricing_lookup_code | The business need is not critical or the effect on Pricing logic is uncertain | Preserve the predefined lookup and consult Oracle when the effect is uncertain | No |
| A lookup code is created or changed | Blocking | resolve_pricing_lookup_type | The exact lookup type or code has not been resolved | Stop and obtain the identity from the approved requirement and applicable Oracle source | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_pricing_lookup_type | A type is selected for inspection or change | Exact LookupType and returned lookup identity | ora_reference_lookups.md |
| resolve_pricing_lookup_code | A lookup code is created, changed, or validated | Existing code facts or available-for-create outcome | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QP.LOOKUPS.ENFORCE_DESIGN | decision | 30 | design_enforcement | compliant->QP.LOOKUPS.EXECUTION_GATE;oracle_consultation_required->RETURN_ORACLE_CONSULTATION;blocked->RETURN_DESIGN_ISSUES | QP.LOOKUPS.RESOLVE_CODE | stop | The lookup type and code have resolved. |
