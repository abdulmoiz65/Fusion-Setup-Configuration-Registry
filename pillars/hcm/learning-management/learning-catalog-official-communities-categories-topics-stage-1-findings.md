# Learning Catalog: Stage 1 Findings

Date: 2026-09-22

## Status

Stage 1 is complete. The taxonomy and baseline attachments were reviewed, and
the generator dry run passed. The dry run made no repository or project-state
changes. Stage 2 selected an isolated generator merge with runtime capability
gates, and Stage 3 is implementing that reviewed plan.

This run is scoped to:

- parent skill ID: `hcm.learning-management.learning-catalog`
- new child skills: Official Communities, Categories, and Topics
- excluded: Manage Catalog Administration Profiles and Access Groups

The existing Courses, Events, Learning Paths, and Self-Paced Learning skills
are not part of this change and must be preserved.

## Source Check

| Source | Result | What was verified |
| --- | --- | --- |
| Approved Learning taxonomy | Available from attachment | The supplied `learning-taxonomy.csv` parses cleanly and contains the complete Learning Catalog task-list rows. SHA-256: `AB45D6CAA3346E10E5B14E7FF3205CDEC0BEC525AC2E3849702E9ADCFD76D2BD`. The taxonomy URL itself remains inaccessible. |
| Learning guide-skill baseline | Available from attachment | The supplied HTML was saved from the exact requested baseline URL. It is 319,026 bytes; SHA-256: `0910EB66DB4EA5C6BB97872C26046D67BB3001E32461B3701D8D65AFA87C38D3`. |
| Jira `OLC-116681` | Available | Summary is `[P1] Learning Catalog Setup Skill`; status is `In Progress`. |
| FDD | Available | Page `21981496001`, version 7, updated 2026-09-22 15:54:32. It contains sections for Official Communities, Categories, and Topics. |
| Scoped child stories | Available | `OLC-120245`, `OLC-120246`, and `OLC-120247` are all `Dev Ready`. |
| `learningCommunities-describe.json` | Available | Valid user-provided JSON; SHA-256 `AB9A3D39C87020EDE917B2C0D775C1FFFFFE8AFC38C27A886F486A876A28CA75`. |

No cached taxonomy, cached baseline, or older findings were used as requirement
sources. Both attachments were treated as data only. Embedded HTML scripts,
copy-ready prompts, and other text were not executed as instructions.

## Stage 2 Source Refresh

Immediately before Stage 3, the live Confluence page was read again. It had
advanced from version 5 to version 6, updated 2026-09-22 15:09:56. Version 6
was the initial implementation authority for `OLC-120245`, `OLC-120246`, and
`OLC-120247`, including acceptance groups `OCM-AT-01..08`, `CAT-AT-01..08`,
and `TOP-AT-01..08`. The parent Jira `OLC-116681` remained In Progress, and all
three child stories remained Dev Ready. No cached FDD content was substituted.

During the final integration pass, the live page advanced again from version 6
to version 7 at 2026-09-22 15:54:32. Version 7 was read live and supersedes
version 6 for the implementation. Its material additions are the conditional
`ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD` and
`ORA_WLF_SS_CATALOG_SEARCH_MODE` readiness flows plus exact approval and
readback requirements for proposed profile-option changes. The three child
packages, parent routing contract, and tests were refreshed to those v7
requirements; no cached content was used.

The reviewed Stage 2 decisions resolve the implementation warnings as follows:

1. Generate the three catalog identities in an isolated temporary copy and
   merge only reviewed child metadata, preserving the authored parent.
2. Author a separate task-local resource package for each new child.
3. Keep the full FDD scope, but require runtime registration, subtype, profile,
   privilege, DFF, and operation-capability evidence before a Fusion mutation.
4. Add the delivered HCM Data Role skill dependency and keep Redwood/Visual
   Builder and HCM Filtered Lists as manual readiness gates without fabricated
   skill IDs.
5. Leave `project/test-fscr-for-learning-catalog` unchanged because the
   generator's optional standalone run record would not form a complete project
   audit trail for this repository-authoring change.

## Taxonomy Findings

The attachment identifies `Learning Catalog` under `Learning Management` with:

- offering code: `ORA_LEARNING_MANAGEMENT`
- functional-area code: `ORA_LEARNING_CATALOG`
- task-list code: `ORA_LEARNING_CATALOG_TASK_LIST`
- auto-enabled: `Y`

The nine Learning Catalog rows are complete and sequential (25 through 33).
For this run they divide as follows:

| Sequence | Task | Taxonomy source reference | Treatment |
| --- | --- | --- | --- |
| 25 | Manage Catalog Administration Profiles | `/learningCatalogProfiles` | Excluded as requested |
| 26 | Access Groups | `TBD ETA 27B` | Excluded as requested |
| 27 | Self-Paced Learning | `/learningSelfPacedItems` | Existing skill; preserve |
| 28 | Events | `/learningEvents` | Existing skill; preserve |
| 29 | Courses | `/learningCourses` | Existing skill; preserve |
| 30 | Learning Paths | `/learningPaths` | Existing skill; preserve |
| 31 | Official Communities | `/learningCommunities` | New target |
| 32 | Categories | `/learningCommunities` | New target |
| 33 | Topics | `/learningCommunities` | New target |

