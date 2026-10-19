# Learning Catalog Skill: Findings and Migration Decisions

Date: 2026-09-22

## Stage Status

Stage 1, Stage 2, and Stage 3 are complete for the canonical Learning Catalog
parent and these four nested task skills:

| Taxonomy task | Task code | REST business object |
| --- | --- | --- |
| Self-Paced Learning | `CUSTOM_SELF_PACED_LEARNING` | `learningSelfPacedItems` |
| Events | `CUSTOM_EVENTS` | `learningEvents` |
| Courses | `CUSTOM_COURSES` | `learningCourses` |
| Learning Paths | `CUSTOM_LEARNING_PATHS` | `learningPaths` |

The canonical parent skill ID is
`hcm.learning-management.learning-catalog`, and the functional-area code is
`ORA_LEARNING_CATALOG`.

The implementation is versioned at `1.0.0`. All five manifests conform to the
repository schema, all four rule registries compile with 10 ready nodes, and
all four execution plans validate without a readiness override. The final
behavioral contract suite passed 12 tests, the resource-authoring suite passed
32 tests, and all five automated skill audits reported zero findings. The
scoped diff check also passed. The generator's own unit suite could not start
in the available Python runtimes because its external `jsonschema` dependency
is not installed; this does not change the successful manifest validation
performed by the contract tests and skill auditor.

## Sources Reviewed

- [Approved Learning taxonomy](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/learning-taxonomy/),
  with the user-supplied `learning-taxonomy.csv` and the effective catalogs as
  the repository-verifiable fallback.
- Approved Learning guide-skill baseline, last verified in this workstream on
  2026-09-18.
- Jira `OLC-116681`, Learning Catalog Setup Skill.
- [OLC-116681 FDD](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21981496001),
  version 5, updated and reviewed 2026-09-22.
- `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`.
- `knowledge/setup-task-catalog/effective/setupTasksAll.json`.
- Current Oracle Fusion Cloud HCM REST documentation for Self-Paced Learning
  and Events.
- Eight developer-supplied raw Oracle Describe payloads. They were treated as
  target-scoped data; environment hosts and payloads were not committed.
- The prior enriched Learning Catalog implementation in Git `HEAD`, used only
  as behavior evidence for the canonical migration.

## Generator Dry-Run Results

Both read-only dry runs passed against the refreshed effective catalog.

The parent-only run proposed:

```text
pillars/hcm/learning-management/learning-catalog/SKILL.md
```

The scoped run used four explicit `--task-skill` inputs, `REST` import mode,
and the business-object mappings in the table above. It proposed:

```text
pillars/hcm/learning-management/learning-catalog/SKILL.md
pillars/hcm/learning-management/learning-catalog/self-paced-learning/SKILL.md
pillars/hcm/learning-management/learning-catalog/events/SKILL.md
pillars/hcm/learning-management/learning-catalog/courses/SKILL.md
pillars/hcm/learning-management/learning-catalog/learning-paths/SKILL.md
```

Neither run proposed a deletion or emitted a conflict. The generator supplied
the canonical identity scaffold, but its generic planning manifests did not
contain the previously authored orchestration, validation, approval, or
resource behavior.

## Migration Decision

The requester confirmed that deletion of the 34 legacy Learning Catalog
artifacts was intentional because they used superseded taxonomy identities.
The approved migration therefore:

- creates the canonical parent and four canonical child paths;
- carries forward source-grounded behavior from Git `HEAD` without restoring
  superseded paths or identifiers;
- preserves the four REST business objects and task-local rule graphs;
- recompiles each registry from its canonical manifest and Markdown rule
  sources instead of copying an old compiled identity;
- treats FDD `Manage ...` story titles as provenance, not task identity; and
- major-versions the migrated orchestration contracts at `1.0.0`.

The current `pillar-skill-gen` must not be used as an ordinary reentrant
refresh of the enriched package. It identifies tasks by current catalog code,
does not move task-local resources, and replaces enriched frontmatter with a
generic manifest. Any future addition requires a reviewed dry run, an isolated
canonical scaffold, preservation of existing authored behavior, and full
manifest/resource/contract/auditor verification.

## FDD v5 Coverage

FDD version 5 supplies these in-scope acceptance groups:

- Self-Paced Learning (`OLC-120241`, `SPL-AT-01..09`): missing inputs,
  supported content creation, invalid content or processing, private publish,
  replacement, lifecycle and deletion, mixed-row batches, stale approval, and
  capped demonstration generation.
- Events (`OLC-120242`, `EVT-AT-01..08`): missing identity, creation and
  activation, schedule/resource/capacity errors, active-event rescheduling,
  lifecycle requests, duplicate-to-Draft, mixed-row CSV, and stale evidence.
