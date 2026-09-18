# ai-content-automation-pipeline

> **Sample / demo build.** This is a small learning project that turns a list of topics into first drafts: one blog outline, one product description, and three social posts per topic. It runs in dry run mode with no API key, or calls the OpenAI API for real drafts. Not production code.

## What it shows

* You give it a topics file, it gives you back a folder of drafts, one folder per topic.
* Two modes: dry run writes template drafts with no API key, full mode calls the OpenAI API.
* Output stays tidy. Every topic gets its own dated folder with `blog.md`, `product.md`, and `social.md`.

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
export OPENAI_API_KEY=your_key_here
python pipeline.py
```

Drafts land in `output/<date>-<topic-slug>/`.

## Notes

* This is a **demonstration**, not a finished product. There is no scheduling, no CMS publishing, and no brand voice tuning.
* In production this would run on a schedule (cron or n8n) and push drafts to a CMS or a review queue instead of local files.
* AI drafts always need a human review before publishing. Treat everything in `output/` as a starting point, not final copy.
* Keep your API key in an environment variable or secret manager, never in the repo.

## Tech

Python · OpenAI API · JSON topics file · Markdown output
