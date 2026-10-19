# Planning CSV preparation

## One preparation, one handoff

Use the four-file route table in SKILL.md as the capability boundary. Do not
invoke an independent scope gate. Select the intended members during intake,
extract their current contracts once, then generate/select/validate the package
in one preparation command. Core receives the resulting evidence unchanged.

Preparation is a local file operation, not a Fusion import or an approval.
Complete SKILL.md's Source system and collection mode intake first, including
for supplied CSVs/ZIPs: require an explicit Source System for this request and
give the Net Change FYI without asking for collection-mode approval.
Use a user-approved folder or a controlled transient location outside the
repository/project. There is no fixed output folder; honor a suitable user
destination, or choose a new controlled folder for the run when none is given.
No customer rows, workbook copies, CSVs, ZIPs, or raw request JSON belong in
project artifacts. Persist only redacted hashes, counts, results and provenance.

### Output location and access

Resolve the output folder before preparation. It must already exist, permit
preparation writes, and allow the intended Core Data Loader execution identity
to read the final ZIP. On Windows, a controlled run folder can inherit access
from an approved parent (for example, using PowerShell `New-Item -ItemType
Directory`); do not put a cross-account handoff inside a creator-only Python
`TemporaryDirectory`. Never broaden folder permissions automatically or grant
Everyone access. If the selected folder is unsuitable, stop and request a
suitable destination or authorized access correction.

The helper stages a uniquely named file directly in the destination, validates
it, and publishes it atomically without replacing existing files. On Windows,
the staged and final files inherit the destination's permissions instead of a
private staging directory's permissions. No particular Windows account name
or same-account execution is required when the approved folder grants the
intended identities access. Keep POSIX temporary-file permissions restrictive.

Return the final ZIP path in the preview and preserve it through Core handoff.
Use Core's existing preflight read to detect an unreadable ZIP before approval;
do not add a duplicate validation cycle or change permissions/copy the artifact
after approval. Supplied supported-only ZIPs retain their original path and
bytes. The manifest's project paths store metadata/evidence only, not raw files.

## Download and contract extraction

1. Use the exact workbook from SKILL.md. Follow
   ora_reference_lookups.md for current public links and source-system eligibility.
   Fetch only needed workbooks and CTLs, once per distinct file in this run.
   Do not search every Planning entity or reuse files from a previous run.
