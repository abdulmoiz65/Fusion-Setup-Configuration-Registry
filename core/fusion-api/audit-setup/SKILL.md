---
skill_id: "core.fusion-api.audit-setup"
name: "Audit Setup"
description: "Provides Oracle Fusion audit setup guidance, API-based business-object and individual-field control, and explicit manual steps for UI-only audit policy tasks."
layer: "core"
pillar: "Core"
type: "import"
execution_mode: "automated"
owner_team: "Central platform team"
version: "0.1.0"
inputs:
  - "fusion_environment_context"
  - "audit_setup_request"
  - "execution_options"
outputs:
  - "execution_result"
  - "diagnostics"
  - "audit_summary"
depends_on:
  - "core.auth.fusion-oauth-authentication"
uses_core:
  - "core.auth.fusion-oauth-authentication"
persists_project_state: false
workspace_outputs: []
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Oracle Fusion Cloud Applications 26B or newer"
side_effects:
  - "Connects to Fusion Audit Setup REST APIs when invoked."
  - "May change product-level audit levels when set-level is invoked."
  - "May change business-object audit status when update-status is invoked."
  - "May refresh the OAuth token cache when the cached token is unavailable or rejected."
required_privileges:
  - "Fusion privileges appropriate to manage audit setup"
---

# Audit Setup

## Purpose

Provides a reusable Oracle Fusion audit setup utility for enabling, disabling,
checking, and interrogating audit setup before and during implementations.

## Capability Boundaries

The three audit-policy controls have distinct support boundaries. Do not
substitute one for another:

| Requirement | Supported? | Route |
| --- | --- | --- |
| Enable or disable auditing for **Oracle Fusion Applications** overall | **Manual only** | Audit Setup UI; `FA_AUDIT_LEVEL` cannot be updated through REST |
| Enable or disable auditing for a business object | Yes | Audit Setup `update-auditstatus` |
| Enable or disable named fields on a business object | Yes | Audit Setup `update-auditstatus` with `attributesList` |
| Retrieve the list of fields currently audit-enabled on a business object | **Manual only** | Audit Setup UI; do not infer it from REST responses |

`get-auditsetup` returns the available/auditable field inventory; it does not
expose each field's current audit-enabled flag. The known enhancement request
for that API gap is **ER 34232448**. Ask the implementor to open **Manage Audit
Policies** in Fusion and inspect the object attributes when an existing
selection must be verified. A successful `update-auditstatus` response is
evidence only for the submitted update; it is not a general field-status read
endpoint.

## REST API Contract

This skill uses the Oracle Fusion Audit Setup REST API:

- Get product audit levels:
  `POST /fscmRestApi/fndAuditRESTService/audittrail/get-auditlevel`
- Set product audit levels:
  `POST /fscmRestApi/fndAuditRESTService/audittrail/set-auditlevel`
- Get auditable objects for a product:
  `POST /fscmRestApi/fndAuditRESTService/audittrail/get-auditsetup`
- Check object audit status:
  `POST /fscmRestApi/fndAuditRESTService/audittrail/check-auditstatus`
- Update object audit status:
  `POST /fscmRestApi/fndAuditRESTService/audittrail/update-auditstatus`
- Get audit history:
  `POST /fscmRestApi/fndAuditRESTService/audittrail/getaudithistory`

Overall Fusion Applications auditing is **not** one of the Audit Setup REST
API's product-level values (`ODI`, `ESS`, `MDS`, `SOA`, `ADF`, or `OPSS`). It is
the `FA_AUDIT_LEVEL` setting in the Audit Setup UI. Although it is represented
as a site-level profile option, Fusion intentionally rejects REST updates for
this profile with `FND-4681`. Do not call the Profile Options REST API for this
operation.

The documented product/domain codes are:

| Product | Domain |
| --- | --- |
| `ODI` | Oracle Data Integrator |
| `ESS` | Enterprise Scheduler Service |
| `MDS` | Metadata Services |
| `SOA` | SOA infrastructure |
| `ADF` | Application Development Framework |
| `OPSS` | Oracle Platform Security Services |

Product-level audit levels are `High`, `Medium`, `Low`, and `None`.

