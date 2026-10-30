"""A DuckDuckGo web search tool for an LLM: results as numbered Markdown sources.

    python llm_search_tool.py "what is retrieval augmented generation" --top 5

web_search() returns the knowledge panel (when DuckDuckGo shows one) and the
top results as compact Markdown, each with a number, title, URL and snippet,
so a model can cite "[2]" in its answer. Import it in your own code and pass
the text to the model, or register the function as a tool in your agent
framework; run this file to see what the model would get.
"""

import argparse

from quanticdata_duckduckgo_search_api import DuckDuckGoSearch

_ddg = None


def web_search(query: str, top: int = 5, country: str = "us", lang: str = "en") -> str:
    """Search DuckDuckGo and return the results as numbered Markdown sources."""
    global _ddg
    _ddg = _ddg or DuckDuckGoSearch()
    run = _ddg.search(query, country=country, lang=lang)
    lines = [f"Web results for: {query}", ""]
    panel = run.meta.get("knowledge") or {}
    if panel.get("description"):
        lines += [f"Summary ({panel.get('title') or 'knowledge panel'}): {panel['description']}", ""]
    for i, r in enumerate(list(run)[:top], 1):
        lines.append(f"[{i}] {r.get('title')}")
        lines.append(f"    {r.get('link')}")
        if r.get("description"):
            lines.append(f"    {r['description']}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("query")
    parser.add_argument("--top", type=int, default=5, help="how many results to include")
    parser.add_argument("--country", default="us")
    parser.add_argument("--lang", default="en")
    args = parser.parse_args()
    print(web_search(args.query, top=args.top, country=args.country, lang=args.lang))


if __name__ == "__main__":
    main()
