#!/usr/bin/env python3
"""Create a new public slide deck from the shared viewer."""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("使い方: python3 scripts/new_deck.py <英数字のslug> <タイトル>")
    slug, title = sys.argv[1:]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise SystemExit("slugは小文字英数字とハイフンのみ使用できます")
    folder = ROOT / "slides" / slug
    if folder.exists():
        raise SystemExit(f"すでに存在します: {folder}")
    folder.mkdir(parents=True)
    shutil.copy(ROOT / "slides" / "welcome" / "index.html", folder / "index.html")
    deck = {
        "title": title,
        "slides": [
            {"label": "結論", "title": title, "body": "ここに一番大事な結論を書きます。", "kind": "cover", "visual": "◉"},
            {"label": "全体像", "title": "何が起きたか", "body": "ここに全体像を短く書きます。", "kind": "steps", "items": ["確認", "実施", "結果"]},
            {"label": "確認ポイント", "title": "大事な点", "body": "ここに数字や判断材料を書きます。", "kind": "number", "visual": "01"},
            {"label": "次の行動", "title": "次にすること", "body": "ここに次の行動と根拠へのリンク先を書きます。", "kind": "closing", "visual": "✓"},
        ],
    }
    (folder / "deck.json").write_text(json.dumps(deck, ensure_ascii=False, indent=2) + "\n")
    catalog_path = ROOT / "catalog.json"
    catalog = json.loads(catalog_path.read_text())
    catalog.insert(0, {"slug": slug, "title": title, "description": "結果資料 · 4枚"})
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    print(f"作成しました: slides/{slug}/")


if __name__ == "__main__":
    main()
