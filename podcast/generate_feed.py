#!/usr/bin/env python3
"""Generate the Vault Radio RSS feed (podcast 2.0 with iTunes tags).

Reads episodes/*.mp3 from this directory, measures real duration with
ffprobe, and writes feed.xml here. This directory is served by GitHub
Pages, so the feed URL is:
  https://ultimatejordan.github.io/dead-media-vault/podcast/feed.xml
"""
import os
import glob
import json
import subprocess
from datetime import datetime, timezone
from xml.sax.saxutils import escape

BASE = os.path.dirname(os.path.abspath(__file__))
EPISODES_DIR = os.path.join(BASE, "episodes")
FEED_BASE_URL = "https://ultimatejordan.github.io/dead-media-vault/podcast"

SHOW = {
    "title": "Vault Radio",
    "description": (
        "The stories behind public-domain art. A deadpan archivist digs up "
        "the wild histories of the illustrations, maps, and manuscripts "
        "everyone forgot — Weird Tales cover artists, botanical explorers, "
        "and globes that say 'here be dragons.' All public domain, all free, "
        "all true. A Dead Media Vault production."
    ),
    "author": "Dead Media Vault",
    "email": "tacatshi@gmail.com",
    "category": "Arts",
    "category_sub": "Visual Arts",
}

# slug -> metadata (audio filename = slug + ".mp3")
EPISODE_META = {
    "ep001-here-be-dragons": {
        "title": "The Queen of the Pulps, the Butterfly Lady, and the Real Here Be Dragons",
        "description": (
            "Episode 1. Three stories from the archives: Margaret Brundage, "
            "the woman who painted Weird Tales' most scandalous covers under a "
            "man's initials; Maria Sibylla Merian, who sailed to Suriname at "
            "age 52 to chase butterflies and invented ecological illustration; "
            "and the Lenox Globe — the only historical map on Earth that "
            "actually says 'here be dragons.'"
        ),
        "pub_date": "2026-10-07",
        "season": 1,
        "episode": 1,
    },
}


def rfc2822(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")


def probe(mp3_path):
    """Return (duration_seconds, size_bytes) measured from the actual file."""
    size = os.path.getsize(mp3_path)
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "json", mp3_path],
            capture_output=True, text=True, timeout=30)
        dur = float(json.loads(out.stdout)["format"]["duration"])
    except Exception:
        dur = 0.0
    return int(dur), size


def fmt_duration(seconds):
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def main():
    items = []
    for slug, meta in sorted(EPISODE_META.items()):
        mp3 = os.path.join(EPISODES_DIR, slug + ".mp3")
        if not os.path.exists(mp3):
            print(f"SKIP {slug}: no MP3 yet")
            continue
        duration, size = probe(mp3)
        url = f"{FEED_BASE_URL}/episodes/{slug}.mp3"
        items.append(f"""    <item>
      <title>{escape(meta['title'])}</title>
      <description>{escape(meta['description'])}</description>
      <pubDate>{rfc2822(meta['pub_date'])}</pubDate>
      <enclosure url="{url}" length="{size}" type="audio/mpeg"/>
      <guid isPermaLink="false">vault-radio-{slug}</guid>
      <itunes:author>{escape(SHOW['author'])}</itunes:author>
      <itunes:summary>{escape(meta['description'])}</itunes:summary>
      <itunes:episodeType>full</itunes:episodeType>
      <itunes:season>{meta['season']}</itunes:season>
      <itunes:episode>{meta['episode']}</itunes:episode>
      <itunes:duration>{fmt_duration(duration)}</itunes:duration>
    </item>""")

    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:podcast="https://podcastindex.org/namespace/1.0">
  <channel>
    <title>{escape(SHOW['title'])}</title>
    <link>{FEED_BASE_URL}</link>
    <language>en-us</language>
    <description>{escape(SHOW['description'])}</description>
    <itunes:author>{escape(SHOW['author'])}</itunes:author>
    <itunes:summary>{escape(SHOW['description'])}</itunes:summary>
    <itunes:owner>
      <itunes:name>{escape(SHOW['author'])}</itunes:name>
      <itunes:email>{escape(SHOW['email'])}</itunes:email>
    </itunes:owner>
    <itunes:image href="{FEED_BASE_URL}/cover.jpg"/>
    <itunes:category text="{SHOW['category']}">
      <itunes:category text="{SHOW['category_sub']}"/>
    </itunes:category>
    <itunes:explicit>false</itunes:explicit>
    <lastBuildDate>{now}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""
    out = os.path.join(BASE, "feed.xml")
    with open(out, "w") as f:
        f.write(feed)
    print(f"Feed written: {out} ({len(items)} episodes)")


if __name__ == "__main__":
    main()
