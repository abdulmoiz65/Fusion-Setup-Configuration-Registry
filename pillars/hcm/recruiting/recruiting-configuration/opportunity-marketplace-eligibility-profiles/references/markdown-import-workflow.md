# Preview, approval and import

Load `core/data-loader/SKILL.md` first. Its current orchestration and approval
requirements are authoritative; do not bypass a missing required gate using
this reference. Reuse its existing Task Hook and the unchanged parent importer,
not the Benefits-only wrapper. Read the parent import/recovery contract.

1. Complete workbook/XML/source validation, design review and current target
   reference resolution. Validate active Run Book and the existing OM task
   context. Verify PRTP/APS/ORA_OPP_MARKET_PLACE in every packaged profile.
2. Through the shared REST client read every page of eligibilityProfilesLOV
   without usage/type filters. Compare trimmed, case-insensitive names across
   the workbook and returned inventory. On collision report exactly:
   "The eligibility profile name you entered is already in use. The name must
   be unique within the enterprise". Lookup failure blocks creation. Visible
   inventory does not replace Fusion's final enterprise-wide validation.
3. Invoke the unchanged parent `scripts/eligibility.py import` with `--zip`,
   `--openapi` pointing to its logical `references/plan-copy.openapi.json`,
   `--task-name "Opportunity Marketplace Eligibility Profiles"`,
   `--operation-label "Opportunity Marketplace Eligibility Plan Copy import"`,
   `--import-prefix OM_ELIG_`, explicit `--effective-date`, matching OAuth
   `--properties`, `--token-cache`, child `--task-context`, `--sequence` and
   a new `--preview-output`. This sends no external request.
4. Inspect the resulting preview: taskCode ORA_IRC_MP_ELIGIBILITY_PROFILE,
   correct task name, active Run Book binding, exact target, package/contract
   hashes, date, profile and supporting-object inventory. Do not accept a
   preview for another task. Provide evaluated rule results if required;
   never mark a rule passed without evidence merely because preview defaults do.
5. Show the full preview and parent design findings, then wait for a later
   standalone `approve`. Source upload or earlier import approval does not apply.
6. Immediately before the first write, repeat the all-usage name check and
   verify unchanged ZIP/preview hashes, target and packaged OM invariants.
   Submit through the same parent import command with `--approve-upload` and
   `--approval-preview`; reuse the exact archive/date and its interactive
   approval prompt. Do not regenerate the archive or use workflow mode.
7. The importer owns metadata creation, enclosure upload, generateMappings,
   ESS polling, mapping verification and final application/consolidated-log
   checks. Never call submitImport or retry a write. Report success only after
   all final checks succeed. Persist the sanitized result and recovery evidence.

The parent importer does not automatically enforce the child-only checks in
steps 1, 2 and 6. They are mandatory agent workflow steps. Monitoring an existing
run uses the parent resume flags and retained identifiers after matching the
archive, target and remote import name; never resubmit on an observation timeout.
This Markdown route has local package/preview evidence, not a new live import
validation. Obtain a fresh approved unique-name test import before claiming
end-to-end validation. Automated post-import evaluation is not yet migrated;
do not run the parent's default Benefits-scoped evaluator for OM profiles.
