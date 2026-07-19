<!-- markdownlint-disable -->

# Hardening Report: piiiico--proof-of-commitment/v1.14.1

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **piiiico--proof-of-commitment/v1.14.1** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): A ${{ }} expression is directly interpolated inside a run: shell command string. In action.yml, the composite action step uses `run: ${{ github.action_path }}/scripts/audit.sh`, which injects the github.action_path context value directly into the shell command before the shell ever sees it. Any ${{ ... }} inside a run: block is a script-injection risk regardless of the context source. The safe pattern is to use the $GITHUB_ACTION_PATH environment variable instead: `run: "$GITHUB_ACTION_PATH/scripts/audit.sh"`

Locations:

- `action.yml:62`

### unpinned-uses (severity: high)

Multiple workflow files reference actions by mutable tag instead of a full 40-character commit SHA, making them vulnerable to supply-chain attacks if the tag is moved or the upstream repository is compromised.

publish.yml:
- `uses: actions/checkout@v4` (line 14)
- `uses: actions/setup-node@v4` (line 17)
- `uses: actions/checkout@v4` (line 44)

supply-chain-audit.yml:
- `uses: actions/checkout@v4` (line 14)
- `uses: piiiico/commit-action@v1` (line 17)

All should be pinned to their full SHA digest, e.g. `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4`.

Locations:

- `.github/workflows/publish.yml:14`
- `.github/workflows/publish.yml:17`
- `.github/workflows/publish.yml:44`
- `.github/workflows/supply-chain-audit.yml:14`
- `.github/workflows/supply-chain-audit.yml:17`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses

**Notes:**

Fixed 3 issues across 3 files: (1) action.yml line 62: replaced `${{ github.action_path }}/scripts/audit.sh` with `"$GITHUB_ACTION_PATH/scripts/audit.sh"` to eliminate script injection via direct expression interpolation in run: command; (2) publish.yml: pinned actions/checkout@v4 → @34e114876b0b11c390a56381ad16ebd13914f8d5 (both occurrences) and actions/setup-node@v4 → @49933ea5288caeca8642d1e84afbd3f7d6820020; (3) supply-chain-audit.yml: pinned actions/checkout@v4 → @34e114876b0b11c390a56381ad16ebd13914f8d5 and piiiico/commit-action@v1 → @fc890899bde18ae82c77f4ab5cb0a12c1c660a67. All SHAs were resolved via lookup_action_sha.

