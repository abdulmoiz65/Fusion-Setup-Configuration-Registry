# Setup Guidance and Blank Template Contract

## Purpose

Provide useful setup guidance before the user has complete implementation
requirements. This stage is local, review-only, and independent of Fusion.

## Entry Conditions

Enter this stage when the user asks for a blank template, questionnaire,
checklist, example, or setup guidance. Readable supplied configuration, even
when incomplete, goes to [preliminary proposal review](review-only-proposal-contract.md)
with its values, rows and uncertainties preserved. A blank template may be
offered as a requested supplement, never as a replacement for those supplied rows.

Do not require an exact setup task, target environment, Fusion release,
authenticated session, lookup result, complete required fields, provider route,
or execution approval. Do not ask a technical questionnaire before returning
the reusable blank template.

## Output

Return the governed blank multi-sheet XLSX intake template and a short
configuration checklist covering:

- the supplied objects and identifiers;
- their parent/child links and relationships;
- required values and explicitly supplied optional values;
- supported dates and translations only when applicable;
- the source references and mappings to confirm.

Offer direct entry, this blank requirements template, or an existing readable
file. Do not require business purpose, workforce scope or downstream consumers.

All configuration sheets contain headers only. Instructions and field labels do
not constitute populated configuration, defaults, lookup evidence, exact-match
evidence, provider readiness, or execution approval.

## Separation From Later Stages

The stages below are distinct and never inherit approval from an earlier stage:

1. Blank setup-intake template and guidance.
2. Populated requirements intake.
3. Complete supplied-configuration review proposal and mapping confirmation.
4. Technical normalization and implementation validation.
5. Immutable package or Data Loader preview.
6. Separately approved live execution and readback.

Template generation must not load Fusion configuration, call a network client,
read a token cache, run a lookup, create an import artifact, or enter a task
execution graph.

## Determinism

The blank workbook uses fixed member order, fixed ZIP timestamps, stable sheet
order, stable headers, and no environment-derived values. Two generations from
the same source version must have the same SHA-256 fingerprint.

## Local Generator Command

Run from the repository root with Python 3.11. Replace `<project_id>` with the
selected durable project ID and choose a new artifact version/destination before
running; the generator does not overwrite an existing workbook.

```bash
python3.11 pillars/hcm/hcm-tool/profile-management-content-library-configuration/scripts/generate_profile_content_library_template.py \
  "project/<project_id>/artifacts/pillars/hcm/hcm-tool/profile-management-content-library-configuration/setup-guidance/v1/content-library-requirements.xlsx"
```

The positional argument is the new `.xlsx` output path, not a source file. Return
the generated workbook and its JSON summary, then register the output and token
usage through the project's Core artifact/state workflow. Never use a supplied
requirements workbook as this destination. Generation is local and requires no
Fusion configuration, login, lookup or execution approval.
