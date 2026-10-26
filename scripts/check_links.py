#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Muad Mohamed Mohamud and contributors
"""Validate the registry CSV files and, optionally, check that their URLs respond.

Usage:
    python scripts/check_links.py                 # validate structure only (no network)
    python scripts/check_links.py --check-urls    # also request every URL
    python scripts/check_links.py --check-urls --report link-report.md

Validation covers: UTF-8 encoding, exact headers, row width, required fields,
controlled vocabularies, ID format and uniqueness, duplicate names, dates, URL
syntax, README documentation of every column, the README category counts, and
relative links in the Markdown files.

URL checks are read-only and never edit data. A failed request is NOT evidence
that a resource does not exist: many sites block automated clients, require a
log-in, or are temporarily down. Treat every non-OK result as a prompt to check
the page by hand.

Exit status: 1 if validation fails; with --strict, also 1 if any URL is not OK.
Only the Python standard library is used.
"""
import argparse
import concurrent.futures
import csv
import re
import socket
import ssl
import sys
import urllib.error
import urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
USER_AGENT = "somali-ai-nlp-registry-link-check/1.0 (+https://github.com/moadjini/somali-ai-nlp-registry)"

# Placeholders allowed instead of a URL. They describe the evidence, not a guess.
URL_PLACEHOLDERS = {"Not released", "Not reported", "Not reviewed", "Not applicable", "Not verified"}

SCHEMAS = {
    "somali_resources": {
        "columns": [
            "id", "resource_name", "category", "task", "artifact_type", "creator", "year", "language_variety",
            "reported_size", "reported_results", "annotation", "source_url", "resource_url", "additional_urls",
            "evidence_type", "access_status", "access_detail", "license_terms", "license_basis",
            "verification_level", "verification_note", "discovery_phase", "date_last_verified",
            "paper_citation", "notes",
        ],
        "optional": {"additional_urls", "notes"},
        "url_fields": ["source_url", "resource_url"],
        "url_list_fields": ["additional_urls"],
        "id_pattern": r"(T|L|G|E|S|P|M|C|D|R)\d+",
        "vocab": {
            "category": {
                "Text corpora", "Pretrained language models", "Lemmatization", "LLM evaluation",
                "Speech recognition", "Text-to-speech", "Machine translation",
                "Sentiment and text classification", "Dialect identification", "Information retrieval",
            },
            "access_status": {"Open", "On request or licensed", "Not released", "Not documented"},
            "license_basis": {"Stated by provider", "Stated in paper", "Provider metadata only",
                              "Not stated", "Not verified", "Not applicable"},
            "verification_level": {"Verified", "Partially verified", "Unverified"},
            "language_variety": {"Maxaa Tiri (Standard Somali)", "Maay", "Maxaa Tiri and Maay", "Not specified"},
            "discovery_phase": {"Main search", "Speech follow-up", "Somali-language pilot", "Final update",
                                "Contribution"},
        },
        # ID prefix must agree with the category.
        "prefix": {"T": "Text corpora", "L": "Pretrained language models", "G": "Lemmatization",
                   "E": "LLM evaluation", "S": "Speech recognition", "P": "Text-to-speech",
                   "M": "Machine translation", "C": "Sentiment and text classification",
                   "D": "Dialect identification", "R": "Information retrieval"},
        "date_field": "date_last_verified",
    },
    "multilingual_resources": {
        "columns": ["id", "resource_name", "task", "somali_component", "source_url", "resource_url",
                    "paper_citation", "date_last_verified", "notes"],
        "optional": {"notes"},
        "url_fields": ["source_url", "resource_url"],
        "url_list_fields": [],
        "id_pattern": r"X\d{2,}",
        "vocab": {},
        "prefix": {},
        "date_field": "date_last_verified",
    },
    "watchlist": {
        "columns": ["id", "resource_name", "type", "source_url", "reason_not_counted", "last_checked", "notes"],
        "optional": {"notes"},
        "url_fields": ["source_url"],
        "url_list_fields": [],
        "id_pattern": r"W\d{2,}",
        "vocab": {},
        "prefix": {},
        "date_field": "last_checked",
    },
}


