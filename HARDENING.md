<!-- markdownlint-disable -->

# Hardening Report: piiiico--proof-of-commitment/v1.36.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **piiiico--proof-of-commitment/v1.36.0** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): A `${{ ... }}` expression is interpolated directly inside a `run:` shell command string in action.yml. The line `run: ${{ github.action_path }}/scripts/audit.sh` embeds the `github.action_path` context value directly into the shell command before the shell ever sees it. Per the check rules, any `${{ ... }}` expression directly inside a `run:` block is a script-injection finding regardless of which context it reads from.

Locations:

- `action.yml:68`

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions by mutable tags instead of full 40-character commit SHAs, making them vulnerable to supply-chain attacks if the referenced tag is moved. Failing references:

.github/workflows/publish.yml:
- `actions/checkout@v4` (line 17)
- `actions/setup-node@v4` (line 20)
- `oven-sh/setup-bun@v2` (line 31)
- `actions/checkout@v4` (second job, ~line 133)

.github/workflows/supply-chain-audit.yml:
- `actions/checkout@v4` (line 21)
- `piiiico/commit-action@v1` (line 24)
- `github/codeql-action/upload-sarif@v3` (line 33)

.github/workflows/test.yml:
- `actions/checkout@v4` (line 50)
- `oven-sh/setup-bun@v2` (~line 73)

Locations:

- `.github/workflows/publish.yml:17`
- `.github/workflows/supply-chain-audit.yml:21`
- `.github/workflows/test.yml:50`

### missing-permissions (severity: medium)

The workflow file test.yml has no top-level `permissions:` key and the single job `contract-tests` also has no job-level `permissions:` block. Without explicit permissions, the job inherits the default repository token permissions, which may be broader than necessary (e.g., write access to contents, pull-requests, etc.).

Locations:

- `.github/workflows/test.yml:1`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses, missing-permissions

**Notes:**

Fixed all three findings: (1) script-injection in action.yml: moved github.action_path from the run: command into the env: block as ACTION_PATH, referenced as $ACTION_PATH in the shell; (2) unpinned-uses: pinned all 8 action references across publish.yml, supply-chain-audit.yml, and test.yml to full 40-char commit SHAs with tag comments; (3) missing-permissions in test.yml: added top-level 'permissions: contents: read' block (minimum needed for checkout).