2. Retain published basenames. Record a local preparation run identifier
   (not Fusion's Run Book runID), documentation release, selected source system
   and type, source catalog URL, actual retrieval timestamp, and each file's
   actual download URL and SHA-256. Use this provenance JSON structure:

   ~~~json
   {
     "run_id": "unique-local-preparation-id",
     "release": "26c",
     "source_system": "user-selected-source",
     "source_system_type": "External",
     "catalog_url": "https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faspf/import-templates-used-to-create-csv-files-for-oracle-supply-chain-planning.html",
     "retrieved_at": "actual-UTC-download-timestamp",
     "files": {
       "ScpSourcingImportTemplate.xlsm": {"url": "actual-public-download-URL", "sha256": "actual-file-digest"},
       "SourcingRules.ctl": {"url": "actual-public-download-URL", "sha256": "actual-file-digest"},
       "AssignmentSets.ctl": {"url": "actual-public-download-URL", "sha256": "actual-file-digest"}
     }
   }
   ~~~

   These are structural placeholders, not Oracle values or safe defaults.
3. Extract a compact contract into a new transient JSON file:

   ~~~text
   python scripts/inspect_planning_fbdi_template.py <ScpSourcingImportTemplate.xlsm> --control-file <SourcingRules.ctl> --control-file <AssignmentSets.ctl> --provenance <downloads.json> --output <contracts.json>
   ~~~

   For ATP, substitute the ATP workbook and requested ATP CTLs. If both families
   are requested, pass both workbooks as positional arguments and all requested
   --control-file arguments in the same command. Each workbook is read once.
4. Read only the selected contract's field_mapping to map the user's business
   values. The extractor selects the data tab by CTL filename prefix, including
   Oracle's trailing underscore convention. It reads metadata only, not sample
   rows, Instructions, or VBA. CTL headers are paired positionally with the full
   worksheet metadata. Internal blank cells retain their positions; only
   trailing worksheet styling beyond the schema is ignored.
5. The contract includes labels, descriptions, data types, physical headers,
   provenance, and position mapping. Interpret documented enum/conditional
   requirements and cross-file business relationships once while mapping the
   request. Sample values are not defaults. Resolve ambiguous values before
   packaging. The helper checks shape/types/lengths/dates; it does not claim
   Fusion referential validation or replace this business mapping review.

All generated CSVs include the CTL's complete input columns, its header
behavior, and an extra END header/value after those input columns. CTL
constants/expressions (including REFRESH_NUMBER and LOAD_REQUEST_ID) are
server-generated and must never be requested from the user.

## Prompt generation

Create a mapped request JSON outside the repository. Keys are exact CTL
input-field names from the contract; values are strings, numbers, or null:

~~~json
{
  "operation": "create",
  "members": {
    "SourcingRules.csv": [
      {"SR_INSTANCE_CODE": "user-source", "SOURCING_RULE_NAME": "Example-Rule"}
    ]
  }
}
~~~

This shows JSON shape only, not a complete business row. Include required and
conditional values from the current contract before preparing. Map the explicit
Source System value for this request to SR_INSTANCE_CODE in every generated row.
Unspecified optional values become blank fields; no implicit business defaults
are added to CSV fields.
The helper always emits all positions, including trailing blank positions
before END. It does not translate English business values or enum labels.

For an update, use operation "update" and represent each row as
{"baseline": {all CTL fields}, "changes": {only requested changes}}.
The full baseline must come from an authorized, trustworthy artifact and
identify the intended row. Explicit null writes a blank CSV field; omitted
changes preserve the baseline value. Do not assume a blank clears a Fusion
value unless the import's documented update semantics say so. If the baseline
is unavailable, ask for it or resolve documented
update semantics; never invent the current state. Do not use this helper to
delete rows or silently turn an update into a create.

~~~text
python scripts/prepare_planning_fbdi.py --request <mapped-request.json> --contracts <contracts.json> --run-id <same-local-run-id> --output-zip <new.zip> --report <preparation.json>
~~~

This replaces per-request generation scripts. It writes the CSV members
directly into the ZIP; no filled XLSM, macro run, workbook rendering, or extra
CSV copy is needed. To show CSV content, read the generated ZIP member.

## Supplied CSV or ZIP

~~~text
python scripts/prepare_planning_fbdi.py --source <source.csv-or.zip> --contracts <contracts.json> --run-id <same-local-run-id> --output-zip <new.zip> --report <preparation.json>
~~~

Inventory the names before template downloads, so only retained members'
contracts are fetched. The command validates original bytes; it does not
regenerate supplied CSV data or add END to supplied files. A supplied file may
have the full CTL width with or without a consistent terminal END. Recognized
XLSM labels/technical names are accepted at their paired CTL positions without
requiring identical column names. Reordered or unknown headers block.

File contents do not replace the explicit Source System intake. During the
existing mapping/content review, compare retained rows' source-system values
with the user's value. A mismatch blocks handoff; request corrected input, not
a silent CSV rewrite or a different inferred source system.

- A supported-only ZIP is returned at its original path, byte-for-byte.
- A mixed ZIP becomes a new supported-only ZIP, preserving retained CSV bytes
  and relative order. Exclusions are returned for disclosure before approval.
- A single supported CSV becomes one root-level member in a new ZIP.
- No supported members, duplicate/empty/nested supported members, unsafe paths,
  links, encrypted data, invalid CSVs, or missing contracts block the entire
  preparation. No unsupported prompt entity is partially generated.
- Existing output files are never overwritten. MacOS resource metadata is
  ignored, not treated as a business entity.

Add --dry-run for validation with no artifact/report writes. It returns
dry_run_passed, not a load-ready archive. No second dry-run or standalone scope
command is required in a normal successful preparation.

## Evidence and Core boundary

The helper verifies the same-run identifier and source hashes without reparsing
the XLSM. It validates each CSV once, builds/selects the ZIP, and reopens newly
created ZIPs to verify exact member bytes/order. The report binds the ZIP hash,
member hashes/counts, mapping positions, exclusions, and template provenance.
Its READY_FOR_CORE_DATA_LOADER status means local preparation only.

For a load request, reuse this evidence through Core preflight and Task Hook.
Carry the explicit Source System and defaulted Net Change mode into the handoff.
Resolve missing task/Run Book or environment context before live work; do not
ask for a collection-mode choice. Do not create/merge a Run Book without
authorization.
Do not perform a separate pillar authentication, BO lookup, or approval.

Do not refetch public templates or repeat preparation after execution approval.
Core's approved-artifact checks remain authoritative. Regenerate and obtain
fresh approval only if the artifact, request, contract, or execution context
changes. Persist the required redacted project evidence together at the
preparation checkpoint; do not repeatedly rewrite audit files between checks.