def latest(kind, data_dir):
    """Return the most recent dated file for a dataset kind, e.g. data/watchlist_2026-10-26.csv."""
    files = sorted(data_dir.glob(f"{kind}_????-??-??.csv"))
    return files[-1] if files else None


def display(path):
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def is_url(value):
    return re.fullmatch(r"https?://[^\s]+\.[^\s]+", value) is not None


def split_list(value):
    return [v.strip() for v in value.split(";") if v.strip()]


def validate_csv(kind, path, errors):
    """Validate one CSV file. Returns its rows (as dicts) so later checks can use them."""
    schema = SCHEMAS[kind]
    where = display(path)
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        errors.append(f"{where}: starts with a byte-order mark; save as UTF-8 without BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"{where}: not valid UTF-8 ({exc})")
        return []
    reader = csv.reader(text.lstrip("﻿").splitlines())
    header = next(reader, None)
    if header != schema["columns"]:
        errors.append(f"{where}: header does not match the documented columns.\n"
                      f"    expected: {schema['columns']}\n    found:    {header}")
        return []
    rows, ids, names = [], {}, {}
    for line_no, cells in enumerate(reader, start=2):
        if not any(c.strip() for c in cells):
            errors.append(f"{where}:{line_no}: empty row")
            continue
        if len(cells) != len(header):
            errors.append(f"{where}:{line_no}: {len(cells)} fields, expected {len(header)} (check quoting)")
            continue
        row = dict(zip(header, cells))
        rid = row["id"]
        tag = f"{where}:{line_no} ({rid or 'no id'})"
        for col in header:
            value = row[col]
            if value != value.strip():
                errors.append(f"{tag}: '{col}' has leading or trailing spaces")
            if col not in schema["optional"] and not value.strip():
                errors.append(f"{tag}: required field '{col}' is empty (use 'Not reported' or 'Not applicable')")
        if not re.fullmatch(schema["id_pattern"], rid):
            errors.append(f"{tag}: id does not match pattern {schema['id_pattern']}")
        if rid in ids:
            errors.append(f"{tag}: duplicate id (also on line {ids[rid]})")
        ids[rid] = line_no
        name_key = re.sub(r"\W+", " ", row["resource_name"].lower()).strip()
        if name_key in names:
            errors.append(f"{tag}: duplicate resource_name (also {names[name_key]})")
        names[name_key] = rid
        for col, allowed in schema["vocab"].items():
            if row[col] not in allowed:
                errors.append(f"{tag}: {col} '{row[col]}' is not one of {sorted(allowed)}")
        if schema["prefix"] and rid[:1] in schema["prefix"] and schema["prefix"][rid[:1]] != row.get("category"):
            errors.append(f"{tag}: id prefix '{rid[:1]}' requires category '{schema['prefix'][rid[:1]]}'")
        when = row[schema["date_field"]]
        try:
            # One day of leeway: dates are recorded in the checker's local time, CI runs in UTC.
            if date.fromisoformat(when) > date.today() + timedelta(days=1):
                errors.append(f"{tag}: {schema['date_field']} {when} is in the future")
        except ValueError:
            errors.append(f"{tag}: {schema['date_field']} must be YYYY-MM-DD, found '{when}'")
        for col in schema["url_fields"]:
            value = row[col]
            if value not in URL_PLACEHOLDERS and not is_url(value):
                errors.append(f"{tag}: {col} must be an http(s) URL or one of {sorted(URL_PLACEHOLDERS)}")
        for col in schema["url_list_fields"]:
            for value in split_list(row[col]):
                if not is_url(value):
                    errors.append(f"{tag}: {col} item '{value}' is not an http(s) URL (separate items with ';')")
        rows.append(row)
    if not rows:
        errors.append(f"{where}: no data rows")
    return rows


def check_readme(columns_by_kind, resource_rows, errors):
    """Every CSV column must be documented in README.md, and the category counts must match."""
    readme_path = ROOT / "README.md"
    if not readme_path.exists():
        errors.append("README.md is missing")
        return
    readme = readme_path.read_text(encoding="utf-8")
    for kind, columns in columns_by_kind.items():
        for col in columns:
            if f"`{col}`" not in readme:
                errors.append(f"README.md does not document column `{col}` of {kind}")
    block = re.search(r"<!-- category-counts:start -->(.*?)<!-- category-counts:end -->", readme, re.S)
    if not block:
        errors.append("README.md: category-counts block not found")
        return
    # Table: | Category | Resources | <one column per access_status> |
    table = [[c.strip() for c in line.strip().strip("|").split("|")]
             for line in block.group(1).strip().splitlines() if line.strip().startswith("|")]
    header, body = table[0], [r for r in table[2:]]
    statuses = header[2:]
    unknown = set(statuses) - SCHEMAS["somali_resources"]["vocab"]["access_status"]
    if unknown:
        errors.append(f"README.md: count table has unknown access columns {sorted(unknown)}")
    actual = {}
    for row in resource_rows:
        for key in (row["category"], "Total"):
            counts = actual.setdefault(key, {"Resources": 0, **{s: 0 for s in statuses}})
            counts["Resources"] += 1
            if row["access_status"] in counts:
                counts[row["access_status"]] += 1
    documented = {}
    for cells in body:
        try:
            documented[cells[0]] = dict(zip(header[1:], (int(c) for c in cells[1:])))
        except ValueError:
            errors.append(f"README.md: non-numeric count in row '{cells[0]}'")
    for cat, counts in actual.items():
        if documented.get(cat) != counts:
            errors.append(f"README.md: counts for '{cat}' are {documented.get(cat)}, the CSV gives {counts}")
    for cat in documented:
        if cat not in actual:
            errors.append(f"README.md: category '{cat}' has no rows in the CSV")


def check_local_links(errors):
    """Relative links in Markdown files must point to files that exist."""
    for md in sorted(ROOT.rglob("*.md")):
        if ".git" in md.parts:
            continue
        text = md.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)\s]+)\)", text):
            if re.match(r"[a-z]+:", target) or target.startswith("#"):
                continue
            path = target.split("#", 1)[0]
            if path and not (md.parent / path).resolve().exists():
                errors.append(f"{md.relative_to(ROOT).as_posix()}: link target '{target}' does not exist")


