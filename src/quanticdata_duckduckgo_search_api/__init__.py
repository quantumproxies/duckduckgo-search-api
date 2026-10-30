"""DuckDuckGo Search API: DuckDuckGo search API for Python and the command line: DuckDuckGo web results with rank, title, link, snippet and source, plus the knowledge panel when DuckDuckGo shows one, as JSON or CSV. A web search step for LLM agents and RAG pipelines. Free and open source; no DuckDuckGo key or proxies needed.

    from quanticdata_duckduckgo_search_api import DuckDuckGoSearch

    scraper = DuckDuckGoSearch()   # saved login (`duckduckgo-search login`) or QUANTICDATA_API_KEY
    run = scraper.search(...)   # DuckDuckGo web results for a query
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["DuckDuckGoSearch", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class DuckDuckGoSearch:
    """DuckDuckGo Search API on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="duckduckgo-search/0.1.0 (+https://github.com/quantumproxies/duckduckgo-search-api)", timeout=timeout)

    def search(
        self, query: str,
        *,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        timeout: float = 1800.0,
    ) -> Run:
        """DuckDuckGo web results for a query: rank, title, link, snippet and source of each organic result, plus the knowledge panel and featured snippet when DuckDuckGo shows them.

        Args:
            query: What to search, e.g. "retrieval augmented generation".
            country: Region to search, as an ISO country code (us, gb, de...); with --lang it becomes DuckDuckGo's region code, e.g. us-en.
            lang: Language of the region, e.g. en, de, fr.
            timeout: seconds to wait before giving up.

        Returns a Run: ``meta`` is the whole response, ``rows`` its ``organic`` list (see ``types.SearchRow``).
        """
        payload = {
            "query": query,
            "country": country,
            "lang": lang,
        }
        return self.client.layer("serp", {**{'engine': 'duckduckgo', 'search_type': 'search'}, **payload}, rows_key='organic', row_field='value', timeout=timeout)
