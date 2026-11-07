"""Local web server for the Clinical AI Agent demo."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from engine import Retriever

ROOT = Path(__file__).resolve().parent
INDEX = Retriever(ROOT / "data")


class Handler(BaseHTTPRequestHandler):
def respond(self, status, content, content_type):
self.send_response(status)
self.send_header("Content-Type", content_type)
self.send_header("Content-Length", str(len(content)))
self.send_header("X-Content-Type-Options", "nosniff")
self.end_headers()
self.wfile.write(content)

def do_GET(self):
if self.path != "/":
self.respond(404, b"Not found", "text/plain")
return

page = ROOT / "index.html"

if not page.exists():
self.respond(
503,
b"Browser interface not added yet.",
"text/plain",
)
return

self.respond(
200,
page.read_bytes(),
"text/html; charset=utf-8",
)

def do_POST(self):
if self.path != "/api/ask":
self.respond(404, b"Not found", "text/plain")
return

try:
size = int(self.headers.get("Content-Length", "0"))

if not 0 < size <= 8192:
raise ValueError("Invalid request size")

body = json.loads(self.rfile.read(size))
question = body.get("question")

if (
not isinstance(question, str)
or not question.strip()
or len(question) > 1000
):
raise ValueError("Invalid question")

result = INDEX.ask(question)

except (ValueError, AttributeError, UnicodeDecodeError):
self.respond(
400,
json.dumps({
"error": "Enter a question of 1 to 1000 characters."
}).encode("utf-8"),
"application/json",
)
return

self.respond(
200,
json.dumps(result).encode("utf-8"),
"application/json",
)


if __name__ == "__main__":
address = ("127.0.0.1", 8000)

print("Open http://127.0.0.1:8000 in your browser.")
print("Press Ctrl+C to stop.")

ThreadingHTTPServer(address, Handler).serve_forever()
