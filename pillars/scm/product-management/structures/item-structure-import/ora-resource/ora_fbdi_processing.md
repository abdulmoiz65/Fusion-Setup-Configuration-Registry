# Item Structure Import FBDI Processing

## Purpose

Define the template-driven mapping, packaging, and validation contract for
Item Structure Import. This skill prepares one immutable archive and hands it
unchanged to `core.data-loader`; it never executes a Fusion transport or
import.

## Current Public Template Authority

For every run, fetch the latest release-compatible public Oracle
`ItemStructureImportTemplate.xlsm` from the Item Structure entry in the Oracle
Fusion Cloud SCM File-Based Data Import guide. Record the public page and
workbook URLs, applicable Oracle release, retrieval time, SHA-256 digest, and
sheet sequence. The workbook and its linked control files are the sole schema
authority for that run.

Read each populated sheet's ordered export columns, technical names, types,
required markers, validations, and allowed values. Preserve its complete column
order, trailing empty fields, encoding, delimiter, quoting, and null
conventions. Stop on template drift: a changed sheet sequence, output filename,
or export contract requires updating this task skill before creating a package.

## Package Contract

Create headerless root-level CSV members only for populated template sheets.
Use the current template's prescribed filenames and preserve this relative
order when the associated sheets are populated:

1. `EgpStructuresInterface.csv`
2. `EgpComponentsInterface.csv`
3. `EgpSubCompsInterface.csv`
4. `EgpRefDesgsInterface.csv`

Use one numeric Batch ID consistently in every populated member at the
template-prescribed position.

Before packaging, reject overlapping effective-date ranges for repeated
component and structure combinations. Require reference-designator effectivity
dates to match the related component effectivity dates. When importing
substitute components or reference designators, include the related parent
component in the same package.

## Validation and Immutable Handoff

Reopen the completed ZIP and fail closed unless it has safe root-level members,
no duplicates or unexpected files, exact template-prescribed names and order,
headerless CSV rows with exact field counts, current-template valid values,
coherent parent/component, substitute-component, and reference-designator
relationships, one Batch ID, and a SHA-256-bound preview.

Hand that exact archive, without copying or changing it, to `core.data-loader`
with task context and registered FBDI Data Loader business object `item`.
Supply template provenance, ZIP digest, member manifest, row counts, mapping
preview, and Batch ID as read-only evidence.

Do not upload the ZIP, call an ESS job, initiate or monitor an import, query a
Fusion execution endpoint, construct execution parameters, or perform UCM
basename checks. `core.data-loader` owns all later authorization, transport,
submission, and monitoring decisions.
