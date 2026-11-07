"""Offline document retrieval with exact source citations."""

import math
import re
from collections import Counter
from pathlib import Path

STOP_WORDS = set(
"what is the a an of to for in are and does how "
"when should be do this with".split()
)


def tokenize(text):
return [
word
for word in re.findall(r"[a-z0-9]+", text.lower())
if word not in STOP_WORDS
]


class Retriever:
def __init__(self, folder):
self.chunks = []

for path in sorted(Path(folder).glob("*.md")):
paragraphs = path.read_text(
encoding="utf-8"
).split("\n\n")

for number, paragraph in enumerate(paragraphs, 1):
text = paragraph.strip()

if text and not text.startswith("#"):
self.chunks.append({
"source": path.name,
"paragraph": number,
"text": text,
})

self.counts = [
Counter(tokenize(chunk["text"]))
for chunk in self.chunks
]

def ask(self, question):
terms = set(tokenize(question))

if not terms:
return {
"status": "no_evidence",
"passages": [],
}

total = len(self.counts)
ranked = []

for chunk, counts in zip(self.chunks, self.counts):
score = 0.0

for term in terms:
if counts[term]:
frequency = sum(
term in document
for document in self.counts
)
score += (
(1 + math.log(counts[term]))
* math.log(
1 + total / (1 + frequency)
)
)

coverage = (
len(terms.intersection(counts))
/ len(terms)
)

if score > 0 and coverage >= 0.5:
ranked.append({
**chunk,
"score": round(score, 3),
})

ranked.sort(
key=lambda item: item["score"],
reverse=True,
)

return {
"status": (
"evidence_found"
if ranked
else "no_evidence"
),
"passages": ranked[:3],
}
