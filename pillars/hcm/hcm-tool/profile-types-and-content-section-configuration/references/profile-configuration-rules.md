# Profile Configuration Rules

## Category and Scope

Resolve the requested target against the exact Profiles V2 seeded type mapping
in [Oracle Profile Configuration Scope](oracle-profile-configuration-scope.md).
Do not propose or import a new custom parent profile type: only the eight seeded
types in that mapping are visible in Profiles V2. UI visibility does not grant
operation support, so confirm the requested type-and-operation combination from
the provider or FSM contract before preview or execution.

Person profile types define worker and non-worker profile data. Model profiles
define Job, Position, Organization, and Prerequisite structures; use only
Job-to-Job, Position-to-Position, and Organization-to-Organization associations.
Person content sections may be added from predefined templates only where the
operation is confirmed as supported. A supported non-Person content section is
instead based on its corresponding active Person section.

For every supported seeded profile type other than Person, require one
corresponding active Person content section before the target section can be
configured. The relationship is unique within the target profile type: the
same Person section can support one section in Job and one in Position, for
example, but not two Job sections. The skill owns dependency discovery and
disclosure. If the Person section is absent, ask for explicit approval to add
that prerequisite to scope, then pass the approved parent-and-target intent to
the FSM processing layer. The skill does not construct the Person section or
enforce FSM row ordering and uniqueness itself. Scope approval does not replace
Core Data Loader's approval for the final immutable package.

## Exact Duplicate Handling

Check every proposed content section by exact seeded profile type and section
context. The duplicate gate clears only when every proposed section has zero
exact matches. One duplicate anywhere rejects the complete ZIP, including any
otherwise-new sections in it. Do not update, merge, overwrite, resubmit, add
child rows, or partially import that archive. Disclose the duplicates and
continue only with a newly prepared ZIP that excludes them and completes a new
validation, preview, and approval cycle. Multiple exact rows for one candidate
are ambiguous and also reject the complete ZIP.

## Content, Subscribers, and Ratings

Create a Person content section only from a resolved predefined template. Create
a supported non-Person content section only from a resolved corresponding active
Person section. Preserve the leading attribute after creation. Configure
subscriber attributes only when the property is Summary or Detail, never Hide.
Create each requested section-to-subscriber assignment through one exact
`ORA_HRT_PROFILE_TYPE_CONTENT_SOURCE` relationship. Subscriber-property rows
configure that assignment but never create it, so reject an archive whose
property rows have no exact content-source parent.
Content library, item catalogs, value sets, flexfields, and rating models are
prerequisites, not outputs.

For Person Profile Talent Ratings, configure delivered ratings or create at most
five custom ratings from an existing rating model. A custom rating cannot be
deleted; make it inactive instead. Its employee/manager access requires a
separate Content Section Access assignment. Manager-facing ratings and skills
require read-only verification of `ORA_HCM_VBCS_PWA_ENABLED=Y` and
`HRC_ELASTIC_SEARCH_ENABLED=Y`.

## Access and Synchronization

Content Section Access applies to person profiles. Resolve only predefined or
custom job/abstract roles and View, Edit, or Report access; Edit includes View
and Report. Role mapping grants data security, while regeneration remains an
external handoff.

Do not enable job-to-position synchronization by default. An explicit request
requires a current-state lookup, an impact warning for add/update/delete effects,
and separate approval; this skill never runs it.

## Sources

- [Profile Management Components](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/profile-management-components-how-they-work-together.html)
- [Talent Profiles](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/talent-profiles.html)
- [Model Profile Types](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/model-profiletypes.html)
- [Model Profile Content Sections](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/model-profile-content-sections.html)
- [Profile Talent Ratings](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/profile-talent-ratings.html)
- [Talent Ratings Templates](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/talent-ratings-templates.html)
- [Content Section Access](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/content-section-access.html)
- [Synchronization Rules](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/rules-for-synchronization.html)
