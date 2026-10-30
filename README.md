# DuckDuckGo Search API

[![ci](https://github.com/quantumproxies/duckduckgo-search-api/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/duckduckgo-search-api/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

DuckDuckGo web results as structured JSON, from Python or the command line: rank, title, link, snippet and source of every organic result, plus the knowledge panel and featured snippet when DuckDuckGo shows them. It works as the web search step of an LLM agent or a RAG pipeline. The code is free and open source (MIT). It runs on the QuanticData Data API: no proxies, no HTML to parse, sign in once and run a query.

```bash
pip install git+https://github.com/quantumproxies/duckduckgo-search-api
duckduckgo-search login
duckduckgo-search search "retrieval augmented generation" --country us -o results.json
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=duckduckgo-search-api).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `duckduckgo-search search` | query | Rank, title, link, snippet, source, 7 fields per row ([docs and price](https://quanticdata.io/serp-api/?utm_source=github&utm_medium=readme&utm_campaign=duckduckgo-search-api)) | one results page per call |

Any region: `--country us --lang en`, `--country de --lang de`, `--country fr --lang fr`. The pair becomes DuckDuckGo's region code (`us-en`), shown in `search_metadata.search_url`.

## Sample output

A real row from `duckduckgo-search search "retrieval augmented generation" --country us --lang en` (2026-10-23):

```json
{
  "rank": 1,
  "title": "Retrieval-augmented generation - Wikipedia",
  "link": "https://en.wikipedia.org/wiki/Retrieval-augmented_generation",
  "display_link": "en.wikipedia.org/wiki/Retrieval-augmented_generation",
  "source": "en.wikipedia.org",
  "description": "Retrieval-augmented generation (RAG) is a technique that enables large language models (LLMs) to retrieve and incorporate new information from external data sources. [1][2] With RAG, LLMs first refer to a specified set of documents, then respond to user queries.",
  "snippet_highlighted_words": [
    "Retrieval-augmented",
    "generation"
  ]
}
```

That is one entry of `organic`. With `-o results.json` you get the whole response, which also carries `search_metadata`, `search_parameters`, `knowledge`, `featured_snippet`, `pagination`.

## Python

```python
from quanticdata_duckduckgo_search_api import DuckDuckGoSearch

ddg = DuckDuckGoSearch()  # saved login, or QUANTICDATA_API_KEY

results = ddg.search("retrieval augmented generation", country="us", lang="en")
for r in results:
    print(r["rank"], r["source"], r["title"])

panel = results.meta.get("knowledge") or {}
print(panel.get("description"))
results.to_csv("rag_results.csv")
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Web search tool for an LLM**: A function that returns the top DuckDuckGo results as compact Markdown with numbered sources, ready to paste into a prompt or to register as a tool in an agent framework. See [`examples/llm_search_tool.py`](examples/llm_search_tool.py).
- **Source list for a RAG index**: Run a list of questions and keep every result link with the question that found it, de-duplicated by URL, as the seed list for a crawl. See [`examples/collect_sources.py`](examples/collect_sources.py).
- **Domain visibility check**: See where a domain appears in DuckDuckGo for a list of keywords and append the positions to a CSV on every run. See [`examples/rank_check.py`](examples/rank_check.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). With `-o results.json` you get the whole API response; the table, CSV and JSONL views hold its main list.

### `duckduckgo-search search`

DuckDuckGo web results for a query: rank, title, link, snippet and source of each organic result, plus the knowledge panel and featured snippet when DuckDuckGo shows them.

```
duckduckgo-search search QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | What to search, e.g. "retrieval augmented generation". |
| `--country` | string |  | Region to search, as an ISO country code (us, gb, de...); with --lang it becomes DuckDuckGo's region code, e.g. us-en. |
| `--lang` | string |  | Language of the region, e.g. en, de, fr. |

Sent with every call: `engine=duckduckgo`, `search_type=search`.

## Output fields

<details><summary><code>duckduckgo-search search</code>: 7 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | Position on the results page, 1-based. |
| `title` | string | Result title. |
| `link` | string | Target URL. |
| `display_link` | string | URL line shown under the title. |
| `source` | string | Host of the result. |
| `description` | string | Snippet shown under the title. |
| `snippet_highlighted_words` | array | Words DuckDuckGo highlights in the snippet, when it highlights any. |

</details>

## Sign-in and API keys

- `duckduckgo-search login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `duckduckgo-search login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `duckduckgo-search login --api-key`.
- `duckduckgo-search logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Searches are billed to your QuanticData account per call, at the price shown on the SERP API page linked above; $2 of usage is free every month and failed calls are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=duckduckgo-search-api).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/serp \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"engine": "duckduckgo", "search_type": "search", "query": "retrieval augmented generation", "country": "us", "lang": "en"}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=duckduckgo-search-api) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=duckduckgo-search-api) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this DuckDuckGo search API free?**

The code is free and MIT-licensed. Searches run on your QuanticData account: $2 of usage is free every month with no card, then you pay per search at the price on the SERP API page. Failed calls are never billed.

**Is this an official DuckDuckGo API?**

No. It reads DuckDuckGo's public results page through the QuanticData Data API and returns it as structured JSON.

**Do I need an API key or proxies?**

Only your QuanticData login or API key. There is no DuckDuckGo key to request and no proxy to configure: you send a query and get the parsed results back.

**Can I use it as a web search tool for an LLM?**

Yes. examples/llm_search_tool.py turns the results into numbered Markdown sources; wrap that function as a tool in LangChain, LlamaIndex or your own agent loop. For Claude, Cursor and other MCP clients, the MCP server linked above gives the same search as a tool.

**Which regions and languages?**

Any: --country and --lang set the DuckDuckGo region, e.g. --country de --lang de.

**Can I export to CSV?**

Add -o results.csv for the organic results; -o results.json keeps the whole response with the knowledge panel and featured snippet.

## Related scrapers

- [Bing Search API](https://github.com/quantumproxies/bing-search-api): Bing Search API alternative for Python and the command line.
- [Google SERP API](https://github.com/quantumproxies/google-serp-api): Google SERP API for Python and the command line.
- [Web Scraper API](https://github.com/quantumproxies/web-scraper-api): Web scraper API for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=duckduckgo-search-api).
