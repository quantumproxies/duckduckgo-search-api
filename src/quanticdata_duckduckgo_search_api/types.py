"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class SearchRow(TypedDict, total=False):
    """One row of `duckduckgo-search search` (POST /v1/serp)."""

    rank: int
    """Position on the results page, 1-based."""
    title: str
    """Result title."""
    link: str
    """Target URL."""
    display_link: str
    """URL line shown under the title."""
    source: str
    """Host of the result."""
    description: str
    """Snippet shown under the title."""
    snippet_highlighted_words: List[Any]
    """Words DuckDuckGo highlights in the snippet, when it highlights any."""
