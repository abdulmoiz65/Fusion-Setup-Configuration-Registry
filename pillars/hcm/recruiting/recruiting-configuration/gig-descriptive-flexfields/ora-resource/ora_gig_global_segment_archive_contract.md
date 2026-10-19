# Gig Global Segment Archive Contract

Use this structural fallback for **Global Gig create, copy, update, or disable**, after a selected-environment exact-task export attempt fails, times out, or returns unusable root/segment rows. It is prohibited for list/inspect, verification, and context-sensitive work. For copy/update/disable follow the confirmed operation-specific fallback below.

## Verified fallback

- Task: `ORA_IRC_MANAGE_OM_GIG_DESCRIPTIVE_FLEXFIELDS`; DFF: `IRC_MP_GIGS_DFF`; application: `821`.
- Captured: 2026-10-04; export process: `300103936510037`; environment host: `cptcpuwqy.fusionapps.ocs.oc-test.com`.
- Archive (repository-relative): `project/gig-dff/exports/recruiting/recruiting-configuration/gig-descriptive-flexfields/https:/cptcpuwqy.fusionapps.ocs.oc-test.com_setup_task_csv_export_ora_irc_manage_om_gig_descriptive_flexfields_300103936510037.zip`.
- SHA-256: `0bd3c7b7bd7d4bc47279a1f9533cb86e52608a9d5f6464e534441595330ff0cc`.
- Captured configuration: one Global segment, `Social Security Number`, API name `socialSecurityNumber`, column `ATTRIBUTE_NUMBER1`, sequence `10`, display `TEXT_BOX`, value set `10/Number`, required `N`; no context-sensitive segments.

This is a structural contract and captured configuration evidence. It is not proof of current state and must not supply a standalone current segment list. Record fallback reason and capture time in the run and immutable preview. Reject checksum, environment, task, DFF, or application mismatch. If the pinned archive is unavailable, stop with `ARTIFACT_PREPARATION`; do not invent its contents.

## Preconditions

- Validate ZIP integrity, the complete exported member set, metadata, exact headers, encoding, and every CSV row's field count. Require exactly one root row for `IRC_MP_GIGS_DFF` / application `821` and matching identity on every child row.
- Apply the name-based design rules in `../SKILL.md`; do not derive every new segment's type, column, display, or value set from the captured Social Security Number row. Confirm the complete new Global design: name, code, API name, column, sequence, value set, prompt, Short Prompt, data type, display type, and optional fields. Disclose unavailable duplicate, column-occupancy, sequence-occupancy, and value-set checks as `UNVERIFIED` and obtain explicit assignment confirmation.
- Validate uniqueness of code, API name, column, and sequence in the exact scope against available target evidence and confirmed assignments. API names contain 1–30 ASCII letters or digits and start with a letter; sequence is positive.
- Select an existing compatible target-environment value set. Context-sensitive work is outside this fallback.
- The output archive path must not exist.

## Transformation and verification

1. Preserve exported members, member order, headers, encoding, root, hidden context-selector transport row, and ASM metadata. Use the verified segment row only as a transport template; replace its data type-related column, value set, and display settings with the confirmed compatible design. Clear audit values for new rows and structural fallback transport rows while retaining exact field counts; never transplant another environment's audit identity or value-set identifier.
2. Retain only the root and hidden context-selector transport rows, with cleared audit values; empty every other CSV while retaining its header. Do not replay historical custom rows.
3. Add exactly one confirmed Global row in `ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_GLOBAL_SEGMENT.csv` with `ContextCode` `Global Data Elements`.
4. Supply the complete exported configuration fields and confirmed design/defaults. Preserve metadata byte-for-byte. Existing target/source properties must come from the explicitly confirmed fallback record, never from an unrelated template row.
5. Reopen the output ZIP; verify integrity, identities, unchanged headers/metadata, every CSV field count, compatibility, uniqueness, and the exact operation delta. Record SHA-256 and show the immutable `core.data-loader` preview for submission approval.

Stop with `ARTIFACT_PREPARATION` if construction or verification fails. Never overwrite or manually repair an archive. Authentication failures and unavailable fresh exports remain recorded diagnostics; fallback package preparation does not bypass live import authentication or submission approval.

## Operation-specific fallback record

Read [Global Fallback for Segment Changes](../SKILL.md#global-fallback-for-segment-changes) before using this contract for copy, update, or disable. The name-based new-row suggestions above apply to create/copy only. Confirm an older matching or requester-supplied complete source/target record as UNVERIFIED; do not fabricate missing identity or preserved properties. For update/disable preserve confirmed target keys, column, sequence, and all unchanged configuration in the single output Global row. For copy use confirmed source type and new identifiers/assignments; for disable change only EnabledFlag to N. Confirm optional values before freezing the archive. Do not replay unrelated historical rows or audit values. Require established existing-row import/key semantics for update/disable; a fallback must not silently create a missing target. The final preview identifies the fallback evidence, unavailable checks, exact operation/delta, and checksum for normal Data Loader approval.
