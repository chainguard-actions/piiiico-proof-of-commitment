#!/usr/bin/env python3
"""Minimal mock of the Commit audit API (POST /api/audit).

Usage: mock_server.py <mode> <port> <request-log>

Modes:
  ok        - every package is returned with no risk flags
  critical  - package named "axios" is CRITICAL, others OK
  error     - always HTTP 500
  batch403  - requests with >1 package get HTTP 403; single-package requests OK
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

MODE = sys.argv[1]
PORT = int(sys.argv[2])
LOG = sys.argv[3]


def result_for(name):
    flags = []
    if MODE == "critical" and name == "axios":
        flags = ["CRITICAL"]
    return {
        "name": name,
        "ecosystem": "npm",
        "score": 42 if flags else 85,
        "riskFlags": flags,
        "maintainers": 1 if flags else 4,
        "weeklyDownloads": 50000000 if flags else 1500000,
        "ageYears": 9.5,
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write(fmt % args + "\n")

    def _send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._send(200, {"status": "ok"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode() if length else ""
        with open(LOG, "a") as f:
            f.write(json.dumps({
                "path": self.path,
                "auth": self.headers.get("Authorization", ""),
                "body": raw,
            }) + "\n")
        try:
            pkgs = json.loads(raw).get("packages", [])
        except Exception:
            self._send(400, {"error": "bad json"})
            return
        if MODE == "error":
            self._send(500, {"error": "internal error"})
            return
        if MODE == "batch403" and len(pkgs) > 1:
            self._send(403, {"error": "batch requires pro"})
            return
        results = [result_for(p) for p in pkgs]
        self._send(200, {"count": len(results), "results": results})


HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