# ---------------------------------------------------------------------------
# URL checking
# ---------------------------------------------------------------------------
NOTES = {
    "ok": "responded",
    "redirected": "responded after a redirect; consider updating the URL",
    "restricted": "access restricted or automated requests refused; check in a browser",
    "not_found": "not found at this address; the resource may have moved, check by hand",
    "server_error": "server error; try again later",
    "http_error": "unexpected HTTP status; check by hand",
    "timeout": "no response before the timeout; try again later",
    "unreachable": "could not connect (DNS or connection error); check by hand",
    "ssl_error": "TLS/SSL problem; check in a browser",
}


def classify(code):
    if 200 <= code < 300:
        return "ok"
    if code in (401, 402, 403, 407, 429, 451):
        return "restricted"
    if code in (404, 410):
        return "not_found"
    if code >= 500:
        return "server_error"
    return "http_error"


def request(url, method, timeout):
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # follows redirects
        if method == "GET":
            resp.read(2048)
        return resp.status, resp.geturl()


def check_url(url, timeout):
    """Return (status, http_code_or_None, final_url, detail). HEAD first, then GET."""
    last = ("unreachable", None, url, "")
    for method in ("HEAD", "GET"):
        try:
            code, final = request(url, method, timeout)
            status = classify(code)
            if status == "ok" and final.rstrip("/") != url.rstrip("/"):
                status = "redirected"
            return status, code, final, ""
        except urllib.error.HTTPError as exc:
            last = (classify(exc.code), exc.code, url, exc.reason if isinstance(exc.reason, str) else "")
            if method == "HEAD":
                continue  # many servers reject HEAD; retry with GET
            return last
        except (socket.timeout, TimeoutError):
            last = ("timeout", None, url, f"{timeout}s")
        except ssl.SSLError as exc:
            last = ("ssl_error", None, url, str(exc)[:80])
        except urllib.error.URLError as exc:
            reason = exc.reason
            if isinstance(reason, (socket.timeout, TimeoutError)):
                last = ("timeout", None, url, f"{timeout}s")
            elif isinstance(reason, ssl.SSLError):
                last = ("ssl_error", None, url, str(reason)[:80])
            else:
                last = ("unreachable", None, url, str(reason)[:80])
        except (ConnectionError, OSError) as exc:
            last = ("unreachable", None, url, str(exc)[:80])
    return last


