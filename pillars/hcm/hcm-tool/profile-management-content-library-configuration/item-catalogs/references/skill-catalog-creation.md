# Skill catalog creation

An explicit Skill item uses ContextName SKILL, not COMPETENCY or GOAL. Route
creation of a new custom Skill catalog and its portable items to the
[new-set FSM contract](../../references/new-catalog-set-contract.md). This is
an enabled controlled-certification route, not a verified production provider.

## Scope and evidence

Oracle's [Skill Item Catalogs documentation](https://docs.oracle.com/en/cloud/saas/talent-management/faidy/skill-item-catalogs.html)
confirms Skill catalogs are maintained in Item Catalogs and can be associated
with Skills Center. It documents UI/HDL maintenance, not successful FSM import.
The repository's generic Item Catalog migration graph is the basis for this
FSM certification candidate; live SKILL acceptance has not been established.

The separate new-set registry includes SKILL. The verified existing-parent
provider registry does not. For one explicitly selected child in an existing
custom catalog, use the separate
[existing-catalog certification contract](existing-skill-catalog-certification.md)
and its independent certification-only registry. Do not add SKILL to the verified
registry or change historical HDL certification as a shortcut. The REST registry's read-only status
and its lack of a previously certified positive match remain accurate.

## Execution contract

The following is the new-catalog route only. An existing-catalog request uses
the separate linked canary contract; do not invent a new catalog to work around
the user's chosen existing parent.

Use the existing --preview-new-catalog-set and --prepare-new-catalog-set modes.
Require one intended-new custom catalog, every supplied portable child, exact
Content Type evidence, explicit supplier C, dates and confirmed field mappings.
The authenticated target must be classified non-production under the bound
new-set contract; general-use, existing-catalog packages through this new-set
mode, and the one-child composite test-batch runner remain unsupported for SKILL. Predefined/managed
catalog codes listed in the new-set registry cannot be targets.

Skip pre-import export and reuse a reviewed template under the
[export policy](optional-export-policy.md); disclose unverified duplicates and
other target checks. Known collisions still block. Preserve all request rows;
do not discard unsupported curation, enrichment, relationships or translations
to make a package eligible. Do not manufacture fields not in the portable schema.

Preparation approval is bound to the full catalog-set fingerprint. Submission
uses core.data-loader, its Task Hook, immutable preview and approval policy.
No direct REST write or HDL fallback is introduced. A request to enable this
repository capability is not approval for a live import.

After import, retain process status and ProcessLog, attempt export and report
failures. If export is unavailable, try registered SKILL reads through the
Content Items adapter and skillContentItems relation (registered template 134).
Compare fresh exact target/catalog/item observations; do not fabricate a positive
match from the requested values. Report partial/incomplete REST coverage under
the export policy, and do not promote the provider or replay an import.

Skills Center enablement, content-section subscriptions, search/AI ingestion,
curation and employee visibility are separate outcomes. Creating an item does
not establish those outcomes or certify a complete Skills Center setup.
