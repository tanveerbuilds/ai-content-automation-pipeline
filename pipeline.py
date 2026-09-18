#!/usr/bin/env python3
"""
Sample AI content pipeline (demonstration only).

Reads topics from topics.json and drafts, for each topic:
  - a blog post outline + opening paragraphs (blog.md)
  - a concise product description (product.md)
  - three short social media posts (social.md)

Runs in --dry-run mode by default (template-based, no API key needed).
With OPENAI_API_KEY set, it calls the OpenAI API instead.

Usage:
    python pipeline.py --dry-run
    python pipeline.py            # requires OPENAI_API_KEY
"""
import argparse
import json
import os
import re
from datetime import date
from pathlib import Path

TOPICS_FILE = Path(__file__).parent / "topics.json"
OUTPUT_DIR = Path(__file__).parent / "output"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def dry_run_draft(topic):
    t = topic["topic"]
    audience = topic["audience"]
    tone = topic.get("tone", "friendly")
    return {
        "blog.md": (
            f"# {t}\n\n_Audience: {audience} · Tone: {tone}_\n\n"
            "## Outline\n\n"
            "1. The problem the reader runs into\n"
            "2. What changes when it's handled\n"
            "3. Three practical next steps\n\n"
            "## Opening (draft)\n\n"
            "[dry-run placeholder: set OPENAI_API_KEY for a real draft]\n"
        ),
        "product.md": (
            f"## {t}\n\nBuilt for {audience}.\n\n"
            "[dry-run placeholder: set OPENAI_API_KEY for a real draft]\n"
        ),
        "social.md": (
            "[dry-run placeholder: set OPENAI_API_KEY for real posts]\n\n"
            f"1. A quick thought for {audience}...\n"
            "2. ...\n"
            "3. ...\n"
        ),
    }


def openai_draft(topic, client):
    t = topic["topic"]
    audience = topic["audience"]
    tone = topic.get("tone", "friendly")

    def complete(prompt):
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You write marketing content in a {tone} tone for {audience}. "
                        "Plain, human language. No hype, no cliches, no emojis."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()

    return {
        "blog.md": complete(
            f"Write a blog post outline plus the opening two paragraphs about: {t}"
        ),
        "product.md": complete(
            f"Write a concise product description (120 words max) for: {t}"
        ),
        "social.md": complete(
            f"Write three short social media posts (each under 240 characters) "
            f"about: {t}. Number them."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="template drafts, no API key needed")
    args = parser.parse_args()

    topics = json.loads(TOPICS_FILE.read_text(encoding="utf-8"))
    client = None
    if not args.dry_run:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("Set OPENAI_API_KEY or use --dry-run.")
            return
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

    today = date.today().isoformat()
    for topic in topics:
        folder = OUTPUT_DIR / f"{today}-{slugify(topic['topic'])}"
        folder.mkdir(parents=True, exist_ok=True)
        drafts = dry_run_draft(topic) if args.dry_run else openai_draft(topic, client)
        for filename, content in drafts.items():
            (folder / filename).write_text(content, encoding="utf-8")
        print(f"Wrote {len(drafts)} drafts to {folder}")


if __name__ == "__main__":
    main()
