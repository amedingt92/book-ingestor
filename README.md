# 📚 Book-Ingestor

**Book-Ingestor** is the backbone of an AI-powered educational platform designed to deeply analyze books—particularly plain-text `.txt` files from Project Gutenberg. Built for legacy-grade homeschooling and intellectual formation, this system transforms raw text into moral, literary, and theological insight.

---

## 🔥 Vision

This isn't just a reading tool. It's a complete ingestion engine that automates:

- Classical education principles
- Moral worldview analysis
- Chapter-level insight extraction
- AI-powered summarization
- Christian formation through literature

> “A good book is the axe for the frozen sea within us.” — Kafka
> This project aims to sharpen that axe for generations.

---

## 🧠 Key Features (Planned + Completed)

| Feature                            | Status   | Description |
|------------------------------------|----------|-------------|
| 🔐 Secure project scaffolding       | ✅ Done  | Environment config, pre-commit, `.env`, `detect-secrets` |
| 📂 Gutenberg .txt ingestion         | ✅ Done  | Load, clean, and parse large classic texts |
| 🧠 AI chapter + book summaries      | 🔜 Next  | GPT-4, HuggingFace, or T5 summaries per chapter |
| 📊 Sentiment + theme analysis       | 🔜 Planned | Emotion timelines, virtue/vice arcs |
| 👤 Character tracking + networks    | 🔜 Planned | POV detection, dialogue mapping, character arcs |
| ✝️ Christian worldview lens         | 🔜 Planned | Moral analysis of themes, actions, quotes |
| 📋 Quote extraction by theme        | 🔜 Planned | Organize by virtue, vice, theology, lesson |
| 🧾 Export reports & dashboards      | 🔜 Planned | HTML, Markdown, JSON, PDF, and Anki export options |
| 👨‍👩‍👧 Personalized learning paths   | 🔜 Planned | Flashcard output per child, age-adjusted filters |

---

## 🧱 Architecture Summary

Modular, pluggable, and future-proof:

- **Language Tools**: `spaCy`, `nltk`, `transformers`, `torch`
- **Visualization**: `matplotlib`, `plotly`, (eventually `Streamlit` or `Flask`)
- **Security**: `pre-commit`, `detect-secrets`, `.env.template`, `.gitignore`
- **Extensibility**: YAML configs, CLI, optional GUI
- **Versioning**: All text and insight tracked and structured for reproducibility

---

## 📁 Folder Layout (Current)

```
book-ingestor/
├── books/                   # ✅ Raw books to be ingested
├── src/
│   ├── ingest.py           # ✅ Handles book loading and cleaning
│   └── structure.py        # ✅ Detects chapter breaks
├── tests/
│   ├── test_ingest.py      # ✅ Unit tests for ingestion
│   └── test_structure.py   # ✅ Unit tests for chapter detection
├── .env.template           # ✅ Safe format for secrets
├── .gitignore              # ✅ Ignores `.env`, outputs, etc.
├── .pre-commit-config.yaml # ✅ Security & code quality hooks
├── pytest.ini              # ✅ Pytest test discovery config
├── requirements.txt        # ✅ All dependencies (runtime + dev)
├── README.md               # ✅ This file
```

---

## 🚀 Project Roadmap

| Phase        | Description                                 | Status  |
|--------------|---------------------------------------------|---------|
| ✅ Phase 0   | Secure project setup, secrets management    | Done    |
| ✅ Phase 1   | Book ingestion, cleaning, chapter detection | Done    |
| 🔜 Phase 2   | Chapter summaries via GPT / HuggingFace     | Next    |
| 🔜 Phase 3   | Sentiment + emotion timeline analysis       | Planned |
| 🔜 Phase 4   | Character graphs + interaction modeling     | Planned |
| 🔜 Phase 5   | Thematic tagging + quote clustering         | Planned |
| 🔜 Phase 6   | Moral overlays + worldview alignment        | Planned |
| 🔜 Phase 7   | HTML/PDF/Markdown/Anki export engine        | Planned |
| 🔜 Phase 8   | Streamlit/Flask UI for reading insights     | Planned |

---

## 🧠 Why This Matters

This tool supports:

- Parents teaching the classics to children
- Readers extracting lessons at scale
- Educators generating summaries and virtue maps
- Homeschoolers layering tech into traditional learning

Books are the backbone of cultural memory. This makes that memory searchable, moral, and generative.

---

## 🛡️ Security Philosophy

- No real secrets are committed — `.env` is ignored
- `.secrets.baseline` is kept local
- GitHub repo is public but hardened via:
  - Auto-formatting
  - Secret scanners
  - Large file filters
  - YAML validation

---

## 🛠️ Getting Started

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pre-commit install
pre-commit run --all-files
cp .env.template .env  # Then fill in your real secrets
```

---

## 🪪 License

MIT License — use, modify, expand. Designed for learning.

---

## 🤝 Contributing

Open to PRs once Phase 2 is underway. Ideas and issues welcome now.

---

## ✍️ Author

Created by **Austin Edington**
Inspired by Christian classical education, modern AI tooling, and moral formation.
