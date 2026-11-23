<!-- markdownlint-disable -->

# Hardening Report: piiiico--proof-of-commitment/v0.5.2

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **piiiico--proof-of-commitment/v0.5.2** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a), direct expression interpolation: the composite step 'Audit dependencies' puts a GitHub Actions expression straight into its run: command: `run: ${{ github.action_path }}/scripts/audit.sh`. The runner substitutes the template text before the shell parses the line. The fix is to use the runner-provided env var, quoted: `run: "$GITHUB_ACTION_PATH/scripts/audit.sh"`.

Locations:

- `action.yml:68`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Replaced inline ${{ github.action_path }} in the bash run: of the 'Audit dependencies' step with the quoted runner-provided "$GITHUB_ACTION_PATH/scripts/audit.sh".

