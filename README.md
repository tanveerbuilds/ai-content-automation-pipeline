# ai-content-automation-pipeline

> **Sample / demo build** — a minimal content pipeline: reads topics from `topics.json` and drafts a blog outline, a product description, and three social posts per topic. Built for learning and demonstration, not production use.

## What this sample demonstrates

- **Topic-driven pipeline** — one topics file in, a folder of drafts out
- **Two modes** — `--dry-run` works with no API key (template drafts), full mode calls the OpenAI API
- **Organized output** — each topic gets its own dated folder with `blog.md`, `product.md`, and `social.md`

## Project structure

```
.
├── pipeline.py     # Sample pipeline (dry-run by default)
├── topics.json     # Example topics to draft about
└── README.md
```

## How to run the sample

```bash
pip install -r requirements.txt

# Template drafts, no API key needed
python pipeline.py --dry-run

# Real drafts via the OpenAI API
export OPENAI_API_KEY=<redacted>
python pipeline.py
```

Drafts land in `output/<date>-<topic-slug>/`.

## Notes

- This is a **demonstration**, not a finished product: no scheduling, no CMS publishing, no brand-voice fine-tuning.
- In production this would run on a schedule (cron / n8n) and push drafts to a CMS or a review queue instead of local files.
- AI drafts always need a human review pass before publishing.

## Tech

Python · OpenAI API · JSON topics file · Markdown output
