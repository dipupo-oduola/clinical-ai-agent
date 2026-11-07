# Clinical AI Agent

A small local clinical-document search prototype. It searches synthetic study
documents and returns the most relevant passages with paragraph-level source
citation metadata.

## Current implementation

- `app.py` runs a local HTTP server and serves the browser interface from
	`index.html`.
- `engine.py` implements keyword retrieval with term-frequency and inverse
	document-frequency-style scoring.
- Documents are read from `data/*.md` at startup. The included
	`sample-protocol.md` is synthetic portfolio data.
- Results include the source filename, paragraph number, and matching passage.
- This project uses keyword retrieval only. It has no LLM, generative model,
	external API, or AWS deployment.

## Setup and run

The project uses only the Python standard library; no package installation is
required.

From the project directory, run:

```bash
python app.py
```

Then open <http://127.0.0.1:8000> in a browser. Stop the server with `Ctrl+C`.

## Example questions

Try questions such as:

- What is the screening window?
- What is the consent process?
- How are deviations recorded?
- What happens at the baseline visit?

The server accepts questions from 1 to 1000 characters. Questions are matched
against the available document text, so wording that shares relevant keywords
will produce the best results.

## Source citations

Each returned passage is cited using its source filename and paragraph number,
for example `sample-protocol.md - paragraph 2`. The citation identifies the
synthetic source passage used by the keyword search; it is not a citation to
real clinical guidance.

## Limitations

- The documents and study details are fictional and intended for demonstration
	only.
- Retrieval is based on keywords, not semantic understanding or an LLM.
- The search corpus is limited to Markdown files in `data/` loaded when the
	server starts.
- There is no authentication, persistence, production deployment, or AWS
	infrastructure.
- The output is not medical advice and must not be used for clinical decisions.
