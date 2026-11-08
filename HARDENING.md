<!-- markdownlint-disable -->

# Hardening Report: piiiico--proof-of-commitment/v0.4.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **piiiico--proof-of-commitment/v0.4.0** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): a GitHub Actions expression is placed directly in a run: shell command in the composite step 'Audit dependencies': `run: ${{ github.action_path }}/scripts/audit.sh`. The value is substituted into the YAML before the shell runs and is not quoted. Fix: set the env var ACTION_PATH: ${{ github.action_path }} and run `"$ACTION_PATH/scripts/audit.sh"` (or use "$GITHUB_ACTION_PATH/scripts/audit.sh").

Locations:

- `action.yml:70`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, I changed the 'Audit dependencies' step from `run: ${{ github.action_path }}/scripts/audit.sh` to `run: '"$GITHUB_ACTION_PATH/scripts/audit.sh"'`. The step's shell is bash, so the double-quoted $VAR form is correct there. The script still runs directly, as upstream ran it, so it still depends on its own executable bit and shebang. Nothing else was changed and nothing was run to test it.

