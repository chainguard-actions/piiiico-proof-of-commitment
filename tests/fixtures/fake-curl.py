#!/usr/bin/env python3
"""Fake curl for the Commit audit API.

Intercepts POST .../api/audit calls and returns canned results.
Mode is read from /tmp/fake-curl/mode:
  ok        -> batch request returns 200
  batch403  -> multi-package request returns 403, single-package returns 200
  error500  -> every request returns 500
Packages whose name starts with "critical-" get the CRITICAL risk flag,
"high-" gets HIGH. Every payload is appended to /tmp/fake-curl/payloads.log.
Any other URL falls through to the real curl.
"""
import json
import os
import sys

STATE = "/tmp/fake-curl"
args = sys.argv[1:]

if not any("/api/audit" in a for a in args):
    for real in ("/usr/bin/curl", "/bin/curl", "/usr/local/bin/curl"):
        if os.path.exists(real):
            os.execv(real, [real] + args)
    sys.exit(127)

out = None
data = None
wfmt = None
i = 0
while i < len(args):
    a = args[i]
    if a in ("-o", "--output") and i + 1 < len(args):
        out = args[i + 1]
        i += 2
        continue
    if a in ("-d", "--data", "--data-raw") and i + 1 < len(args):
        data = args[i + 1]
        i += 2
        continue
    if a in ("-w", "--write-out") and i + 1 < len(args):
        wfmt = args[i + 1]
        i += 2
        continue
    i += 1

os.makedirs(STATE, exist_ok=True)
try:
    mode = open(os.path.join(STATE, "mode")).read().strip()
except OSError:
    mode = "ok"

with open(os.path.join(STATE, "payloads.log"), "a") as f:
    f.write((data or "") + "\n")

try:
    pkgs = json.loads(data or "{}").get("packages", [])
except Exception:
    pkgs = []

if mode == "error500":
    code = "500"
    body = json.dumps({"error": "internal error"})
elif mode == "batch403" and len(pkgs) > 1:
    code = "403"
    body = json.dumps({"error": "batch requires pro"})
else:
    code = "200"
    results = []
    for p in pkgs:
        flags = []
        if p.startswith("critical-"):
            flags = ["CRITICAL"]
        elif p.startswith("high-"):
            flags = ["HIGH"]
        results.append({
            "name": p,
            "ecosystem": "npm",
            "score": 42 if flags else 85,
            "riskFlags": flags,
            "maintainers": 1 if flags else 5,
            "weeklyDownloads": 20000000 if flags else 50000,
            "ageYears": 6.5,
        })
    body = json.dumps({"count": len(results), "results": results})

if out:
    with open(out, "w") as f:
        f.write(body)
else:
    sys.stdout.write(body)

if wfmt and "http_code" in wfmt:
    sys.stdout.write(code)
sys.exit(0)