## Audit History Query Shapes

`getaudithistory` has two supported query shapes; do not apply the
business-object requirement from one to the other.

| Audit scope | Required request fields | Optional narrowing fields | Discovery route |
| --- | --- | --- | --- |
| Oracle Fusion Applications business-object history | `fromDate`, `toDate`, `product`, `businessObjectType` | user, event type, child objects, attributes, impersonator, time zone, pagination | Use `get-auditsetup` with a known functional application to obtain the exact business-object type. |
| Infrastructure-domain history (`ESS`, `MDS`, `OPSS`, or `SOA`) | `fromDate`, `toDate`, `product` | user, event type, attributes, impersonator, time zone, pagination | Query the named domain directly. Do not call `get-auditsetup` with a domain code. |

For the infrastructure-domain shape, omit `businessObjectType`. Fusion can
return domain-specific records such as SOA rule, task, sandbox-name, and
operation changes without a business object. A `get-auditsetup` call is only
for functional application names; `OPSS`, `ESS`, `MDS`, and `SOA` are audit
domains, not application names for that API.

Functional application/product names used by `get-setup` are maintained in:

```text
knowledge/fusion-audit-metadata/fnd-audit-webapp-applications.json
```

## Project Scripts

Run from the repository root.

List known product/domain codes:

```bash
python3 core/fusion-api/audit-setup/scripts/audit_setup.py domains
```

List known functional application/product names for `get-setup`:

```bash
python3 core/fusion-api/audit-setup/scripts/audit_setup.py applications
```

Get current levels:

```bash
python3 core/fusion-api/audit-setup/scripts/audit_setup.py get-level \
  --product MDS \
  --token-cache auto
```

Set a product-level audit level:

```bash
python3 core/fusion-api/audit-setup/scripts/audit_setup.py set-level \
  --product MDS \
  --audit-level Low \
  --token-cache auto
```

Disable product-level audit:

```bash
python3 core/fusion-api/audit-setup/scripts/audit_setup.py set-level \
  --product MDS \
  --audit-level None \
  --token-cache auto
```

To change overall Fusion Applications auditing, instruct the implementor to
perform this manual task in Fusion:

1. Open **Setup and Maintenance** and search for **Manage Audit Policies**.
2. Select **Oracle Fusion Applications**.
3. Change the audit level to **Auditing** or **None**.
4. Save the change and confirm the displayed value in the UI.

Do not attempt a REST fallback or report a profile-option read as proof that
the UI-level policy changed.

Interrogate auditable objects for a product:

```bash
python3 core/fusion-api/audit-setup/scripts/audit_setup.py get-setup \
  --application Receivables \
  --token-cache auto
```

Get audit history for a specific object:

```bash
python3 core/fusion-api/audit-setup/scripts/audit_setup.py get-history \
  --from-date 2026-04-17 \
  --to-date 2026-04-18 \
  --product Receivables \
  --business-object-type oracle.apps.cdm.foundation.parties.customerAccountService.view.CustomerAccountVO \
  --include-child-objects false \
  --include-attributes true \
  --attribute-detail-mode true \
  --token-cache auto
```

Get infrastructure-domain audit history without a business-object type:

```bash
python3 core/fusion-api/audit-setup/scripts/audit_setup.py get-history \
  --from-date 2026-09-01 \
  --to-date 2026-09-09 \
  --product SOA \
  --token-cache auto
```

Enable specific fields while retaining object-level auditing. Use a complete,
reviewed payload when changing fields because there is no API to retrieve the
current set of audit-enabled fields first:

```bash
python3 core/fusion-api/audit-setup/scripts/audit_setup.py update-status \
  --business-object oracle.apps.cdm.foundation.parties.organizationService.view.OrganizationDVO \
  --parent-business-object oracle.apps.cdm.foundation.parties.organizationService.view.OrganizationDVO \
  --enable ON \
  --attribute DUNSNumberC=true \
  --attribute StockSymbol=true \
  --token-cache auto
```

This produces the `update-auditstatus` field contract below (boolean values are
intentional):