- Courses (`OLC-120243`, `CRS-AT-01..08`): missing identity, Draft creation,
  invalid children, activation readiness, assignment-safe updates, copy and
  retirement, mixed-row uploads, and stale relationships.
- Learning Paths (`OLC-120244`, `LPT-AT-01..08`): missing identity or
  structure, valid multi-section paths, membership and graph errors,
  activation readiness, active-path changes, renewal and validity, grouped
  graph batches, and stale child or path state.

FDD v5 also supplies detailed Official Communities (`OLC-120245`), Categories
(`OLC-120246`), and Topics (`OLC-120247`) sections. Those tasks remain deferred
from this four-task migration and do not receive placeholder or executable
routes here.

## Raw Describe Reconciliation

The primary resource inventories are:

| Resource | Nodes | Attributes | LOV-decorated | Queryable |
| --- | ---: | ---: | ---: | ---: |
| learningSelfPacedItems | 20 | 410 | 77 | 300 |
| learningEvents | 21 | 365 | 56 | 283 |
| learningCourses | 15 | 307 | 46 | 252 |
| learningPaths | 16 | 292 | 41 | 239 |

They confirm:

- Self-Paced Learning collection and item CRUD, publish, reprocess, content
  CRUD, exact finders, required fields, defaults, and LOV routes.
- Event collection create/read, item update/read, copy, activity CRUD, exact
  finders, required fields, defaults, and LOV routes. Finalize and parent
  delete are absent.
- Course collection create/read, item update/read, copy, activity
  create/update, exact finders, defaults, and LOV routes. Parent and activity
  delete are absent.
- Learning Path collection and item CRUD, section CRUD, nested-activity CRUD,
  exact finders, defaults, and LOV routes. Copy is absent.

The normalized guidance must not invent absent
`learningItemSourceId`, `learningItemSourceType`,
`learningItemSourceInformation`, `learningItemObjective`, or
`learningItemIdealLearner` REST fields. Self-Paced content uses the actual
content-level source, launch URL, provider, scoring, language, and publication
fields. Objective or ideal-learner requests remain preview-only when no
writable REST representation exists.

The validation-resource inventories are:

| Resource | Nodes | Attributes | LOV-decorated | Queryable |
| --- | ---: | ---: | ---: | ---: |
| hcmLists | 1 | 16 | 0 | 15 |
| learningTrainingSuppliers | 3 | 64 | 3 | 49 |
| learningInstructors | 5 | 96 | 9 | 80 |
| learningClassrooms | 5 | 142 | 4 | 99 |

These resources are read-only validation dependencies. They resolve list,
supplier, instructor, classroom, capacity, schedule-availability, and generic
provider-account evidence. They do not create additional Learning Catalog
management tasks or authorize association writes.

## Resolved Blockers and Scope Decisions

- Access Groups is not part of the current release.
- Catalog Administration Profiles is assigned to a separate transaction after
  this migration merges.
- Official Communities, Categories, and Topics are deferred even though FDD v5
  now contains their detailed requirements.
- General Self-Paced and Event public REST contracts are resolved.
- General Course and Learning Path read/write contracts are resolved for the
  described preproduction target.
- HCM list identity and active-state lookup is resolved through read-only
  `hcmLists`; Learning-specific association writes are not inferred.
- Event supplier, instructor, classroom, availability, capacity, and generic
  virtual-account validation are resolved through the supplied target
  resources.
- Course default-instructor and type-routed facilitator identity validation is
  resolved.
- No payload advertises ETag or `If-Match`. Immediate pre-write readback,
  immutable fingerprints, single-submit writes, no automatic retry, and
  post-write reconciliation remain mandatory.

## Remaining Request-Scoped Gates

These gates do not block generation or unrelated operations:

- Owner or coordinator labels require an authoritative person resolver before
  they can become writable technical values.
- A Self-Paced language label requires a live mapping to the accepted request
  representation.
- Event ad hoc resources remain blocked without an authoritative availability
  resolver.
- Provider-specific webinar requests stop when `validateProviderUser` input or
  success semantics remain opaque or indeterminate.
- Course requests that add children remain gated on child eligibility and
  course-versus-path exclusivity evidence.
- Learning Path requests that add or replace activities remain gated on
  authoritative activity eligibility and relationship evidence.
- Enabled LOV values, Data Loader registration, security associations, and
  target-specific DFF segments require current target metadata.
- The optional Learning Catalog Assistant remains non-executable until its
  provider contract and configuration readiness are confirmed.

Each gate applies only when its associated capability is requested. None of
these gates permits fabricated identifiers, inferred write contracts, or a
write that bypasses preview and fresh approval.
