# Referral Global Segment Archive Contract

Use this contract for the `EXPORT_BASELINE_MISSING` fallback for **Global Referral create, copy, update, or disable**. It is not valid for inspect/list, verification, or `EMPLOYEE_REFERRAL` work.

## Inputs and preconditions

- A historical Referral FSM ZIP whose SHA-256 is `4973ec635a6ecb8092dde7e80ee28e4ae7afb1c4672cb555092055d84eb0a32d`.
- A new, project-local output archive path that does not already exist.
- Confirmed `Name`, `SegmentCode`, `SegmentIdentifier`, `ColumnName`, `SequenceNumber`, `ValueSetCode`, `Prompt`, and `ShortPrompt` values.
- `SegmentCode` is 1–30 uppercase letters, digits, or underscores and starts with a letter; `SegmentIdentifier` is 1–30 ASCII letters or digits and starts with a letter; `ColumnName` belongs to the supported storage family compatible with the confirmed data type (Character, Number, Date, or Date Time); and sequence is positive.

For create/copy when current-definition data is unavailable, the interactive intake must first apply the name-based design rules in `../SKILL.md`, propose a supported type-compatible column candidate (Character: `ATTRIBUTE_CHAR1`; Number: `ATTRIBUTE_NUMBER1`; Date: `ATTRIBUTE_DATE1` only when supported; Date Time: a verified compatible timestamp column) and unverified sequence `10`, then retrieve and list existing compatible target-environment value sets for selection. The requester must explicitly select or revise the column, sequence, and displayed value-set code or name. Do not create a new value set or treat any suggestion as evidence that the column or sequence is free.

Record the resolved source archive path and checksum in the project run and immutable preview. If the checksum-pinned archive cannot be located, or any precondition fails, stop with `ARTIFACT_PREPARATION`; do not substitute an arbitrary package or fabricate its structure.

## Required archive transformation

1. Validate the source ZIP against the pinned SHA-256 before use. Read its complete member set/order, CSV headers/column order, encoding, and metadata directly from that verified archive; require the root, Global-segment, hidden context-selector transport, and ASM metadata members. Do not reconstruct the remaining members from memory or a hardcoded list.
2. Preserve CSV headers, order, encoding, and metadata byte-for-byte. Retain one `IRC_RF_REFERRALS_DFF` / application `821` root row and one hidden context-selector row (`Context Data Element`, `Context Segment`, `ATTRIBUTE_CATEGORY`); clear their audit fields.
3. Empty every other CSV while retaining its header. Replace the Global CSV with exactly one row for `IRC_RF_REFERRALS_DFF`, application `821`, and `Global Data Elements`, using the confirmed values. For create/copy use the confirmed required values and optional defaults/overrides. For update/disable use the complete confirmed target configuration, applying only the requested update or Enabled `N` for disable; never apply create defaults to an existing target.
4. Do not copy historical custom Global rows, audit identities, timestamps, or process provenance.
5. Reopen the new ZIP and verify it is readable, preserves member order and headers, has exactly one root, one hidden context-selector, and one Global row, and keeps metadata unchanged. Calculate SHA-256 before submission approval.

Never overwrite an existing archive or manually repair a failed archive.

## Operation-specific fallback record

Read [Global Fallback for Segment Changes](../SKILL.md#global-fallback-for-segment-changes) before using this contract for copy, update, or disable. The name-based new-row suggestions above apply to create/copy only. Confirm an older matching or requester-supplied complete source/target record as UNVERIFIED; do not fabricate missing identity or preserved properties. For update/disable preserve confirmed target keys, column, sequence, and all unchanged configuration in the single output Global row. For copy use confirmed source type and new identifiers/assignments; for disable change only EnabledFlag to N. Confirm optional values before freezing the archive. Do not replay unrelated historical rows or audit values. Require established existing-row import/key semantics for update/disable; a fallback must not silently create a missing target. The final preview identifies the fallback evidence, unavailable checks, exact operation/delta, and checksum for normal Data Loader approval.