def collect_urls(datasets):
    urls = {}
    for kind, rows in datasets.items():
        schema = SCHEMAS[kind]
        for row in rows:
            values = [row[c] for c in schema["url_fields"]]
            for c in schema["url_list_fields"]:
                values += split_list(row[c])
            for value in values:
                if is_url(value):
                    urls.setdefault(value, []).append(row["id"])
    return urls


def run_url_checks(datasets, timeout, workers, report_path):
    urls = collect_urls(datasets)
    print(f"\nChecking {len(urls)} unique URLs (timeout {timeout}s, {workers} workers)...")
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(check_url, url, timeout): url for url in urls}
        for fut in concurrent.futures.as_completed(futures):
            results[futures[fut]] = fut.result()
    order = list(NOTES)
    lines = []
    for url in sorted(urls, key=lambda u: (order.index(results[u][0]), u)):
        status, code, final, detail = results[url]
        ids = ", ".join(sorted(set(urls[url])))
        extra = f" -> {final}" if status == "redirected" else (f" ({detail})" if detail else "")
        lines.append((status, code, url, ids, extra))
        print(f"  {status:<12} {code or '-':>4}  {url}  [{ids}]{extra}")
    counts = {s: sum(1 for r in results.values() if r[0] == s) for s in order}
    print("\nSummary: " + ", ".join(f"{n} {s}" for s, n in counts.items() if n))
    print("A non-OK result does not show that a resource is gone; open the page by hand before changing data.")
    if report_path:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# Link check report ({date.today().isoformat()})\n\n")
            f.write("Automated, read-only check. A non-OK result does not show that a resource no longer exists.\n\n")
            f.write("| Status | HTTP | URL | Used by | Note |\n|---|---|---|---|---|\n")
            for status, code, url, ids, extra in lines:
                f.write(f"| {status} | {code or '-'} | {url} | {ids} | {NOTES[status]}{extra} |\n")
        print(f"Report written to {report_path}")
    return counts


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check-urls", action="store_true", help="request every URL (needs network access)")
    parser.add_argument("--timeout", type=float, default=20, help="seconds per request (default 20)")
    parser.add_argument("--workers", type=int, default=6, help="parallel requests (default 6)")
    parser.add_argument("--report", help="write a Markdown report of the URL check to this file")
    parser.add_argument("--strict", action="store_true", help="exit with status 1 if any URL is not OK")
    parser.add_argument("--data-dir", default=str(DATA), help="directory with the dated CSV files")
    args = parser.parse_args()

    data_dir = Path(args.data_dir).resolve()
    errors, datasets = [], {}
    for kind in SCHEMAS:
        path = latest(kind, data_dir)
        if path is None:
            errors.append(f"no file matching {kind}_YYYY-MM-DD.csv in {data_dir}")
            continue
        datasets[kind] = validate_csv(kind, path, errors)
        print(f"{display(path)}: {len(datasets[kind])} rows")

    resource_ids = {r["id"] for r in datasets.get("somali_resources", [])}
    for kind in ("multilingual_resources", "watchlist"):
        for row in datasets.get(kind, []):
            if row["id"] in resource_ids:
                errors.append(f"{kind}: id {row['id']} also used in somali_resources")
    if datasets.get("somali_resources"):
        check_readme({k: SCHEMAS[k]["columns"] for k in datasets}, datasets["somali_resources"], errors)
    check_local_links(errors)

    if errors:
        print(f"\nValidation FAILED with {len(errors)} problem(s):")
        for e in errors:
            print(" -", e)
    else:
        print("\nValidation OK")

    url_problems = 0
    if args.check_urls and datasets:
        counts = run_url_checks(datasets, args.timeout, args.workers, args.report)
        url_problems = sum(n for s, n in counts.items() if s not in ("ok", "redirected"))
    return 1 if errors or (args.strict and url_problems) else 0


if __name__ == "__main__":
    sys.exit(main())