```json
{
  "auditData": [
    {
      "businessObject": "oracle.apps.cdm.foundation.parties.organizationService.view.OrganizationDVO",
      "parentBusinessObject": "oracle.apps.cdm.foundation.parties.organizationService.view.OrganizationDVO",
      "enable": true,
      "attributesList": [
        { "attributeName": "DUNSNumberC", "isAuditable": true },
        { "attributeName": "StockSymbol", "isAuditable": true }
      ]
    }
  ]
}
```

To disable an individual field, submit that field with
`--attribute <attributeName>=false`. The command serializes `--enable ON|OFF`
as Boolean `true|false`, as required by the REST payload. Do not treat
`--enable OFF` as a field-level disable: it changes the business-object audit
state.

## Inputs

- `fusion_environment_context`
- `audit_setup_request`
- `execution_options`

Script-level inputs:

- `domains`: prints the supported product/domain code catalog for
  product-level audit levels.
- `applications`: prints the known functional application/product names used
  by `get-setup`.
- `get-level --product PRODUCT`: retrieves audit level for one or more
  products. Defaults to all known products when no `--product` is supplied.
- `set-level --product PRODUCT --audit-level LEVEL`: sets product-level audit.
- `get-setup --application APPLICATION`: retrieves auditable object metadata
  for a functional application such as `Receivables`.
- `get-history`: retrieves either functional application business-object
  history (supply `--business-object-type`) or `ESS`, `MDS`, `OPSS`, or `SOA`
  infrastructure-domain history (omit it). Both forms support the documented
  user, event, attribute-detail, impersonator, time-zone, and pagination
  filters.
- `check-status --business-object BO --parent-business-object PARENT`: checks
  business-object audit state.
- `update-status --business-object BO --parent-business-object PARENT --enable
  ON|OFF`: changes business-object audit state, serializing the value as a JSON
  Boolean. Add one or more
  `--attribute ATTRIBUTE=true|false` options to set individual field audit
  status in the same request.
- `--body-key auditData|auditDate`: selects the array key for endpoints that
  carry audit setup rows. The default is `auditData` because working examples
  use that key, while the 26B OpenAPI metadata uses `auditDate`.
- `--payload` or `--payload-file`: sends an exact JSON payload for advanced
  cases.
- `--application-metadata`: optional override for the local application/product
  catalog used by `applications` and `get-setup` diagnostics.
- `--token-cache`, `--force-login`, `--auth-code`, `--redirect-url`, and browser
  flags passed to the shared OAuth flow when login is required.

## Outputs

- `execution_result`
- `diagnostics`
- `audit_summary`

Script-level outputs:

- Structured JSON containing the endpoint called, request summary, raw Fusion
  response, normalized `auditData`, and target environment summary.
- Exit code `0`: Fusion returned a successful HTTP response and no clear
  `FAIL` status.
- Exit code `4`: Fusion returned an unsuccessful audit setup status in the
  response body.

## Implementation Notes

Use this utility instead of duplicating Audit Setup REST calls in pillar skills.
For implementation start-up, prefer:

1. `domains` to confirm available domains.
2. `applications` to confirm known functional application/product names.
3. `get-level` to capture current levels.
4. For a functional application history request, use `get-setup` for the
   target application to inspect available objects. For `ESS`, `MDS`, `OPSS`,
   or `SOA` history, query `get-history` with the domain code and no business
   object instead; those codes are not valid `get-setup` application values.
5. For the overall Fusion Applications switch, instruct the implementor to
   perform and confirm the UI task; do not call a Profile Options REST endpoint.
6. When the current audit-enabled field list is required, instruct the
   implementor to verify it in the Audit Setup UI; do not infer it from
   `get-setup`, `check-status`, or audit history.
7. `set-level` or `update-status` only after the user explicitly names what to
   audit and the desired level/state. For fields, require the exact field list
   and desired `isAuditable` value; do not claim or attempt to discover the
   currently enabled field list.

Never print access tokens, refresh tokens, client secrets, token-cache contents,
or Authorization headers.

The implementation may send authenticated REST requests only to HTTPS hosts
configured by `restBaseUrl` or `*_restBaseUrl` in
`core/auth/fusionEnv.properties`; it rejects all other hosts and redirects to
them.
