# Manage Procurement Agents Client-Side Error Handling

## Source Basis

- Oracle Fusion Cloud Procurement 26C Procurement Agents and Flexfields for Procurement Agents documentation
- Procurement-agent Redwood, REST, and UI acceptance-criteria exports supplied by the developer

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required parent identity or access-policy input is missing or invalid | Stop client-side processing and identify the exact missing or invalid parent fields |
| Supplied client-side candidate data contains the same resolved Agent and Procurement BU pair | Stop the client preview and require a different pair or corrected candidate data |
| Client-side duplicate evidence is unavailable | Continue without prompting; the selected Data Loader route owns environment validation |
| Parent Agent or Procurement BU is absent for an update | Stop update preparation and request the missing display value needed for surrogate-key derivation |
| DFF parent linkage is absent in a prepared loader row | Derive Agent and Procurement BU from the parent record; do not request them as child-level input |
| A parseable DFF value is supplied | Accept and normalize the value through the registered DFF child section; do not request a duplicate DFF attribute name or enabled-attribute evidence |
| A live DFF attribute header includes a context binding | Treat the header-bound context as authoritative and leave `FLEX:PO_AGENT_ASSIGNMENTS`, `__FLEX_Context`, and `__FLEX_Context_DisplayValue` blank; do not ask the user for a context value |
| Fusion reports that a Context Prompt is not in the list of values | Remove any populated context-selector value, retain the DFF value in its header-bound attribute column, validate the corrected archive, and require new approval before resubmission |
| A supplied DFF date is invalid or uses an unsupported loader literal | Identify the DFF date field and request a parseable ISO date or timestamp; normalize valid values to `YYYY/MM/DD HH24:MI:SS` before validation |
| The user lacks the required client action or implementation privilege | Disable the action and report the authorization requirement without attempting a remote request |
| The registered DFF child section cannot accept the supplied value | Stop client-side processing with a metadata-contract mismatch; correct the child-section metadata or source value without asking the user to reconfirm the DFF input |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Duplicate candidate | Supplied identity fields, client-side duplicate result, and one safe correction path |
| Validation failure | Exact field names, accepted values, and whether the issue blocks create, update, or DFF maintenance |
| Client-side readiness limit | That no live lookup or remote mutation was performed, plus the separate workflow needed for environment verification |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PAG.HANDLE_ISSUES | step | 50 | error_handler | handled->PAG.RETURN_ISSUES | none | stop | Client-side validation, duplicate checking, design enforcement, privilege, or DFF readiness is blocked |
| PAG.RETURN_ISSUES | terminal | 60 | terminal | none | none | stop | A client-side blocking issue has been disclosed with a safe next action |
| PAG.READY_CREATE | terminal | 70 | terminal | none | PAG.ENFORCE_CREATE | stop | The client-side create preview is complete; any environment verification or mutation belongs to a separate workflow |
| PAG.READY_UPDATE | terminal | 80 | terminal | none | PAG.ENFORCE_UPDATE | stop | The client-side update or DFF maintenance preview is complete; any environment verification or mutation belongs to a separate workflow |
