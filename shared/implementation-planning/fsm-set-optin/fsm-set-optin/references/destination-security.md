# FSM opt-in destination security

## Finding and status

H13 / Union CS3 (High), tracked as ATEAM-1462 in the supplied fix bundle,
concerns tokens sent outside the approved service origin through overrides,
redirects, and pagination. This remediation is separate from H08 / ATEAM-1457
and REST/UCM findings. Local implementation and tests do not close CS3;
independent retest and Murillo Pontual's recorded Security acceptance remain
required. Confirm the engineering owner and target dates with Abhay Kumar.

The opt-in code at base commit `00afbf5bc03729196ddd808556edd579d66af7b4`
matches the reported `f828a265480d445d775ff822b8e711784bfcc0e2` baseline.
It acquired profile-scoped tokens while accepting an independent `--base-url`,
used unguarded `urlopen`, and followed BOSS next links without origin checks.
The shared OAuth host guard was not invoked by this implementation and permits
multiple configured service origins, so it did not close this separate finding.

## Trust boundary

The caller selects a trusted environment profile through the existing
`--properties` mechanism. Protect that profile, its `restBaseUrl`, the Python
runtime, and the repository installation against unauthorized modification.
An attacker-controlled profile is not a trust anchor. This fix does not approve
arbitrary profiles, isolate token caches, or change OAuth endpoint handling.

The CLI derives `approved_origin` only from that profile. A `--base-url`,
redirect Location, or pagination href cannot redefine it. Other `*_restBaseUrl`
properties do not expand the opt-in allowlist. All three contexts currently
share the same approved origin but retain their distinct tokens and scopes.

Origin comparison uses HTTPS scheme, normalized hostname, and effective port
(443 by default). Host case and explicit default ports are equivalent; foreign
hosts, changed ports, HTTP downgrades, embedded credentials, control characters,
backslashes, encoded hostnames, and malformed authorities fail closed.

## Enforcement and compatibility

- `fsm_set_optin.py` validates the override before obtaining any token. Offering,
  functional-area, and feature wrappers inherit the same boundary.
- Python entry points require an explicit `approved_origin` from trusted
  configuration, separately from `base_url`/request URL. This applies to
  `run_set_optin`, `BossClient`, `request_json`, `lookup_code_api`,
  `patch_feature`, and `refresh_feature_selections`.
- `core/fusion-api/rest-api-client/scripts/trusted_http.py` validates the initial
  destination and every redirect hop, without token acquisition or refresh.
  Same-origin GET/HEAD redirects retain the method. Cross-origin redirects and
  automatic write redirects are blocked before the next request.
  The engine loads this helper from its own checkout's exact core path; a
  missing or redirected helper fails closed without module-search fallback.
- BOSS next links resolve against the final response URL, then pass through the
  same guard. Valid absolute/relative links and offset pagination remain usable.
- Destination failures raise `OptinError` without entering the 401/403 refresh
  branch. They do not echo sensitive URL values. `--force`, explicit tokens,
  and dry runs do not bypass this rule. A dry run still makes authorized reads.
- OAuth flows, scopes, caches, feature selection, disable checks, PATCH/refresh
  payloads, and public report result shapes remain unchanged. The final URL is
  retained internally only where pagination needs it.
- Existing multi-service REST clients are not silently migrated to the new
  strict transport. Their separate host-guard policy remains unchanged.

On a post-write failure, an approved-origin PATCH or refresh may already have
succeeded. Do not replay the workflow automatically; verify the current state
through the approved workflow before proposing recovery.

## Verification and closure evidence

From the repository root, without live Fusion access:

```sh
python3 -B -m unittest discover -s shared/implementation-planning/fsm-set-optin/fsm-set-optin/tests -v
python3 -B -m unittest discover -s core/auth/fusion-oauth-authentication/tests -v
git diff --check
```

Tests use synthetic bearer tokens and an in-memory HTTP transport with actual
urllib redirect processing. Socket/DNS access is blocked. Assertions check that
unauthorized destinations receive no request, not merely that a later exception
occurs. Coverage includes all token contexts, all three wrappers, overrides,
301/302/303/307/308 and chained redirects, malicious pagination, direct Python
callers, force/explicit-token/dry-run paths, no retry on destination rejection,
scope/cache preservation, unchanged report shapes, and valid entity payloads.

The H13 portion of the supplied ZIP was adapted rather than copied wholesale:
current FSCR layout discovery is retained; malformed-authority checks and
regression coverage are expanded. No H08 or Data Loader replacement from the ZIP
is part of this change.

### Local developer results — 2026-09-18

- Destination/security regression suite: 21 tests passed on Python 3.14.7 and
  Python 3.9.6, with real network access blocked by the test harness.
- Existing shared OAuth host-guard suite: 3 tests passed.
- FSM Designer regression suite: 72 of 73 tests passed; only the pre-existing
  task-ID expectation failure remains (`12` versus `ORA_EXISTING_TASK`). The
  existing H08 security fix is preserved, not replaced with the ZIP version.
- Raw opt-in CLI and all three entity wrappers: `--help` passed.
- Changed manifests: repository schema checks passed. `git diff --check` passed.

These are uncommitted developer-worktree results, not an independent CS3 retest.
Re-run and attach evidence against the final committed revision before review.

Before closure, attach the fix/merge revision, test output for that exact
revision, separate independent CS3 retest results, and Murillo's recorded
Security disposition. Complete the repository's committed-HEAD skill audit
before merge; uncommitted local tests are not a merge or Security approval.
