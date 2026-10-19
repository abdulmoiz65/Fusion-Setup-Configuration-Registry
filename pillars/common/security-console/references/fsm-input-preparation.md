# Prepare Security Console FSM Inputs

Use this guide for custom roles, duties, data-security policies, HCM provisioning
rules and LDAP account options. Each task owns its own objects and archive;
never substitute one task's files for another's.

## Help users who do not have a template

Accept the intended create, update, delete or redesign change in plain language.
Users do not need to supply an archive, know CSV column names or fill a template
before the workflow can start. Capture exact business values and the target
environment; ask only for genuinely missing business choices.

1. Resolve the task and current CSV support through
   `shared.setup-export.task-level-export`, using the active project context.
2. Obtain the selected task's template/spec package through that skill. A
   necessary template/spec export is automatically authorized for a requested
   change; do not add a separate confirmation. This exception does not authorize
   populated data exports, imports, deletion or uncertain-write retries.
3. Preserve the downloaded template. List its files and extract only safe,
   relative members into a new project folder. Reject absolute paths, traversal,
   links, duplicate member names, encryption or overwrite conflicts. Keep the
   original XML metadata and CSV headers, ordering and encoding intact.
4. Read any supplied specifications and explain each required file and field
   in business terms. Map the user's values into a separate candidate using the
   actual template. Show a small populated example or field-to-value table when
   the user needs guidance. Do not alter the original supplied file.
5. Derive technical codes from documented mappings or a verified same-task
   reference; preserve explicit user-confirmed mappings. Ask only about values
   that remain unresolved. Never substitute an unrelated role, policy or rule.
6. For updates or redesign, establish the exact existing identity and preserve
   unrelated fields and relationships. Use an approved scoped export or supplied
   baseline where needed; automatic template approval is not data-export approval.
7. Assemble the task's supported candidate archive before validation. Compare
   member names, headers, fields and relationships with the template. Report
   proposed changes and unresolved inputs; once validated, preserve the candidate.
8. Route shared validation to `shared.validation.setup-data-validator` and all
   upload/import actions to the persistent `core.data-loader` session. Data
   Loader owns Task Hook checks, the final immutable preview and import approval.
   Follow its memory and output rules; do not persist session snapshots or approvals.

Template acquisition and intentional configuration changes in the target are
not same-environment restores. Apply restore confirmation only when restoring
exported configuration to its source environment.

## Create, update, delete and redesign

Accept all four operation intents for the objects owned by the selected task.
Use only supported fields and operations from current Oracle guidance and the
target's contract. A request is not rejected merely because it is an individual
object change instead of a migration, or because the user lacks a CSV file.

For deletion, identify exactly which object or relationship is to be removed.
Use an explicit documented deletion/removal action. An omitted row or empty
cell does not establish deletion. A membership REMOVE does not delete its role.
If whole-object deletion is not supported or its contract is unavailable, record
the precise operation-support gap and next action. Do not invent DELETE flags,
change the schema, or substitute browser, REST, SCIM, HDL or another task.

For redesign, prepare the before/after fields and explicit additions/removals.
Do not silently change unrelated security scope. Seeded objects remain protected
unless the applicable Oracle contract permits the requested operation. Only
templates are automatically authorized; actual changes use Data Loader approval.

## Oracle references and task-specific limits

- [Role CSV contents](https://docs.oracle.com/en/cloud/saas/sales/oscus/export-and-import-of-custom-roles-role-hierarchies-and-role-to.html)
  describes role details, hierarchy and privilege memberships. Direct data-security
  policies are excluded from the Manage Job Roles package.
- [Edit role CSV packages](https://docs.oracle.com/en/cloud/saas/human-resources/ochus/manage-role-definitions-using-csv-file-packages.html)
  documents ADD/REMOVE membership actions and unchanged metadata. It does not
  establish a whole-role deletion action.

For other tasks, consult their own current Oracle contract and live template;
do not copy the Job Roles columns or ADD/REMOVE rules into another object schema.
