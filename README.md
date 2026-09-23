# QwenOnLocalWifi

An offline, AI-powered learning assistant that runs entirely on a Raspberry Pi 5 and serves answers to students over a local WiFi hotspot. No internet connection is needed at any point after setup.

## Problem

Millions of students, smallholder farmers, and small business owners across rural Africa have phones but little or no affordable internet access. The information they need most, such as how to grow maize well, how to use mobile money safely, or how to apply for a farm loan, exists online but is out of reach. Schools and community centres in these areas often have no connectivity at all, so cloud-based AI tools and online courses are simply not an option.

See [PROBLEM.md](PROBLEM.md) for a fuller description of who is affected and why it matters now.

## Proposed Solution

A self-contained "knowledge box" built on a Raspberry Pi 5 that:

- **Runs a small language model locally.** Qwen 2.5 (1.5B) is served by Ollama on the Pi itself, so questions are answered on-device with no cloud calls.
- **Answers from curated, trusted content.** Plain-text guides in the `documents/` folder are chunked and indexed into ChromaDB on startup. Each question retrieves the most relevant sections and the model answers using only that reference material (retrieval-augmented generation). This keeps answers grounded and lets teachers add or edit content by dropping in a text file.
- **Broadcasts its own WiFi hotspot.** Any phone or laptop connects to the Pi's hotspot and opens a mobile-friendly web page in the browser. Nothing needs to be installed on the student's device.
- **Serves offline video.** Educational videos placed in `static/videos/` are listed and playable from the same page.

The web interface offers three learning topics: Agriculture & Farming, Digital Skills, and General Knowledge. Each topic gives the model a different persona prompt so answers are framed appropriately.

### How it works

```
Phone (browser) --WiFi hotspot--> Flask app on Raspberry Pi
                                      |
                                      |-- ChromaDB: retrieve top matching sections from documents/
                                      |-- Ollama + Qwen 2.5 1.5B: generate answer from those sections
                                      |
                                  <-- answer + response time
```

### Tech stack

| Layer | Choice |
|---|---|
| Hardware | Raspberry Pi 5 (8 GB), 32 GB SD card |
| LLM runtime | Ollama with `qwen2.5:1.5b` |
| Embeddings and retrieval | ChromaDB (default embedding function) |
| Web server | Flask, single-file app (`app.py`) |
| Networking | NetworkManager WiFi hotspot, served at `http://10.42.0.1:5000` |

## Current Progress

**Status: working prototype, tested end to end on a Raspberry Pi 5.**

Done:

- Flask application with home page, topic selection, chat interface, response timer, and video player.
- Automatic indexing of every `.txt` file in `documents/` into ChromaDB at startup.
- Retrieval-augmented question answering through Ollama and Qwen 2.5 1.5B.
- Quick canned replies for greetings and "help" so trivial messages skip the model.
- Six seed knowledge documents: maize farming, digital skills, general knowledge, bank loan products, how to apply for a loan, and government schemes for farmers.
- One sample farming tutorial video.
- Full installation guide for a fresh Raspberry Pi, including systemd services and hotspot setup, in [INSTALL.txt](INSTALL.txt).
- Measured performance on the Pi: roughly 2 to 5 seconds per answer, 3 to 5 concurrent users, 40 to 60 second boot.

Known limitations and next steps:

- Document indexing uses fixed IDs, so re-indexing on every restart can raise a duplicate-ID error that is caught and logged. Indexing should become idempotent or check for existing content.
- Quick-reply matching is a substring check, so a question containing "hi" (for example "which") can trigger the greeting. This should match whole words only.
- Content is currently English only. Swahili and other local-language documents and prompts are the highest-value addition.
- No teacher-facing admin page yet. Adding content requires copying files onto the Pi and restarting the service.
- The hotspot password and SSID are hard-coded in the install guide and should be configurable.
- No automated tests yet.

## Repository layout

```
app.py                  Flask app, indexing, retrieval, and inline HTML/JS UI
documents/              Plain-text knowledge base, one topic per file
static/videos/          Offline educational videos
INSTALL.txt             Step-by-step Raspberry Pi setup and troubleshooting
PROBLEM.md              Problem statement
```

## Quick start (on the Pi)

```bash
python3 -m venv venv && source venv/bin/activate
pip install flask chromadb ollama sentence-transformers pydantic requests
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull qwen2.5:1.5b
python3 app.py
```

Then connect a phone to the Pi's hotspot and open `http://10.42.0.1:5000`. Full details, including running everything as services on boot, are in [INSTALL.txt](INSTALL.txt).
