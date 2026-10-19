# Repository lifecycle

Use this reference for every request that can change a repository.

## Contents

- Discover
- Enforce the branch gate
- Plan and confirm
- Change minimally
- Verify
- Commit
- Push
- Recovery

## 1. Discover

Run:

```text
node <skill-root>/scripts/repository_preflight.js --repo <workspace> --json
```

Resolve `<skill-root>` from the loaded skill location and `<workspace>` from the
current Git repository or explicit user input. Never substitute a packaged
machine path.

Capture:

- Repository root and starting commit
- Current branch and upstream
- Remote default branch
- Ahead/behind state
- Modified, staged, and untracked files
- Extension topology and metadata
- Installed build and audit prerequisites
- Custom protected branches supplied by the repository or user
- Intended integration base for the complete reviewed change set

Redact credentials or user information embedded in remote URLs.

Local Git can prove branch names and tracking state, but not all server-side
branch policies. Report the protection source as built-in, remote-default,
explicit, or unknown.

## 2. Enforce the branch gate

Treat these as protected:

- `main`
- `master`
- The resolved remote default branch
- Any repository-declared protected branch

Reuse any named branch other than `main`, `master`, or the resolved remote
default branch. On one of those main branches, create a feature branch
automatically before editing. Derive a unique name from the requested feature,
use only 5-20 lowercase ASCII letters, and never include `codex`. Stop on a
detached HEAD or when a unique compliant name cannot be chosen safely.

If the worktree is dirty:

- Inventory the existing changes.
- Ask only when overlap or ownership is ambiguous.
- Do not stash, reset, revert, or rewrite user work automatically.
- Restrict the proposed scope to known target files.

## 3. Plan and confirm

Before editing:

1. Identify the page and effective configuration.
2. State the intended business behavior.
3. Record the files and properties expected to change in the internal handoff.
4. Identify prerequisites and unverified assumptions.
5. Explain the verification plan.
6. Obtain explicit change approval.

The final internal proposal is the implementation handoff. Include exact target files,
source fingerprints, evidence inputs, and planned content. When the user
unambiguously answers that proposal with `yes`, `implement`, or `IMPLEMENT`, do
not ask again and do not restart semantic feasibility analysis. Re-read the
approved target files and compare the recorded fingerprints; reassess only an
invalidated claim.

Repository access alone is not change approval.

## 4. Change minimally

- Change only Extension-owned artifacts.
- Preserve unrelated rules, expressions, properties, and files.
- Re-read a file immediately before editing.
- If the file differs from the inspected snapshot, stop and reassess.
- Keep build output, dependency folders, caches, credentials, and reports out
  of the source diff unless the user explicitly requests them.

## 5. Verify

Use `validate_extension_changes.js`, repository-provided tests, scenario checks,
and a final diff. Read [validation-and-vx.md](validation-and-vx.md).

For commit readiness, pass the intended integration base explicitly and
require a non-empty change set. After commit, require the exact reviewed `HEAD`
and a clean worktree:

```text
node <skill-root>/scripts/validate_extension_changes.js \
  --repo <workspace> \
  --base <integration-ref> \
  --expected-head <reviewed-commit> \
  --require-clean \
  --require-changes \
  --json
```

Classify every check as:

- Passed
- Failed
- Not run
- Not applicable

Never convert “not run” into “passed.”

After an `IMPLEMENT` request:

1. Build and validate the `.vx` locally.
2. Show the archive identity and target environment.
3. Send one deployment request and report its response.
4. Derive the deployed snapshot URL without requesting it.
5. Do not retry or poll.
6. Return the generated URL without opening it.

## 6. Commit

Only after deployment, user verification, and a new message that begins with
`COMMIT`:

1. Recheck the internally recorded task files and verification result.
2. Report all blocking and remaining non-blocking findings.
3. Treat `COMMIT` as approval for one scoped commit.
4. Create a feature-focused commit message.
5. Stage only approved files.
6. Commit without including unrelated changes.

Do not amend or rewrite existing commits unless the user explicitly requests
that operation.

## Recovery

Record the starting commit, created branch, committed paths, and generated
artifacts. Prefer a normal revert commit for published changes. Never use a
destructive reset as an implied rollback.
