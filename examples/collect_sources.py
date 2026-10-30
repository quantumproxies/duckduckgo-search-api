"""Collect the DuckDuckGo result links of a list of questions, for a RAG index.

    python collect_sources.py @questions.txt --country us --out sources.csv

Searches every question (given on the command line or as @file.txt, one per
line), keeps each result link once with the first question that found it, its
rank, title, host and snippet, and writes sources.csv: the seed list to crawl
or scrape into your index.
"""

import argparse

from quanticdata_duckduckgo_search_api import DuckDuckGoSearch, write


def read_args(values):
    items = []
    for v in values:
        if v.startswith("@"):
            with open(v[1:], encoding="utf-8") as fh:
                items.extend(line.strip() for line in fh if line.strip() and not line.startswith("#"))
        else:
            items.append(v)
    return items


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("questions", nargs="+", help="questions, or @file.txt with one per line")
    parser.add_argument("--country", default="us")
    parser.add_argument("--lang", default="en")
    parser.add_argument("--out", default="sources.csv")
    args = parser.parse_args()

    ddg = DuckDuckGoSearch()
    rows, seen = [], set()
    for question in read_args(args.questions):
        run = ddg.search(question, country=args.country, lang=args.lang)
        fresh = 0
        for r in run:
            link = r.get("link")
            if not link or link in seen:
                continue
            seen.add(link)
            fresh += 1
            rows.append({"question": question, "rank": r.get("rank"), "title": r.get("title"),
                         "link": link, "source": r.get("source"), "snippet": r.get("description")})
        print(f"{question!r}: {len(run)} results, {fresh} new links")

    write(rows, args.out)
    print(f"{len(rows)} unique links written to {args.out}")


if __name__ == "__main__":
    main()
