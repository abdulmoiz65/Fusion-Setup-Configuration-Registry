# Person Security Profile Error Handling

Source: developer-provided person security profile business rules.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A new person security profile Name duplicates an existing profile | Stop before preview or CSV package generation and ask for a unique Name |
| A configuration violates the Areas of Responsibility or View All compatibility rules | Stop before preview and identify each unsupported selected criterion |
| ApplyExclusionRulesFlag is true while neither SecureByAreasOfResponsibilityFlag nor ViewAllFlag is true | Stop before preview or CSV package generation; select Secure By Areas of Responsibility or View All, or remove the exclusion rules |
| More than three exclusion rules are associated | Stop before preview and identify the excess exclusion rules |
| A person type selection has no AccessTo value, uses a value other than All or Restricted, or uses All while an applicable criterion restricts that same selected person type | Stop before preview and identify the affected selection; evaluate each person type independently, retaining All for unrestricted selections and requiring Restricted only for the selection that an applicable criterion limits |
| Assignment evaluation is required but remains blank after defaulting | Stop before preview and apply the documented default or request an explicit value |
| Assignment evaluation contains a display meaning or exceeds the CSV field length | Stop before preview, resolve the value through ORA_PER_PRSN_ASGS_TO_EVALUATE, and write only the exact enabled lookup code |
| An enabled profile uses the same complete work-structure criterion set and the AOR alternative has not been reviewed | Stop before preview. Show the matching profile Names, shared criteria, and the exact AOR scope recommendation when one is available; require an explicit exception confirmation to continue the original design. |
| The similar-profile or AOR-scope lookup is unavailable or incomplete | Stop before preview; do not infer existing configurations or an AOR scope recommendation. |
| A CSV package is requested before all profile attributes and the current task template are available | Stop before package generation; do not invent columns, package members, mappings, or metadata |
| A generated package omits, duplicates, renames, reorders, or changes the header of a CSV member from the current template-only export | Classify as a package-completeness failure. Stop before preview or import; rebuild the ZIP from the template's ordered CSV-member manifest, retaining each no-data member as its exact template-header-only CSV. |
| A CSV package cannot be resolved from the current template-only export, or a generated row differs from its resolved parent link, field mapping, or header order; or conflicts with template-declared ViewInstanceName or GroupingKey evidence | Stop before preview or import. Obtain a current template-only export, resolve the CSV context again, rebuild the package only from that result, use the documented fallback only where the template omits the value, and retain ASM_SETUP_CSV_METADATA.xml byte-for-byte unchanged. |
| Fusion reports a child-logical-row error, including `childLogicalRows` being null | Classify as a package-completeness failure. Preserve the sanitized process-log reference, rebuild from a fresh template-only export with every template CSV member included (header-only where no rows apply), validate the corrected package, and require fresh approval before resubmission. |
| A CSV import is requested before exact package approval | Classify as an approval blocker; do not invoke core.data-loader |
| A live create or update is requested | Require the current template-backed immutable CSV package, exact approval, one core.data-loader task-level import, and process-log verification before reporting a result |
| A direct REST create or update is requested | Stop as unsupported; do not send REST POST, PUT, or PATCH for person security profile configuration |
| Parent ManagerTypes cannot be exactly resolved | Stop before preview and request a permitted parent selection from PER_PRSN_SEC_PROF_MGR_TYPES |
| hierarchy_content cannot be exactly resolved | Stop before preview and request an enabled hierarchy-content value from PER_PRSN_SEC_PROF_MGR_HIER_FOR. Delegating manager hierarchy is hierarchy content, not a supervisor type. |
| A specific supervisor type is requested but parent ManagerTypes is not SELECTIVE_MGR, the derived manager-type child row is absent or differs, or ManagerTypeValue cannot be exactly resolved | Stop before preview; set parent ManagerTypes to SELECTIVE_MGR, create exactly one manager-type child row, and request the enabled supervisor type from PER_SUPERVISOR_TYPE |
| supervisor_type conflicts with requested_manager_type or legacy manager_type | Stop before preview and request one consistent supervisor type and parent selection; do not silently apply the LINE_MGR default |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Blocked | Any supplied configuration fails a documented business rule or the CSV layout resolver cannot establish the package contract | Correct the configuration or export and resolve the current template-only package, then restart validation |
| Approval blocker | The exact CSV package preview has not been approved | Stop before core.data-loader |
| Process failed | core.data-loader import returns a failure or does not produce a verifiable process log | Persist the sanitized diagnostic and process-log reference; do not retry the import automatically |
| Ready | The configuration passes validation, defaulting, and design enforcement | Continue to the task's separately authorized preview and execution workflow |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Blocked validation | The failed rule, affected criterion or person type, exclusion-rule count when applicable, and the permitted correction |
| Similar-profile AOR review | Matching profile Names, the shared work-structure criterion set, the exact AOR scope recommendation when one exists, and the explicit exception confirmation required to continue |
| Specific work-structure access request | State that Areas of Responsibility controls access to a specific legal employer, business unit, department, position, LDG, or payroll and that appropriate AOR assignments are required; continue with CSV package creation |
| Ready validation | The applied AssignmentsToEvaluate default when used and the validated configuration constraints |
| CSV import failure | The failure class, task name, process identifier when available, last status, sanitized diagnostic, and safe next action |
| Any response | Do not display internal IDs, including profile, child-row, lookup, process, request, content, or data-set identifiers; retain them only in sanitized internal evidence when needed |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A person security profile create or update is requested | Do not use REST POST, PUT, or PATCH; prepare, approve, and submit the current template-backed CSV package through core.data-loader only |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PSP.ERROR | terminal | 9 | terminal | none | none | stop | A validation, lookup, dependency, or design-enforcement rule is blocked |
| PSP.READY | terminal | 10 | terminal | none | PSP.CSV_READINESS | stop | Person security profile validation, CSV layout readiness, and design enforcement are compliant |
