<!-- markdownlint-disable -->

# Hardening Report: piiiico--proof-of-commitment/v0.5.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **piiiico--proof-of-commitment/v0.5.0** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) violation: a GitHub Actions expression is placed directly in the run: command string of the composite step 'Audit dependencies': `run: ${{ github.action_path }}/scripts/audit.sh`. The value is substituted into the script text before the shell parses it, and it is unquoted. Fix: use the shell variable instead, quoted: `run: "$GITHUB_ACTION_PATH/scripts/audit.sh"`.

Locations:

- `action.yml:66`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Replaced `run: ${{ github.action_path }}/scripts/audit.sh` with the quoted shell variable `"$GITHUB_ACTION_PATH/scripts/audit.sh"` (bash step); invocation semantics unchanged.

