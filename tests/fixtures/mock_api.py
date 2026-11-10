#!/usr/bin/env python3
"""Local stand-in for the Commit audit API, used via the action's api-url input.

Usage: mock_api.py PORT [MODE]
  MODE=ok      (default) always 200
  MODE=batch403  403 for multi-package requests, 200 for single-package
  MODE=error   always 500

Package name conventions:
  crit-*  -> riskFlags ["CRITICAL"]
  high-*  -> riskFlags ["HIGH"]
  warn-*  -> riskFlags ["NO_RECENT_RELEASE"]
  others  -> no flags
Every request body is appended to /tmp/mock-requests.jsonl.
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(sys.argv[1])
MODE = sys.argv[2] if len(sys.argv) > 2 else "ok"
LOG = "/tmp/mock-requests.jsonl"


def result_for(name):
    flags = []
    if name.startswith("crit-"):
        flags = ["CRITICAL"]
    elif name.startswith("high-"):
        flags = ["HIGH"]
    elif name.startswith("warn-"):
        flags = ["NO_RECENT_RELEASE"]
    return {
        "name": name,
        "ecosystem": "npm",
        "score": 42,
        "riskFlags": flags,
        "maintainers": 1,
        "weeklyDownloads": 12000000,
        "ageYears": 5.0,
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send(200, {"ok": True})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode() if length else "{}"
        try:
            payload = json.loads(raw)
        except Exception:
            payload = {}
        pkgs = payload.get("packages", [])
        with open(LOG, "a") as f:
            f.write(json.dumps({"path": self.path, "packages": pkgs,
                                "auth": self.headers.get("Authorization", "")}) + "\n")
        if self.path != "/api/audit":
            self._send(404, {"error": "not found"})
            return
        if MODE == "error":
            self._send(500, {"error": "internal"})
            return
        if MODE == "batch403" and len(pkgs) > 1:
            self._send(403, {"error": "batch requires pro"})
            return
        results = [result_for(p) for p in pkgs]
        self._send(200, {"count": len(results), "results": results})


HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
