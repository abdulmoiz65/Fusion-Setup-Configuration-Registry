# Learning Resources Dependency Handoffs

Source: [Learning Management Guide Skill Baseline](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/learning-guide-skill-baseline/), Learning Resources Setup Skill (`OLC-116674`).

## Baseline Dependency Map

| Baseline dependency | Current FDOS provider | Status | Activation condition | Evidence required before Learning Resources resumes |
|---|---|---|---|---|
| Application Value Set Foundation Skill | `core.fusion-api.apps-common.value-sets` | Enabled | A selected resource field or configured flexfield depends on a value set | Resolved value-set code and validated value evidence |
| Application Flexfield Foundation Skill | `core.fusion-api.apps-common.descriptive-flexfields` | Enabled | A resource DFF context or segment is configured, required, or supplied | Deployed context, segment metadata, requiredness, and accepted value evidence |
| HCM Security Profile Setup Skill | `hcm.hcm-security.hcm-security-profile` | Manual baseline handoff | Required worker, resource, or reference data is hidden by HCM data security | Applicable profile identifier, scope, validation result, and accessible read-back |
| Locations Setup Skill | `hcm.global-human-resources.locations.manage-locations` | Manual baseline handoff | A Classroom row has no exact accessible active HCM Location with address details | LocationId or LocationCode, name, address, Active status, and successful `locationsLov` read-back |
| Visual Builder and Redwood Extension Foundation Skill | No exact provider skill delivered | Manual baseline gap | The requested outcome changes Redwood page properties, layouts, or business rules | Explicitly selected manual provider route and verified deployed behavior; do not substitute another skill automatically |
| HCM Data Role Setup Skill | `hcm.hcm-security.hcm-data-role.assign-security-profiles-to-role` | Enabled | A completed security profile must be assigned to the implementation or integration role | Role, assigned security profiles, effective user assignment, and access validation |

## Handoff Rules

1. Query and validate the current dependency before proposing a change.
2. Do not run an unrelated dependency merely because it appears in the baseline.
3. Preserve the blocked Learning Resources row and its user-supplied values while a dependency is resolved.
4. A manual dependency requires an explicit routed subflow; it is not permission for the consuming skill to mutate the provider's setup.
5. Resume the consuming task only after the provider returns the evidence in the table and the consuming task independently reads back the resolved reference.
6. Record unavailable providers as a blocker with one concrete next action. Do not replace a missing provider with a similarly named skill or direct REST mutation.

## Classroom-to-Location Handoff

`Manage Classrooms` owns the classroom request; `Manage Locations` owns location creation or correction.

1. `Manage Classrooms` searches `locationsLov` using the supplied location ID, code, or name and completes all pages needed for an exact match.
2. When one accessible active location with address details resolves, the classroom proceeds without invoking the provider skill.
3. When no eligible location resolves, the classroom row becomes blocked and is handed to `hcm.global-human-resources.locations.manage-locations` with the requested location details and project context.
4. Location setup follows its own validation and approval workflow.
5. After location completion, `Manage Classrooms` repeats `locationsLov`; provider output alone is not sufficient.
6. The classroom resumes only when exactly one eligible location is returned. Ambiguous, inactive, inaccessible, or addressless locations remain blocked.

An ad hoc classroom address is not a substitute for this dependency in the `learningClassrooms` Data Loader route.
