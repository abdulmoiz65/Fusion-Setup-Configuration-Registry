# Oracle Profile Configuration Scope

## Profiles V2 Seeded Type Identity

Profiles V2 shows only the following seeded profile types. Use this table as
the authoritative UI visibility allowlist for this skill.

| Seeded Type ID | Seeded Type Key | Display Label |
|---:|---|---|
| 1 | PERSON | Person |
| 2 | JOB | Job |
| 3 | POSITION | Position |
| 4 | ORGANIZATION | Organization |
| 5 | TEMPLATE | Template |
| 10 | REQUISITION | Requisition |
| 11 | PREREQUISITE | Prerequisite |
| 12 | GUIDE | Guide |

UI visibility and operation support are separate contracts. A seeded type may
be displayed while create, update, content-section configuration, or FSM import
for that type remains unsupported or unconfirmed. Require the active provider
or FSM contract to authorize the requested operation for the selected seeded
type; otherwise stop before immutable preview or execution.

Do not treat the seeded key as `HRT_PROFILE_TYPES_B.ProfileTypeCode` or
`ProfileUsageCode`. `ProfileTypeCode` is the profile-type business key in the
FSM CSV, while `ProfileUsageCode` is a usage classification. If input supplies
both a seeded type ID and seeded type key, require the exact pair shown above.
Do not create a custom parent profile type because it won't be visible in
Profiles V2.

## In-Scope Configuration

Oracle documents that the Profile Definition page provides profile name,
description, active status, and person-profile autocreation. For Person, an
administrator can create multiple content sections from predefined templates;
model-profile content sections are selected from sections already defined for
Person. The skill then configures the selected section's supported properties
within the target profile type.

The documented content-section controls include section name, description,
active state, default behavior, display order, approvals, property display,
subscriber configuration, and supported descriptive-flexfield references.
Content section access is configured through the Profile Content Section Access
task and remains part of the same business proposal when supplied.

For every supported non-Person target, select a corresponding active Person
content section before target-section property customization. The skill checks
and discloses this prerequisite. When it is absent, obtain explicit approval to
include the Person section in scope and delegate construction, ordering, and
uniqueness handling to the confirmed FSM processing layer.

## Exclusions and Dependencies

Do not invent or create a template. Item catalogs, value sets, profile options,
security roles, flexfield definitions, ratings, lookups, and regeneration remain
separately owned dependencies. A leading attribute cannot be changed after the
content section is created. Create, exact-search, immutable-preview, approval,
and readback remain blocked until their HCM Tool provider contract is confirmed.

## Sources

- Profiles V2 seeded UI mapping supplied by the HCM pillar contributor on
  2026-09-04.
- [Profile Definition](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/person-definition.html)
- [Content Sections](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/content-sections.html)
- [Content Section Properties](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/content-section-properties.html)
- [Profile Type Sections REST Resource](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-profiletypesectionslov-get.html)
