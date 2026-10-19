# Value Set Value Bulk Intake

## Source Handling

| Source | Contract | Handling |
|---|---|---|
| Text | One or more rows with required flags | Normalize all rows to Values[] |
| Image | Visible spreadsheet/table rows | Transcribe deterministically and retain row provenance |
| CSV | UTF-8, headerless, 13 through 101 columns | Pad supported short rows to the 101-column contract |
| ZIP | Safe archive containing `GlSegmentValuesInterface.csv` | Select values CSV; hierarchy member isn't required or used |

## Safety and Shape Rules

| Gate | Requirement |
|---|---|
| Encoding | UTF-8; accept and remove UTF-8 BOM on intake, write no BOM |
| ZIP paths | Reject absolute paths, drive paths, and `..` traversal |
| ZIP limits | At most 50 files, 10 MiB per member, 50 MiB total uncompressed, and 100:1 maximum compression ratio |
| Encryption | Reject encrypted members |
| Selection | Prefer one case-insensitive basename `GlSegmentValuesInterface.csv`; otherwise require one unambiguous CSV |
| Row width | Require at least 13 columns; preserve through 101; reject populated columns after 101 |
| Value-set scope | Require exactly one Value Set Code per run |
| Output width | Write exactly 101 columns on every row |
| Package members | Include only `GlSegmentValuesInterface.csv` for values-only import |
| Import row set | Include requested rows only; never compare them with existing values or append exported rows |

## Validated ZIP Fast Path

A user-supplied import ZIP is faster when it is already the final values-only
FBDI package. Reuse its exact bytes instead of rebuilding only when all of these
conditions pass:

- The user identifies it as import data and gives explicit live import intent;
  this requests execution but does not replace approval of the exact immutable
  Data Loader preview.
- The safe archive checks pass and the archive contains exactly one root member
  named `GlSegmentValuesInterface.csv` with no hierarchy member.
- The CSV is UTF-8 without a BOM, has no header, and every nonblank row has
  exactly 101 columns.
- Every row targets the exact requested Value Set Code and passes all applicable
  semantic, maximum-length, explicit-usage-context, flag, date, and Account Type
  rules.
- No normalization, default, padding, column clearing, or row change is needed.
- Reopening the ZIP reproduces the parsed CSV bytes and final hashes.

If any condition fails, normalize and rebuild through the standard package
path. A ZIP reduces local transcription and packaging time, but it doesn't
bypass validation, preview, authentication, or `core.data-loader`
authorization. Data Loader owns import selection, upload, submission,
monitoring, and its returned outcome.

## FBDI Field Preservation

Preserve supported translated descriptions, Attribute1 through Attribute50,
and Data Source from CSV/ZIP input. Canonical fields override their matching
positions after validation. Always clear the workbook-only Is Validated marker.
Use the exact intake, column-mapping, and package-generation algorithms in
`ora_fbdi_processing.md`; no local executable helper is part of this skill.

## Preview Requirements

Before live upload, report whether the ZIP was reused or rebuilt, row count, all
values, defaults, column count, ZIP member list, hierarchy-file absence, CSV
SHA-256, and ZIP SHA-256. Reopen the ZIP and compare its contained CSV bytes
with the validated source bytes.