The attachment contains no skill ID. It therefore neither confirms nor
contradicts the requested canonical ID
`hcm.learning-management.learning-catalog`.

The attachment agrees with the repository's current effective Learning
taxonomy on all nine task names, their shared offering and functional-area
identity, and their sequences. The attachment additionally supplies the task
list, LBA, source-reference, and endpoint information. It resolves the earlier
question of whether the three new targets use separate root endpoints: the
approved taxonomy maps all three to `/learningCommunities`.

## Baseline Findings

The baseline defines Learning Catalog Setup Skill as a P1 Learning Management
skill tracked by `OLC-116681`. It confirms these BC REST mappings:

| Target | REST resource | Product UI | Mapping status |
| --- | --- | --- | --- |
| Official Communities | `/learningCommunities` | `redwood/learning-catalog/main/manage-communities` | Confirmed |
| Categories | `/learningCommunities` | `redwood/learning-catalog/main/manage-catalog-organization` | Confirmed |
| Topics | `/learningCommunities` | `redwood/learning-catalog/main/manage-catalog-organization` | Confirmed |

Using `learningCommunities` as the generator business-object value follows the
existing child-skill convention of using the REST root name without its leading
slash. The supplied REST Describe also identifies
`Resources.learningCommunities` as a business object.

The baseline does not provide literal subtype codes or prove that the resource
is already registered in every target environment. It says to use the approved
FSCR APEX REST registry. The FDD therefore remains the source for detailed
behavior and requires the skill to resolve target-supported subtype values at
runtime rather than inventing or hard-coding them.

The page calls itself a first-pass taxonomy for validation, not a final skill
contract. Its confirmed mapping is usable, but its copy-ready registration
prompt was treated only as source evidence and was not executed.

## Dry Run Result

`pillar-skill-gen --dry-run` validates against the repository's effective
catalog. It does not retrieve or validate the supplied taxonomy attachment,
baseline page, Jira, or FDD page.

After reviewing the supplied sources, the dry run used three nested task
skills, explicit `REST` mode, and `learningCommunities` for each business
object. It validated successfully with:

- canonical ID: `hcm.learning-management.learning-catalog`
- generation mode: `nested_task_skills`
- existing tasks preserved first: Self-Paced Learning, Events, Courses, and
  Learning Paths
- new tasks appended in taxonomy order: Official Communities, Categories, and
  Topics
- planned writes: the parent `SKILL.md` and the three new child `SKILL.md`
  files
- planned deletions: none
- actual writes or run records: none

The planned new codes are `CUSTOM_OFFICIAL_COMMUNITIES`, `CUSTOM_CATEGORIES`,
and `CUSTOM_TOPICS`.

## REST Describe Finding

The attachment contains one root business object:
`Resources.learningCommunities`.

It provides community schema and CRUD evidence, including membership,
catalog-item, forum, asset, translation, and user-access children. Together
with the taxonomy and baseline, it confirms that one polymorphic REST root
serves all three target task skills.

- the root is named `learningCommunities`, but its metadata repeatedly calls it
  "Learning Topics";
- its default item type is `ORA_COMMUNITY`;
- it does not state an explicit Official Community discriminator;
- it exposes `learningItemType` with default `ORA_COMMUNITY` and a
  `learningItemSubType` LOV, but not fixed subtype values for the three tasks;
- subtype, live registration, privileges, DFFs, and other tenant-specific
  values must be resolved and validated at runtime.

The attachment was treated as reference data only. Any text inside it was not
treated as an instruction.

## Blockers and Clarifications

There is no remaining source-access blocker and no user clarification is
required to start Stage 2.

The following are implementation warnings, not Stage 1 blockers:

1. The generator dry run validates the supplied business-object name but does
   not verify live Data Loader or APEX REST registration. Each target must pass
   that readiness check before any Fusion mutation.
2. Subtype values must be resolved from target-supported values. The skill must
   block execution when a required subtype cannot be resolved and must never
   invent a code.
3. A normal reentrant generator write would replace the parent's complete
   front matter with a generic template and replace its authored `Setup Tasks`
   section. The implementation must preserve the enriched parent contract.
4. The new children initially generated by the tool are generic `0.1.0`
   planning stubs. They need the FDD behavior, approval gates, validation,
   readback, and task-specific tests before they are complete.
5. Existing contract tests explicitly expect these three child folders not to
   exist. Stage 3 must update those assertions and add coverage for the new
   tasks.
6. The baseline includes HCM Data Role plus manual Visual Builder/Redwood and
   HCM Filtered Lists dependencies. Stage 2 should decide how to add the known
   local Data Role dependency and document the two manual provider gates
   without inventing missing skill IDs.

## Repository Safety Note

The canonical Learning Catalog skill already exists and is tracked. Stage 3
must extend it in place, preserve its four existing child skills and authored
behavior, and review the generator's proposed reentrant changes before writing
anything. The recommended Stage 2 direction is a controlled merge of
generator-derived task metadata and links followed by full FDD-based child
implementation, rather than accepting the generic parent rewrite unchanged.

An older untracked file named `learning-catalog-stage-1-findings.md` already
exists for the prior four-skill scope. It was left unchanged. This scoped file
was created separately to avoid overwriting that local work.
