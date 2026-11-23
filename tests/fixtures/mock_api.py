#!/usr/bin/env python3
"""Deterministic stand-in for the Commit audit API (POST <prefix>/api/audit).

Path prefixes select behaviour:
  /api/audit                 normal batch responses
  /batch403/api/audit        403 for multi-package requests, 200 for single
  /error500/api/audit        always HTTP 500

Package name determines riskFlags:
  crit*  -> ["CRITICAL"]   high* -> ["HIGH"]   stale* -> ["STALE"]   else -> []

Each request is appended as a JSON line to /tmp/mock-api-requests.log.
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

LOG = "/tmp/mock-api-requests.log"


def result_for(name):
    if name.startswith("crit"):
        flags = ["CRITICAL"]
        score = 20
    elif name.startswith("high"):
        flags = ["HIGH"]
        score = 40
    elif name.startswith("stale"):
        flags = ["STALE"]
        score = 55
    else:
        flags = []
        score = 90
    return {
        "name": name,
        "ecosystem": "npm",
        "score": score,
        "riskFlags": flags,
        "maintainers": 1 if flags else 5,
        "weeklyDownloads": 25_000_000 if flags else 12_345,
        "ageYears": 7.5,
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._send(200, {"ok": True})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length).decode() if length else "{}"
        try:
            payload = json.loads(raw)
        except Exception:
            payload = {}
        pkgs = payload.get("packages", [])
        with open(LOG, "a") as f:
            f.write(json.dumps({
                "path": self.path,
                "auth": self.headers.get("Authorization", ""),
                "packages": pkgs,
            }) + "\n")

        if not self.path.endswith("/api/audit"):
            self._send(404, {"error": "not found"})
            return
        if self.path.startswith("/error500/"):
            self._send(500, {"error": "boom"})
            return
        if self.path.startswith("/batch403/") and len(pkgs) > 1:
            self._send(403, {"error": "batch requires pro"})
            return
        results = [result_for(p) for p in pkgs]
        self._send(200, {"count": len(results), "results": results})


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
