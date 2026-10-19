---
task_code: "ORA_FND_MANAGE_INDEX_CONFIGURATION"
task_name: "Manage Search Indexes"
parent_skill_id: "hcm.learning-management.learning-management-common"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Management Common"
functional_area_code: "ORA_LEARNING_MANAGEMENT_COMMON"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Search Indexes

## Setup Task Metadata

- Task name: `Manage Search Indexes`
- Task code: `ORA_FND_MANAGE_INDEX_CONFIGURATION`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: ``

## Learning Scope and Execution Gate

Read [the Common skill](SKILL.md), its selected provider contract and the task's
compiled resource plan before using this metadata. Catalog availability and
CSV/export flags are not execution approval. Index enablement, initial ingestion and HCM Tool Search Views are separate steps; no recurring initial ingest or invented ESS identifiers.

The task's resource contract is incomplete; preserve the documented proposal
and resolve the gap shown by the planner before execution. No provider shortcut.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.


## Data Loader Contract Not Resolved

The generated REST import mode has an empty businessObject. Do not call sample
download, GET, POST, PATCH or import with that empty value. Obtain a catalog-owner
confirmed task-specific provider and registered business-object contract first.
Do not infer one from the task label, change CSV flags, or substitute direct REST.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Search Indexes` under `Learning Management Common`.

Guidance migrated from the offering setup workflow and PM FDD version 7;
source review dates and limits are retained in [taxonomy and sources](references/taxonomy-and-sources.md).
Use [Common workflow](references/workflow.md) for intake, proposal, approval and
reconciliation. This is task-specific guidance within the Common skill, not a
new nested skill or a new executor.

## Oracle documentation and applicability

Use Oracle's [Overview of Search Indexes (26C)](https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-search-indexes.html),
[Add Extensible Attributes to Search Indexes (26C)](https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/add-extensible-attributes-to-search-indexes.html)
and [Remove Extensible Attributes from Search Indexes (26C)](https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/remove-extensible-attributes-from-search-indexes.html),
reviewed 2026-09-22. The task adds or removes extensible attributes for products
using the search extension framework; only non-predefined attributes are
selectable. This is not a general index creation/deletion or database-index
administration contract. Confirm applicability to the target Learning feature
and release; these pages do not establish a mandatory list of Learning indexes.

## Baseline and proposed attribute changes

For the selected Learning requirement, capture the exact index and attribute
identities, business labels/purpose, predefined status, current selection and
evidence of publication. Distinguish published configuration from pending edits
and unknown evidence; a selected attribute alone does not prove readiness.
Show the proposed add/remove/keep decision and its affected search/filter
consumers. Ask for the specific missing index, segment or business decision;
continue independent planning rather than guessing an attribute or treating an
unread baseline as absent.

Preserve unrelated attributes. For removal, explain the affected Learning
filters/views and obtain approval for that exact delta. If existing unpublished
edits could be included in publication, reconcile their ownership and scope
before proposing Publish; do not silently publish someone else's changes.

## Configuration and publication

The linked Oracle procedures are implementer guidance, not authorization for
browser automation or a replacement for the unresolved provider contract:

1. In Setup and Maintenance, use Tasks panel > Search > Manage Search Indexes,
   locate the exact index and use Configure.
2. On Edit Index Attributes, select attributes for approved additions or
   deselect them for approved removals, then use Save and Close. Only
   non-predefined attributes can be selected or deselected; preserve all
   selections outside the approved delta.
3. Publish the index changes. Oracle enables Publish only after attributes have
   been added or removed; Save and Close alone does not persist the changes
   permanently to index metadata.

Verify the resulting published attribute selection against the approved delta.
An already-published matching selection is a configuration no-op; do not toggle
attributes merely to enable Publish. If publication is unverified or fails,
report that stage as pending or failed, not complete. Published metadata,
successful ingestion and Learning page acceptance require separate evidence.

## Learning index readiness

Identify the intended Learning search/filter requirement, the index and exact
segment, current evidence and personas. Release/build is optional context and
must not become an intake or execution prerequisite. A deployed DFF alone
does not prove index enablement, completed ingestion or page configuration.
Require successful configuration and deployment from
[Manage Descriptive Flexfields](manage-descriptive-flexfields.md#configuration-deployment-and-acceptance)
when the requested filter uses a DFF.

For catalog DFF search, the [25B feature guidance](https://docs.oracle.com/en/cloud/saas/readiness/hcm/25b/lear-25b/25B-learning-wn-f38613.htm)
requires the combined catalog browse/search experience with hover cards and
catalog Search Views support. Verify current capability and actual enablement;
hand missing profile/page prerequisites to their owning workflows, not an
implicit profile change here. Older readiness notices describe feature rollout,
not proof that a current environment needs the same upgrade action.

1. For catalog attributes, configure `fa-hcm-learningitem` and expand
   `liFlexFields`. Choose `Value [Value]` for LOV segments and the segment's name
   for text, date/time or table-validated segments. The index is predefined;
   the add/remove restriction applies to its attributes, not to configuring the
   index itself. For assignment/record requirements, assess the corresponding
   `fa-hcm-learningrecord` segments separately using
   [current Learning setup](https://docs.oracle.com/en/cloud/saas/talent-management/famlc/set-up-oracle-learning.html);
   do not assume the catalog node path applies to every index. Save and publish
   the approved delta as described above.
2. The documented process is **ESS job to create index definition and perform
   initial ingest to OSCS**, accessed through Tools > Scheduled Processes.
   For this catalog change, use `fa-hcm-learningitem` as **Index Name to Reingest**.
   Initial setup is a one-time initialization; Learning index changes require
   deliberate reingestion so the changed segments become available. This is not
   a recurring maintenance schedule. Follow
   [current ingestion guidance](https://docs.oracle.com/en/cloud/saas/human-resources/faeos/run-initial-data-ingestion.html):
   select only applicable supported indexes and submit them serially with an
   explicit index parameter. A blank parameter can ingest all supported
   predefined indexes. Do not use it or treat `fa-hcm-learningitem` as sufficient
   for every Learning feature. Use the declared search/ESS workflow; the display
   name and UI parameter label do not supply an executable package/API contract.
3. After successful ingestion, hand the indexed segments to the appropriate
   HCM Tool Search Views workflow. For catalog DFFs, distinguish LOV filter
   facets, text keyword fields and administrator result columns; indexing alone
   does not enable their view configuration. Validate the requested fields,
   filters, synthetic results, translations and learner/manager/administrator
   access. Learning Items and Learning Assignments views are distinct, as are
   filtered-list attributes. A completed ingestion job is not business acceptance.

Global search configuration and suggestion groups have their own task
identities; do not substitute them for index or Search Views work. No Learning
search executor is declared by this guidance. Resolve the exact search and ESS
contracts, approvals and bounded status workflow before any remote action.
When unavailable, preserve the proposal and give the owner a precise next
action; do not submit an invented job or claim full DFF/search readiness.

## Oracle Text maintenance is a separate operation

[Optimize Learning Text Indexes](https://docs.oracle.com/en/cloud/saas/talent-management/faiml/optimize-learning-text-indexes.html)
maintains Oracle Text indexes, not the OSCS ingestion described above. Do not
substitute it for publishing DFF attributes, reingesting the Oracle Search
index or configuring Search Views.

Oracle documents a monthly run on the 25th at 02:30 UTC and warns against
running it more than once per month. Check existing scheduling and recent runs
before proposing any action; do not add a duplicate schedule. Normal optimization
keeps search available. **Recreate Index = Yes** drops and rebuilds the text
indexes, makes search unavailable during the operation and is only for use when
Oracle Support requests it; never propose it as routine optimization or a generic
search repair. Any authorized maintenance uses the
[background-process handoff](references/setup-capability-handoffs.md#non-fsm-foundation-handoffs)
with its own exact contract, impact review and approval.
