# Change Order Import FBDI Processing

## Purpose

Define the template-driven mapping, packaging, and validation contract for
Change Order Import. This skill prepares one immutable archive and hands it
unchanged to `core.data-loader`; it never executes a Fusion transport or import.

## Current Public Template Authority

For every run, fetch `ChangeOrderImportTemplate.xlsm` from the current public
Oracle Change Order Import page. Record the page URL, workbook URL, retrieval
time, SHA-256 digest, and sheet sequence. The workbook and its linked control
files are the sole schema authority for that run.

Select one current workbook/control-file set and retain those exact bytes for
the mapping, package, validation, and handoff cycle. Do not treat an older
release workbook, a retired local exporter, or Git history as a candidate run
input.

Read each populated sheet's ordered export columns, technical names, types,
required markers, validations, and allowed values. Preserve its complete column
order, trailing empty fields, encoding, delimiter, quoting, and null
conventions.

Stop on template drift: a changed sheet sequence, output filename, or export
contract invalidates the current cycle. Do not build a comparison archive or
fall back to an older template; start a fresh cycle only with the selected
current workbook/control-file set after the drift is resolved.

## Package Contract

For source-data input, create headerless root-level CSV members only for
populated sheets. Use the current template's prescribed filenames and member
order. Use one numeric Batch ID consistently in every populated member where
the template requires it. For a supplied prebuilt FBDI ZIP, do not rebuild it;
validate the supplied archive against this same contract.

## Validation and Immutable Handoff

Reopen the completed ZIP and fail closed unless it has safe root-level members,
no duplicates or unexpected files, exact template-prescribed names and order,
headerless CSV rows with exact field counts, valid values, coherent cross-file
references, one Batch ID, and a SHA-256-bound preview.

Hand that exact archive, without copying or changing it, to `core.data-loader`
with task context and task business object `Change Order`.
Supply template provenance, ZIP digest, member manifest, row counts, mapping
preview, and Batch ID as read-only evidence.

For unchanged source data or a supplied prebuilt ZIP, template/control files,
and archive digest, perform one Data Loader preflight and retain its immutable
envelope for later approval. Do not regenerate or replace the archive, or
repeat local, preflight, or Task Hook validation after that point.

Do not upload the ZIP, call an ESS job, initiate or monitor an import, query a
Fusion execution endpoint, construct execution parameters, or perform UCM
basename checks. `core.data-loader` owns all later authorization, transport,
submission, and monitoring decisions.
