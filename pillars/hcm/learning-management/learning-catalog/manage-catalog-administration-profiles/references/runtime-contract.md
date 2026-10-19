# CAP runtime contract
Record the exact tested source commit and results in each project validation run.
Historical source baselines are provenance, not current compatibility certification.
No locally patched core is required. Offline compatibility evidence is not
live certification; all current target facts must be established through the
authorized route. The known write contract backlog remains in the nested task's
metadata and below, not disguised as executable lookup definitions.

## Available read route
cap_workflow.execute -> source-current shared build_rule_execution_plan and
compile_task -> shared fusion_auth.read_properties target preflight -> documented
fusion_rest_client.py subprocess -> rest_client_common.run_client/request_bytes ->
fusion_auth.authorized_urlopen -> configured HTTPS/host redirect handler.
No CAP HTTP client, raw urllib request, loader call or fallback exists.

The shared client accepts configured HTTPS authorities and refuses unconfigured
redirect destinations. Same-host redirects are allowed under the accepted shared
policy. CAP no longer requires reject-all redirects. Only declared CAP and loader
metadata GET paths are constructed. Read request input cannot supply arbitrary URL, query, auth/body or
headers. Exact environment and standard restBaseUrl origin must match.
Credentials and raw subprocess output remain transient; errors are sanitized.

The compiled thirty-five-node graph has draft, read, root/child inspection, contract-inspection,
separate evidence-gated create/update-preparation, basic-attribute batch preparation,
and raw-write-refusal branches.
Runtime compares its current shared compilation with the stored graph.
readiness returns ready_for_read_preflight, not proof of authentication/access.
Metadata establishes collection GET and field/query/finder shape before data
reads. Number finder is independently cross-checked by equality query. Exact
matches are case/whitespace sensitive; unverified quote/escape syntax is refused.
List paginates with count/offset/limit/hasMore validation and identity loop checks.
Projection: number, name, description, status, visibility, system-default and
processing status where metadata declares text fields. Optional ID check remains
internal and lossless; no raw self-link persistence.

Bounded shared CLI invocation includes auth/refresh time. Metadata60seconds,
collection120seconds; default20pages/2000rows,100perpage. Exact failures do not
produce uniqueness. List limits/errors return verified pages with partial/failed,
pagination_completed=false and total_count=null. Always report access/date/
language/non-snapshot limits. Shared OAuth flow owns login/one refresh, not CAP.
Current exact lookup may refuse names with unverified query-literal syntax.

Profile inspection additionally projects the three reconciliation fields when
described as datetime, and priority only as string. Returned strings/timezones
are preserved; null is an observation, not an absent field or never-run proof.
The source-backed contributorCriteria.criteriaId string contract may establish
identity without a key:true marker; contradictory metadata blocks collection GET.
No generic key waiver applies. Person-list identity remains unavailable without
advertised keys; unadvertised defaults/certificates are not queried. Counts are
criterion rows only, never effective membership. See the owning lookup contract
and metadata-shaped regression fixture. A partial inspection remains partial.

## Offline preparation and live write refusal
cap_create_validation retains the one-root POST fixture/archive/evidence
validator and digest over archive, inputs/evidence, target, operation, Run Book
and source fingerprint. It is offline only; write_eligible is always false.
The real shared validate_source_attributes + prepare_archive path can validate
prepared DAT and build deterministic ZIP without @oai/artifact-tool. Do not infer
deployment fields or omit mandatory values from synthetic template tests.

All mutations stop in cap_workflow. The separate cap_create_handoff preparation
entrypoint requires current verified evidence, exact configured target and active
project binding, and invokes shared read-only loader preflight and Task Hook.
It retains a digest-bound unapproved preview, never an approval or submission.
The ready read graph is never translated to passed write rules. Known denied grants
or unverified omission effects stop preparation; no status is synthesized as verified.
An attributed assessed privilege state may continue through shared authenticated
preflight without an independent grant certificate; retain the unverified-write-
access warning as specified in create-source-contract.md. Fusion authorizes the
later exact-approved load, never a probe. Failed preflight still blocks preview.

Unchanged shared limitations, reproduced with offline actual-boundary tests:
- core/data-loader/scripts/data_loader_metadata.py OAuthSession uses shared OAuth
  but _request_bytes uses ordinary urllib.request.urlopen. No documented equivalent
  configured-host redirect guarantee was established for loader traffic.
- Task Hook intentionally consumes calling-workflow rule evaluation. A central
  CAP plugin is not mandatory: a pillar wrapper can execute domain validation,
  derive inputs from the exact ZIP, bind its evidence/operation/target and call
  the unchanged public approval/uploader interfaces after all gates pass.
- Generic approval binds task/archive but is not a digest of arbitrary CAP
  finalData inputs/evidence. The retained negative test changes inputs while the
  generic envelope remains accepted. This does not permit changing the approved
  ZIP: the unchanged uploader separately verifies its hash. Pillar input/evidence
  integrity must accompany, not replace, that authoritative approval.

