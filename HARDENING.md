<!-- markdownlint-disable -->

# Hardening Report: piiiico--proof-of-commitment/v1.14.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **piiiico--proof-of-commitment/v1.14.0** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Both workflow files use mutable tag-based refs instead of pinned full SHA commits, making them vulnerable to supply-chain attacks if the referenced actions are compromised or tags are moved.

.github/workflows/publish.yml:
- `uses: actions/checkout@v4` (tag, not SHA)
- `uses: actions/setup-node@v4` (tag, not SHA)

.github/workflows/supply-chain-audit.yml:
- `uses: actions/checkout@v4` (tag, not SHA)
- `uses: piiiico/commit-action@v1` (version string, not SHA)

Locations:

- `.github/workflows/publish.yml:14`
- `.github/workflows/supply-chain-audit.yml:18`

### script-injection (severity: high)

Sub-rule (a): The run: block in action.yml directly interpolates a ${{ ... }} expression inside the shell command string: `run: ${{ github.action_path }}/scripts/audit.sh`. Any ${{ ... }} expression directly inside a run: shell command string is a script-injection risk because the value is substituted by the YAML template engine before the shell ever sees it. The safe alternative is to use the $GITHUB_ACTION_PATH environment variable instead.

Locations:

- `action.yml:68`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection

**Notes:**

Fixed all three findings:
1. publish.yml: Pinned actions/checkout@v4 → @11d5960a326750d5838078e36cf38b85af677262 and actions/setup-node@v4 → @49933ea5288caeca8642d1e84afbd3f7d6820020.
2. supply-chain-audit.yml: Pinned actions/checkout@v4 → @11d5960a326750d5838078e36cf38b85af677262 and piiiico/commit-action@v1 → @fc890899bde18ae82c77f4ab5cb0a12c1c660a67.
3. action.yml: Replaced `run: ${{ github.action_path }}/scripts/audit.sh` with `run: "$GITHUB_ACTION_PATH/scripts/audit.sh"` to eliminate the script-injection risk — $GITHUB_ACTION_PATH is a pre-set environment variable that the shell resolves safely, not a YAML-template expression.

