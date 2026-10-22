#!/usr/bin/env python3
"""Deterministic mock of the Commit audit API (POST <prefix>/api/audit).

Risk classification is derived from the package name:
  crit-*  -> CRITICAL
  high-*  -> HIGH
  stale-* -> STALE (warning)
  other   -> no flags (OK)

Path prefixes select special behaviors:
  /fail500/api/audit  -> always HTTP 500
  /batch403/api/audit -> HTTP 403 when more than one package is requested
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

LOG = "/tmp/mock-api-requests.log"


class Server(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def result_for(name):
    flags = []
    if name.startswith("crit-"):
        flags = ["CRITICAL"]
    elif name.startswith("high-"):
        flags = ["HIGH"]
    elif name.startswith("stale-"):
        flags = ["STALE"]
    return {
        "name": name,
        "ecosystem": "npm",
        "score": 42,
        "riskFlags": flags,
        "maintainers": 1,
        "weeklyDownloads": 12_000_000,
        "ageYears": 5.5,
    }


class Handler(BaseHTTPRequestHandler):
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
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw or b"{}")
        except Exception:
            payload = {}
        pkgs = payload.get("packages", []) or []
        with open(LOG, "a") as f:
            f.write(json.dumps({"path": self.path,
                                "auth": self.headers.get("Authorization", ""),
                                "packages": pkgs}) + "\n")
        if not self.path.endswith("/api/audit"):
            self._send(404, {"error": "not found"})
            return
        if self.path.startswith("/fail500"):
            self._send(500, {"error": "internal error"})
            return
        if self.path.startswith("/batch403") and len(pkgs) > 1:
            self._send(403, {"error": "batch requires pro"})
            return
        results = [result_for(p) for p in pkgs]
        self._send(200, {"count": len(results), "results": results})

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 18080
    Server(("127.0.0.1", port), Handler).serve_forever()
