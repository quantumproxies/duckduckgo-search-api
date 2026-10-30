"""Where does a domain rank on DuckDuckGo for a list of keywords?

    python rank_check.py wikipedia.org "retrieval augmented generation" "vector database" --country us

Searches each keyword, finds the first result whose host is the domain (or one
of its subdomains) and appends date, keyword, position, title and URL to
ddg_positions.csv. An empty position means the domain is not on the results
page. Run it from cron to follow the positions over time.
"""

import argparse
import csv
import os
from datetime import datetime, timezone

from quanticdata_duckduckgo_search_api import DuckDuckGoSearch

FIELDS = ["checked_at", "keyword", "domain", "position", "title", "link"]


def matches(host: str, domain: str) -> bool:
    host = (host or "").lower().removeprefix("www.")
    domain = domain.lower().removeprefix("www.")
    return host == domain or host.endswith("." + domain)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("domain", help="e.g. wikipedia.org")
    parser.add_argument("keywords", nargs="+")
    parser.add_argument("--country", default="us")
    parser.add_argument("--lang", default="en")
    parser.add_argument("--out", default="ddg_positions.csv")
    args = parser.parse_args()

    ddg = DuckDuckGoSearch()
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    new_file = not os.path.exists(args.out)
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        for keyword in args.keywords:
            run = ddg.search(keyword, country=args.country, lang=args.lang)
            hit = next((r for r in run if matches(r.get("source"), args.domain)), None)
            writer.writerow({"checked_at": checked_at, "keyword": keyword, "domain": args.domain,
                             "position": hit.get("rank") if hit else "", "title": hit.get("title") if hit else "",
                             "link": hit.get("link") if hit else ""})
            print(f"{keyword!r}: {hit['rank'] if hit else '-'}")
    print(f"{len(args.keywords)} positions appended to {args.out}")


if __name__ == "__main__":
    main()
