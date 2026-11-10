<!-- markdownlint-disable -->

# Hardening Report: piiiico--proof-of-commitment/v0.5.1

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **piiiico--proof-of-commitment/v0.5.1** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): a GitHub Actions expression is placed directly into the run: command. Offending line: `run: ${{ github.action_path }}/scripts/audit.sh`. The value is substituted into the shell text before bash parses it, so a path containing shell metacharacters or spaces would be run as code. Fix: use the env var the runner already sets and quote it: `run: "$GITHUB_ACTION_PATH/scripts/audit.sh"`.

Locations:

- `action.yml:67`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Replaced `run: ${{ github.action_path }}/scripts/audit.sh` with `run: '"$GITHUB_ACTION_PATH/scripts/audit.sh"'` under shell: bash. The step still runs the same script, which is already executable.

