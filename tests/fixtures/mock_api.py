#!/usr/bin/env python3
"""Mock Commit audit API for act tests.

Usage: mock_api.py PORT MODE LOGFILE
  MODE: normal   -> 200 for every request
        batch403 -> 403 for multi-package requests (free tier), 200 for single
        error500 -> 500 for every request

Risk flags are derived from package names:
  contains "critical" -> CRITICAL
  contains "high"     -> HIGH
  contains "stale"    -> STALE
  otherwise           -> no flags
Each request (path, Authorization header, body) is appended to LOGFILE as JSON.
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(sys.argv[1])
MODE = sys.argv[2]
LOGFILE = sys.argv[3]


def result_for(name):
    flags = []
    downloads = 5000
    maintainers = 4
    score = 85
    if "critical" in name:
        flags = ["CRITICAL"]
        downloads = 50_000_000
        maintainers = 1
        score = 30
    elif "high" in name:
        flags = ["HIGH"]
        downloads = 2_000_000
        score = 45
    elif "stale" in name:
        flags = ["STALE"]
        downloads = 500
        score = 60
    return {
        "name": name,
        "ecosystem": "npm",
        "score": score,
        "riskFlags": flags,
        "weeklyDownloads": downloads,
        "maintainers": maintainers,
        "ageYears": 5.5,
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
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode() if length else ""
        try:
            payload = json.loads(raw)
        except Exception:
            payload = {}
        pkgs = payload.get("packages", [])
        with open(LOGFILE, "a") as f:
            f.write(json.dumps({
                "path": self.path,
                "auth": self.headers.get("Authorization", ""),
                "packages": pkgs,
            }) + "\n")
        if self.path != "/api/audit":
            self._send(404, {"error": "not found"})
            return
        if MODE == "error500":
            self._send(500, {"error": "internal error"})
            return
        if MODE == "batch403" and len(pkgs) > 1:
            self._send(403, {"error": "batch requires pro"})
            return
        results = [result_for(p) for p in pkgs]
        self._send(200, {"count": len(results), "results": results})


HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
