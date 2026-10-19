# Organization-setting transport profile

Profile `org-settings-11.13.27.01-v1` supports explicit reviewed
EXM_ORG_SETTING insert/update values on the exact task schema and release
11.13.27.01.0. Use `scripts/fsm_transport.py` with core's captured template and
normalized intent after fresh same-target baseline comparison. It checks task,
release, members, exact field membership, attribute types, XML paths, sequence and
batch. It preserves the fresh target CSV header order when serializing by field
name. A mismatch requires a maintained profile refresh, not a customer-created
import ZIP. This profile is source-backed and has one independently checked successful FSM
import. It is not certification of every environment or release.

## Evidence and its limits

The authoring user attested on 2026-10-13 that the supplied same-task ZIP was
successfully imported. SHA-256:
`476ae1aa6cc13401045096190f503e569b44388e45d354b843d15733367ad01c`.
Inspection found 352 organization-setting rows, including 76 blank BuName
global rows, and two identical 306-row option aliases. Its metadata records
release 11.13.27.01.0 and the originating **export**. Export metadata is expected
inside an import package and does not contradict the user's import testimony.
No import ProcessId, server result or before/after comparison was supplied.
All five audit fields are populated in every supplied row. Therefore the ZIP
is evidence for the user-attested global representation, not a live test of
empty audit fields, new target rows or a minimal delta. Keep these distinctions.

The blank audit and insert contracts come from the owning sources:

- [FSM owner FAQ, version 37](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=1681235222),
  section “Behavior of Updateable property during readXML()”, lines 323–347:
  non-updateable attributes are ignored by readXML.
- OrgSettingVO marks CreationDate, CreatedBy, LastUpdateDate, LastUpdatedBy and
  LastUpdateLogin non-updateable. OrgSettingEO declares history columns for
  them; audit values belong to the server. Source links are SRC-ORG-VO/EO in
  `../ora-resource/ora_input_validation.md`.
- CSVXmlTransform.populateXmlRequest, lines 779–809, parses date text only when
  nonempty. Empty audit cells can pass conversion without fabricated dates.
  `markVOsToUseXMLExplicitNull`, lines 611–623, enables explicit null output.
  Source: SRC-FSM-CSV-TRANSFORM in `../ora-resource/ora_error_handling.md`.
- ExpenseOrgSettingServiceAMImpl.importData resolves BuName to target OrgId,
  uses -1 for global scope, and invokes updatePrimaryKeysInXML followed by
  readXML. OrgSettingEO primary and alternate keys are OrgId + SettingCode.
  An absent expense-setting row is an insert into that verified scope, not a
  business-unit creation. [Oracle's ADF readXML documentation](https://docs.oracle.com/en/middleware/developer-tools/adf/12.2.1.4/develop/working-programmatically-view-objects.html)
  describes updating matching keys and inserting absent rows.

The initial qualification combined these owning contracts with the
user-attested successful blank-global representation; the subsequent live
organization-setting import below provides additional execution evidence. It does not require a
separate empirical example of every empty non-updateable audit column. It also
does not erase the source/deployed-version boundary: execute through the normal
preview and loader, report actual failures, and verify results through the
declared status/reconciliation workflow. Never report source reasoning or unit
tests as a successful Fusion import.

## Verified organization-setting import

On 2026-10-13, the governed loader submitted this profile's four-row delta.
The status workflow checked both dataLoaderDataSets and dataSetErrors, then
retrieved the FSM ProcessLog. The server reported four OrgSetting rows
processed with zero failures and zero warnings, and skipped Expense Setup
Option because its CSV members were empty. Overall import completed
successfully on release 11.13.27.01.0. This verifies import acceptance of the
minimal organization-only package with empty audit fields, BU/global scope,
and header-only option aliases. Baseline comparison identified two existing
keys and two missing keys before the import. The log does not report a per-key
insert/update breakdown or independently read back the resulting values.

No production/customer rows, private hostnames, credentials, local paths or
request identifiers are included in this reusable evidence summary. The
profile evidence flag describes this historical test; `live_result_verified`
remains false for a newly composed target until that run is actually verified.

## Serialization

Create one row per requested organization-setting key. BuName is the verified
exact BU name or empty only for explicit global scope. All five audit fields
are empty. SettingCode and SettingValue come from normalized user intent.
For these reviewed codes, SettingValueDecoded mirrors SettingValue, matching
the export projection; independent decoded-value input is rejected. Account
and template remapping codes are excluded by the input contract.

All unrequested controls produce no row. Both setup-option CSVs retain their
headers with zero rows. The service-empty check and MigratorHelper's positive
row-count guard establish that empty option members contribute no writes;
their collision cannot select an unwanted value in this profile. Retain exact
target metadata byte-for-byte. The task prepares a local candidate ZIP; core
preflight and Task Hook bind its exact bytes to the preview before approval.
Core alone uploads and initiates. Do not copy source-environment audit identities or unrelated settings.

## Remaining product dependency

This profile does not support a required ENABLE_AUTO_SUB_DA_EXP write when the
two populated option aliases collide. The historical authoring ZIP contains identical
aliases, but does not include resulting values proving the proposed minimal
delta strategy. Preserve FSM_ALIAS_COLLISION for that case. Resolve it in the
repository using an owning FSM selection contract or a verified import/result
for identical minimal alias deltas. Do not ask every customer to bring a ZIP,
guess a winning alias, or drop the enable change. If the fresh target baseline
already satisfies enablement, show that fact and use this organization-only
profile for the remaining requested changes.

The [customer workflow and alias policy](customer-input.md#repository-only-customer-workflow)
is part of this shipped skill. The workflow obtains its own target exports;
customers never need to provide that historical ZIP or select an alias. Equal
current-data values support baseline reconciliation only, not qualification of
an identical-row dual-alias import strategy.
