<!-- markdownlint-disable -->

# Hardening Report: piiiico--proof-of-commitment/v1.36.2

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **piiiico--proof-of-commitment/v1.36.2** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): a GitHub Actions expression is put directly into a run: shell command in the composite step 'Audit dependencies': `run: ${{ github.action_path }}/scripts/audit.sh`. Use the env var instead, e.g. `run: "$GITHUB_ACTION_PATH/scripts/audit.sh"`.

Locations:

- `action.yml:68`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

action.yml 'Audit dependencies' step now runs "$GITHUB_ACTION_PATH/scripts/audit.sh" (bash shell) instead of inlining ${{ github.action_path }}.