Use the unchanged shared loader transport with the limitation documented above;
there is no unconditional CAP transport blocker and no added redirect guarantee.
Project-specific transport risk acceptance is historical evidence, not reusable
authorization for another target or load. This is not a transport fix or a new approval gate.
Read-client redirect protections remain unchanged. Configured-target checks,
shared approval-bound host/environment/Run Book checks, create evidence, privileges,
exact-artifact validation and approval remain required. Evidence-gated creation
has a separate approved continuation in cap_create_submission; raw cap_workflow
mutation requests still refuse. Basic updates use the separate evidence-gated route in references/update-contract.md; lifecycle and child writes remain unavailable.
CAP must not monkeypatch, copy auth/loader services, fabricate
passed rules or remove negative tests. Existing generic archive/target/Run Book
checks are preserved, not represented as absent. No broader redesign is attempted.

The read-only inspect-write-contract branch uses the existing shared GET client
for CAP root describe plus loader BO describe/exact registration/detail. It
uses the public shared resolve_business_object with aliases disabled and an
explicit bounded shared-GET adapter, never the loader's default HTTP getter.
The shared resolver selects exact discriminators after its standard finder
query and deduplicates the same BusinessObjectId/discriminator, including repeats
across advancing pages. Distinct matching IDs remain ambiguous. Enforce
100rows/page,20pages/2000rawrows/120seconds before deduplication; malformed or
nonadvancing offsets fail. The selected positive-decimal ID and discriminator
must agree with the authoritative detail GET. Normal profile-list duplicate
detection is unchanged. This
reports observed writable/required-input markers and registration fields, without
equating them with actual privileges or omission defaults. A template reference
is not a verified template. Its output cannot feed createEvidence as verified
facts wholesale or satisfy Data Loader Task Hook write rules.

## Separate basic-attribute shared REST route

`cap_batch_update.py` selects CAP-BATCH nodes, checks current metadata and unique
canonical identity, and freezes one sparse name/description/visibility update for
exact approval. Rename adds complete duplicate checks; visibility requires current
enum evidence and non-default eligibility. Status writes are not basic edits.
It calls the unchanged shared REST client with POST and the ADF batch media type,
not UCM/Data Loader. See [batch contract](batch-update-contract.md). Source/UI
evidence supports the protocol. Consult the selected project's execution receipts
and readback for target/run-specific live acceptance; neither source evidence nor
offline correctness establishes it. An expired/tampered preview or previous attempt
blocks submission. Readback and processing completion are distinct.

## Operation-specific backlog
| Operation | Required evidence before enablement |
|---|---|
| Root create | Current writable/required fields, number/status/date/contributor-omission defaults, attributed privilege assessment and successful shared preflight with no known denial, complete duplicate baseline, registered BO/live template, project Run Book, validated exact artifact and approval, shared safety above |
| Basic update | Loader route requires the verified canonical date-plus-number mapping/header under update-contract.md. The separately selected shared REST route supports name/description/visibility under batch-update-contract.md, without loader mapping inference. Both require their own current evidence, exact approval and readback. |
| Activate/deactivate | Unavailable: current transition eligibility, action hints, provider/usage/default restrictions, grants and a separately implemented lifecycle contract are required; basic-update readiness does not enable status writes. |
| Contributors | Reconcile historical excluded hierarchy with newer saved contributorCriteria template; verified person resolver, criterion/parent/attachment keys, number/email/local-file-to-product conversion, add/replace/remove semantics, counts/errors and membership processing |
| Delete | Source logical status/eligible replacement contract, system-default prohibition, usage/provider safeguards and association migration; MERGE_DELETE is not proof of safe deletion |
| Content defaults | Existing seeded per-type rows, type allowlists/root mappings, observer replacement effects, null/omission/reset/inheritance, current registration; no internal defaultedRow bypass |
| Certificates | Existing CAP row/template lookup, privileges, registration/key, enabled/template/null semantics, inheritance and actual rendering; no global-course inference |
| Reconciliation | Actual action arguments/grants/shared route and terminal correlation. No invented RestAction=RECONCILE. Read root processingStatus only as an observation, not dedicated reconcile completion |

Root field evidence: name250, description4000; number displaySize30 is not a
maximum (inherited source precision2000 supplies the local safety bound, with
current advertised maxLength enforced where present). Historical deployed
visibility ORA_EVERYONE/ORA_CONTRIBUTORS. These do not substitute current metadata.
EffectiveDated=Y and Effective-Of handling are separate from the CAP composite
item key. Historical number-only PATCH failed; no fix inferred from a flag.
Composite update mapping separates the ISO canonical key date from its DAT
representation: verified Date helpers use YYYY/MM/DD with verified registered
SQL DATE-to-ISO URL conversion; verified String helpers retain ISO. This source-
aligned local contract does not establish the actual target's PatchUrl mapping.
Source-exposed read-only audit/system/processing attributes are not user inputs.

Registration, template, REST requiredness, create-writability and server defaults
are distinct. APEX metadata envelope is not a business payload. Compare current
authoring/deployment before proposing registration changes; none are made here.
Keep the existing Run Book binding. Prepared DAT does not require a workbook,
but a real XLSX path still needs its supported runtime and tests.

## Future approved execution and recovery
When and only when a supported write route exists, core.data-loader owns immutable
ZIP validation/approval, UCM upload, initiateDataLoad and separately requested
status steps. Proposal agreement is not load approval. Any artifact/input/target/
operation/evidence change invalidates applicable approval.
Submission receipt != terminal load success != contributor processing success.
Require row counts/errors, exact canonical readback of every attempted row and
approved fields, plus effective membership where supported. Preserve partial
outcomes; no automatic uncertain-write retry, cleanup deletion or fake portal URL.
