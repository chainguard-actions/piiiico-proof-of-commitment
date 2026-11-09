<!-- markdownlint-disable -->

# Hardening Report: piiiico--proof-of-commitment/v0.4.1

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **piiiico--proof-of-commitment/v0.4.1** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a), direct expression interpolation: the composite step 'Audit dependencies' puts a GitHub Actions expression straight into its run: line: `run: ${{ github.action_path }}/scripts/audit.sh`. The expression is substituted into the shell script text before bash parses it, and the result is unquoted. Fix: use the runner-provided env var with double quotes, i.e. `run: "$GITHUB_ACTION_PATH/scripts/audit.sh"`.

Locations:

- `action.yml:68`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the 'Audit dependencies' step used to run `${{ github.action_path }}/scripts/audit.sh`. It now runs `"$GITHUB_ACTION_PATH/scripts/audit.sh"` (YAML-quoted). The step still uses shell: bash and calls the script directly, as upstream did. Nothing else was changed.

