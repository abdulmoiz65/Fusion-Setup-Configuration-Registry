# Partial REST identity observations

The routed workflow may select this assisted evidence step when a candidate
contains explicit organization party, party-site and account numbers, with
BILL_TO or SHIP_TO purpose. It is useful for checking known existing identities
before a proposed change or observing them after import. It does not prove
create/update eligibility, global absence, active status or a complete outcome.

Read the existing core REST skill and its standard Fusion REST instructions.
The selected environment/profile must match, the principal must have read
privileges for the organization and account-site resources, and the scope must
be authorized by the active workflow. Retain evidence in a new private directory
outside the checkout. Never put tokens or raw customer responses in Git.

Invoke the existing `scripts/customer_api_collect.py` with its normal candidate,
operation, phase, environment, repo, properties, token-cache and output arguments,
adding `--read-scope rest-identity`. The default remains `complete`, which uses the task-owned SOAP adapter alongside
the existing REST reads. This option does not run SOAP,
extract views, authentication code owned by this task, or a direct HTTP client.
It delegates fixed GETs to the existing central CLI.

For each of at most 20 candidate rows, the mode performs three bounded GETs:

1. `hubOrganizations` with `PartyNumberRF` and the exact candidate party number.
2. That party's `Address` item using the candidate party-site number.
3. `customerAccountSitesLOV` using the exact account number and site purpose.

Selectors accept only letters, digits, underscore, dot and hyphen. Missing or
unsupported selectors fail before profile access. Missing, ambiguous, incomplete,
foreign-parent or malformed responses fail closed. Results larger than the
bounded page are incomplete; the mode does not enumerate more broadly. An empty
LOV cannot prove account absence. Large IDs are retained as strings.

`rest-identity-review.json` binds the candidate hash, environment, phase, task
implementation hashes and timestamped capture interval to raw response hashes.
`PARTIAL_REST_IDENTITIES_MATCH` means the returned party identity, scoped address
owner/location and visible account/party association agree. The address-to-account
site link is explicitly not proven. Authentication is delegated to core; this
report does not independently certify the principal's identity or visibility.

The same Address response also supplies selected location values. Before-phase
captures record those values without comparing them to proposed changes.
After-phase captures compare only explicitly supplied candidate values using exact
text. Missing fields remain unknown; explicit null is retained; omitted input is
not an expected null, default or preservation claim. Requested mismatches or
unavailable values produce `PARTIAL_REST_VALUE_REVIEW_REQUIRED` and exit code 2.
The short description, tax geocode, inside-city-limit flag and timezone remain
unexposed by this mapping. No additional REST requests are made for this check.

The documented field basis is Oracle's [organization Address GET](https://docs.oracle.com/en/cloud/saas/sales/faaps/op-huborganizations-partynumber-child-address-addressnumber-get.html).
The [account-site LOV contract](https://docs.oracle.com/en/cloud/saas/financials/26c/farfa/op-customeraccountsiteslov-get.html)
does not establish a full party-site/account-site join or persisted DFF values.
An active customer profile is distinct from a profile-class LOV. Source-reference
rows are not source-system name/code configuration validation. No guessed APIs,
extract views, SOAP-through-POST or weaker matching are substituted for these gaps.

All outcomes retain `execution_authorized=false`,
`persisted_reconciliation_complete=false` and
`full_functional_reconciliation=false`. They use a distinct schema and output
filename, not the full collector/replay contract. Source-system resolution,
cross-party site discovery, account/site/use hierarchy, profile, DFF, full values,
operation ownership and central Data Loader dependencies remain outstanding.
Do not feed this report to a full-evidence gate or reinterpret a partial match as
an approval override. Existing historical evidence keeps its original revision.
