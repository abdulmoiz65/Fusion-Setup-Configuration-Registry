# Validation and `.vx` readiness

## Validation layers

### Repository safety

- Work is on a non-protected feature branch.
- Starting commit and intended base are known.
- Existing unrelated changes remain untouched.
- Changed files match the approved scope.

### Source integrity

- JSON parses.
- JavaScript parses.
- No conflict markers or whitespace errors remain.
- Advanced Expression imports resolve.
- Rule identifiers are unique.
- Extension-owned files are used.
- No local machine paths or likely secrets were introduced.
- Each changed artifact is classified as Business Rules, Advanced Expression,
  Page Properties, read-and-preserve Express metadata, or out of scope.

### Business behavior

- Conditions, actions, messages, and ordering match the requirement.
- Field paths and lookup values are backed by page/release evidence.
- Business Rules counterparts may come from the repository or from a focused
  deployed evidence manifest supplied with `--evidence-manifest <path>`. Cache
  evidence is read-only Oracle-delivered proof and does not imply customer
  overlay ownership.
- Positive, negative, null, boundary, and setup-missing scenarios are covered.
- Overlap with existing rules has been assessed.

### Page Properties behavior

- The FA property definition and Extension overlay are identified.
- Property names, types, allowed values, and merge behavior are supported by
  target-page or release evidence.
- Unknown keys and unrelated property values are preserved.
- Structural checks are not reported as runtime verification.
- Unknown property contracts block speculative writes.

### Page Property rules and rule-set layouts

- `page-r-x.json` has a readable `page-r.json` counterpart and recognized root shape.
- Every configured Page Property is defined by the Oracle rule contract.
- `layout-x.json` has a readable `layout.json` counterpart and recognized root shape.
- Rule-set rule references, variants, `usedIn`, fields, groups, and sections are consistent.
- Added fields belong to the component data resource.
- Added container sections use an Oracle-provided template.
- Structural checks do not prove runtime condition inputs or service behavior.

### Project tooling

Prefer repository-provided, version-matched build and audit tooling. If
dependencies are absent, stop and report the prerequisite. Never install them.
Report skipped audit or build work as “not run.” Explicitly approved release-alignment package changes
can be validated with `--allow-release-tooling-update`; without that flag,
files outside Extension source remain outside scope.

## `.vx` topology gate

Before building:

1. Classify the repository using [repository-topologies.md](repository-topologies.md).
2. Verify the Visual Builder build dependency is declared and installed.
3. Discover the repository’s supported build command or build API.
4. Determine whether the request is package-only or includes deployment.
5. Keep package output under the repository’s ignored build directory.
6. For a fresh build, record the source `HEAD` and whether the worktree was
   clean. Use `--expected-head` and `--require-clean` for a reviewed release.

An AppUI helper that requires `vb-extension.json` and one `app.json` is not
automatically compatible with a multi-product repository that uses
`extension.json`.

## Archive validation

After a repository-supported build creates a `.vx`, inspect it without
uploading. Validate:

- Required root metadata exists.
- Manifest and build information parse.
- Manifest file references exist in the archive.
- Build resource references exist in the archive.
- Extension identifier and name are internally consistent.
- Version format is accepted by the target build contract.
- Test-only artifacts are absent when required.
- The archive was produced from the reviewed source state.

Do not assume that a zip of processed files is a valid `.vx`.
An explicitly selected existing archive can be structurally validated without
proving which source commit produced it. Report that source binding as
unavailable rather than inferred.

## Preview and deployment

A multi-product extension may affect multiple applications, flows, and pages.
Use the approved proposal's deployment target first. This may be an authentic
Extension page artifact or a complete supplied Redwood URL when the change
is dynamic-layout-only. Then check supplied URLs, exact app-info/repository
evidence, and the active/open page file. Ask the user only when every source is
missing or ambiguous. A standard page-preparation pair may be created when
deployed source proves its exact owner/application/flow/page and preparation is
part of the customization; otherwise do not infer the target from Git history
or manufacture a page overlay. Package creation remains independent of page mapping, and a
deploy without an explicitly selected archive creates a fresh snapshot version.

Treat these as distinct approvals:

1. Install dependencies
2. Deploy, including its fresh snapshot build when no archive is supplied
3. Push source to Git
4. Open and test a preview

Success at one stage does not authorize the next.

## Packaged capability

This skill includes:

- Deterministic repository and source validation
- Optional deployed evidence-manifest proof for read-only Oracle counterparts
- Optional release-tooling validation for explicitly approved version alignment
- A topology-aware local wrapper around the repository's pinned Oracle
  `vb-process-local` and `vb-package` tasks
- Validation of the resulting `.vx`
- A one-request HTTPS uploader for the Fusion extension collection

Read [local-vx-build-and-deploy.md](local-vx-build-and-deploy.md) before
building or deploying.

The uploader does not retry, poll deployment status, or request resolved page
URLs. The upload response and derived URLs remain separate
evidence.
