#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_doi.py：用 Crossref 公開 API 逐筆核對 DOI。

沒有 Python 時，到 https://doi.org/ 逐筆貼上 DOI 核對。

用法：
    python verify_doi.py dois.txt            # dois.txt 一行一個 DOI
    python verify_doi.py dois.txt --mailto 你的信箱 > result.csv

輸出 CSV 欄位：doi, found, title, first_author, year, container, update_flags
  found=yes 表示 Crossref 有這筆；found=no 時其他欄位一律留空，不猜補。
  update_flags 為 Crossref 記錄的更正、撤稿等更新類型（例如 retraction），多個以分號分隔。
  沒有標記不等於沒問題，只代表 Crossref 目前沒有記錄。

只使用 Python 標準函式庫。--mailto 為選填，程式內不含任何信箱。
"""
import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.crossref.org/works/"
FIELDS = ["doi", "found", "title", "first_author", "year", "container", "update_flags"]


def first(lst):
    return lst[0] if isinstance(lst, list) and lst else ""


def lookup(doi, mailto):
    ua = "ntc-academic-kit-verify-doi/1.0"
    if mailto:
        ua += " (mailto:%s)" % mailto
    url = API + urllib.parse.quote(doi, safe="")
    if mailto:
        url += "?mailto=" + urllib.parse.quote(mailto)
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            msg = json.loads(resp.read().decode("utf-8"))["message"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"doi": doi, "found": "no"}
        raise
    author = ""
    authors = msg.get("author") or []
    if authors:
        a = authors[0]
        author = (a.get("family") or a.get("name") or "").strip()
    year = ""
    for key in ("issued", "published-print", "published-online", "created"):
        parts = (msg.get(key) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            year = str(parts[0][0])
            break
    flags = []
    for u in msg.get("update-to") or []:
        if u.get("type"):
            flags.append(str(u["type"]))
    for u in msg.get("updated-by") or []:
        if u.get("type"):
            flags.append(str(u["type"]))
    for r in (msg.get("relation") or {}).get("is-retracted-by", []) or []:
        flags.append("retraction")
    return {
        "doi": doi,
        "found": "yes",
        "title": first(msg.get("title")),
        "first_author": author,
        "year": year,
        "container": first(msg.get("container-title")),
        "update_flags": ";".join(sorted(set(flags))),
    }


def clean(line):
    d = line.strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "doi:", "DOI:"):
        if d.startswith(prefix):
            d = d[len(prefix):]
    return d.strip()


def main():
    ap = argparse.ArgumentParser(description="用 Crossref 核對 DOI 清單")
    ap.add_argument("infile", help="DOI 清單檔，一行一個")
    ap.add_argument("--mailto", default="", help="選填：你的聯絡信箱（Crossref 禮貌池）")
    ap.add_argument("--delay", type=float, default=1.0, help="每筆之間的等待秒數，預設 1")
    args = ap.parse_args()

    with open(args.infile, encoding="utf-8-sig") as f:
        dois = [clean(x) for x in f if clean(x)]

    out = csv.DictWriter(sys.stdout, fieldnames=FIELDS, lineterminator="\n")
    out.writeheader()
    for i, doi in enumerate(dois):
        try:
            row = lookup(doi, args.mailto)
        except Exception as e:  # 網路錯誤等：不猜，標示查詢失敗
            sys.stderr.write("查詢失敗 %s：%s\n" % (doi, e))
            row = {"doi": doi, "found": "error"}
        out.writerow({k: row.get(k, "") for k in FIELDS})
        if i < len(dois) - 1:
            time.sleep(args.delay)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
