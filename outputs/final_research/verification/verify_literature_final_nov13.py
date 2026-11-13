"""Independent read-only PDF locator/extractor. Does not save or republish PDF text.

Run: python verify_literature_final_nov13.py gao --pages 1 12 13
     python verify_literature_final_nov13.py zhang --find 2017 121
PDF page numbers are one-based, including the cover. Set --downloads as needed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from pypdf import PdfReader

FILES = {
    "gao": "ssrn-5373282.pdf",
    "gao_duplicate": "ssrn-5373282 (1).pdf",
    "zhang": "ssrn-6210408.pdf",
    "liu": "ssrn-7042518.pdf",
    "he": "1-s2.0-S0048733325001404-main.pdf",
    "chen": "1-s2.0-S0304387825001506-main.pdf",
    "kang": "1-s2.0-S026156062400216X-main.pdf",
    "shen": "1-s2.0-S1057521924004423-main.pdf",
}

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("paper", choices=[*FILES, "all"])
    ap.add_argument("--downloads", type=Path, default=Path.home() / "Downloads")
    ap.add_argument("--pages", nargs="*", type=int, default=[])
    ap.add_argument("--find", nargs="*", default=[])
    a = ap.parse_args()
    keys = list(FILES) if a.paper == "all" else [a.paper]
    for key in keys:
        path = a.downloads / FILES[key]
        reader = PdfReader(path)
        print(json.dumps({"paper": key, "file": path.name, "sha256": sha256(path),
                          "pdf_pages": len(reader.pages)}, ensure_ascii=False))
        if a.find:
            for i, page in enumerate(reader.pages, 1):
                text = page.extract_text() or ""
                hits = [s for s in a.find if s.casefold() in text.casefold()]
                if hits:
                    print(json.dumps({"pdf_page": i, "search_hits": hits}, ensure_ascii=False))
        for number in a.pages:
            text = reader.pages[number-1].extract_text() or ""
            print(f"\n--- {path.name}: PDF page {number} ---\n{text}")

if __name__ == "__main__":
    main()
