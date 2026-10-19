# Person Section Submission Readiness

Use this checklist for a new Person section before promising an immutable
preview or interpreting a general “submit” instruction as executable approval.

## Separate the Three Contracts

1. **Read-only discovery:** `ptcs.read-only-verification` can verify an exact
   template, section, flags, properties, and requested catalog/subscriber
   references. Its report is not a Task Hook validation envelope.
2. **Native FSM transport:** the task metadata selects FSM, and the existing
   Core Data Loader task adapter owns validated archive submission. Do not
   invent a direct content-section POST or a replacement provider.
3. **Person package semantics:** a transport exists, but it does not prove that
   a proposed native archive correctly creates this Person section, preserves
   its references, or implements future activation. These are required evidence,
   not defaults and not cleared by login or GET success.

## Evidence Needed Before an Immutable Preview

| Gate | Required evidence | If missing |
|---|---|---|
| Business scope | Reviewed target environment, proposed section name, employee population, approval behavior, start date, and exclusions | Retain the proposal for review |
| Exact template and target | Fresh complete GET results for the predefined template and exact Person section; distinguish not_found from blocked | Run only the declared diagnostic workflow |
| Native source | A validated source Profile Types FSM archive and the exact Person Certification source section/template business keys; the generic member inventory alone is insufficient | Request the source artifact, or propose a separately approved export; never export automatically |
| Field mapping and operation support | Validated native HRT_MANAGE_PROFILE_TYPES metadata and headers, deterministic Person business-key mapping, complete runtime template/property rows, optional subscriber closure, ImportSupportedFlag=Y, and the exact readback contract | Stop when any candidate-specific evidence is missing; do not copy Job parent rules into Person or treat generic transport support as proof that an invalid package is safe |
| Employee presentation | Exact predefined Talent Profile subscriber and existing employee access verified through their owning supported workflows | Report the dependency; do not silently omit it or create security assignments |
| Approval behavior | Supported Approval Required flag mapping and existing approval workflow prerequisites; disclose that the documented flag also covers deletions | Review any material difference from the requested behavior |
| Activation timing | Supported evidence for the requested start date at content-section setup level | Never substitute item date fields or enable immediately; retain timing as unresolved |
| Full archive scope | Only reviewed Person-section rows and required references/children/translations; unchanged native metadata marker | Reject unrelated source rows and synthetic blank ZIPs |
| Execution and readback | Task Hook rules pass for the immutable archive; Core Data Loader approval binds exact environment and archive SHA-256; declared readback covers every changed value | Stop before submission; readback gaps are not successful persistence |

Do not present a CSV/ZIP as ready merely because it parses. Do not enable a
section today and claim it begins on a future date. Deferred execution or
inactive preparation may be proposed as alternatives only with a reviewed
business decision and a confirmed supported operation; neither schedules a
later action automatically.

## Source Boundaries

The user-supplied HAR demonstrates a Person Language section transaction and
related reads. It does not establish Certification-specific native FSM
construction, future-dated activation, or an approved submission payload.
An older Job package establishes only its demonstrated schema/relationships.
Do not treat either as approval to replay a request or copy unrelated rows.

Oracle documents predefined-template creation, the Active and Approval Required
controls, and the Talent Profile subscriber requirement. The cited pages do
not establish a scheduled-activation field or the task's complete native CSV
construction contract. Keep those distinctions visible.

- [Content Sections](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/content-sections.html)
- [Content Section Properties](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/content-section-properties.html)
- [Native package contract](fsm-profile-types-package.md)
- [Core Data Loader](../../../../../core/data-loader/SKILL.md)

The mandatory implementation Task Hook graph remains fail-closed whenever its
candidate-specific capability, package, reference, approval, or readback
evidence is missing. The standalone diagnostic workflow is not permission to
override that graph or to substitute a different executor.
