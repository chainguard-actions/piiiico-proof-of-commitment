<!-- markdownlint-disable -->

# Hardening Report: piiiico--proof-of-commitment/v1.31.1

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **piiiico--proof-of-commitment/v1.31.1** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): A ${{ }} expression is directly interpolated inside a `run:` shell command string in action.yml. The line `run: ${{ github.action_path }}/scripts/audit.sh` embeds `${{ github.action_path }}` directly in the run command. Although `github.action_path` is not attacker-controlled in the same way as `github.head_ref`, any `${{ ... }}` expression directly inside a `run:` block is a script-injection finding per the check rules — the value flows through YAML template substitution before the shell ever sees it. The safe alternative is to use the pre-set environment variable `$GITHUB_ACTION_PATH` instead.

Locations:

- `action.yml:68`

### unpinned-uses (severity: high)

Multiple `uses:` references in publish.yml are pinned to mutable tags rather than immutable 40-character SHA digests, making the workflow vulnerable to supply-chain attacks if those tags are moved. Failing references: `actions/checkout@v4` (line 17), `actions/setup-node@v4` (line 20), `oven-sh/setup-bun@v2` (line 30), `actions/checkout@v4` (line ~131, second job).

Locations:

- `.github/workflows/publish.yml:17`
- `.github/workflows/publish.yml:20`
- `.github/workflows/publish.yml:30`
- `.github/workflows/publish.yml:131`

### unpinned-uses (severity: high)

Multiple `uses:` references in supply-chain-audit.yml are pinned to mutable tags rather than immutable 40-character SHA digests. Failing references: `actions/checkout@v4` (line ~23), `piiiico/commit-action@v1` (line ~26), `github/codeql-action/upload-sarif@v3` (line ~39).

Locations:

- `.github/workflows/supply-chain-audit.yml:23`
- `.github/workflows/supply-chain-audit.yml:26`
- `.github/workflows/supply-chain-audit.yml:39`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses

**Notes:**

Fixed 3 findings across 3 files: (1) action.yml line 68: replaced `${{ github.action_path }}/scripts/audit.sh` with `$GITHUB_ACTION_PATH/scripts/audit.sh` to eliminate the script-injection finding. (2) publish.yml: pinned actions/checkout@v4 → @11d5960a326750d5838078e36cf38b85af677262 (both occurrences), actions/setup-node@v4 → @49933ea5288caeca8642d1e84afbd3f7d6820020, and oven-sh/setup-bun@v2 → @0c5077e51419868618aeaa5fe8019c62421857d6. (3) supply-chain-audit.yml: pinned actions/checkout@v4 → @11d5960a326750d5838078e36cf38b85af677262, piiiico/commit-action@v1 → @fc890899bde18ae82c77f4ab5cb0a12c1c660a67, and github/codeql-action/upload-sarif@v3 → @4187e74d05793876e9989daffde9c3e66b4acd07. All mutable tag references replaced with immutable full-SHA digests with the original tag preserved in a comment.

