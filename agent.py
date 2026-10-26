"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""
import json
import re

import config
from mcp_client import call_tool
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── query parsing ─────────────────────────────────────────────────────────────

NUMBER = r"(\d+(?:\.\d+)?)"

# Tried in order; the first that matches sets max_price.
PRICE_PATTERNS = [
    # A range takes its upper number: "between $20 and $50", "$20-$50", "$20 to $50"
    re.compile(rf"\bbetween\s*\$?\s*{NUMBER}\s*(?:and|to|-)\s*\$?\s*{NUMBER}(?:\s*dollars?)?", re.IGNORECASE),
    re.compile(rf"\$\s*{NUMBER}\s*(?:-|to)\s*\$?\s*{NUMBER}", re.IGNORECASE),
    # "under $30", "below 30", "less than $30", "max $30", "up to 30", "no more than $30"
    re.compile(rf"\b(?:under|below|less than|max|up to|no more than)\s*\$?\s*{NUMBER}(?:\s*dollars?)?", re.IGNORECASE),
    # "50 max", "$25 max", "50 dollars or less", "$30 or less"
    re.compile(rf"\$?\s*\b{NUMBER}\s*(?:dollars?\s*)?(?:max|or less)\b", re.IGNORECASE),
    # a bare "$30"
    re.compile(rf"\$\s*{NUMBER}(?:\s*dollars?)?", re.IGNORECASE),
]

# "size M", "size xl", "size US 9", "size W30", "size small"
SIZE_PATTERN = re.compile(
    r"\bsize\s+(us\s*\d+(?:\.\d+)?|w\d+(?:\s*l\d+)?|xxs|xs|xxl|xl|small|medium|large|s|m|l)\b",
    re.IGNORECASE,
)
SIZE_WORDS = {"small": "S", "medium": "M", "large": "L"}

FILLER_PATTERN = re.compile(
    r"\b(?:i'?m looking for|looking for|i want|i need|find me|show me|something|please)\b",
    re.IGNORECASE,
)


def parse_query(query: str) -> dict:
    """
    Pull a description, a size, and a max_price out of a plain-language query.

    Regex, not the model, so the same query always parses the same way.
    Anything not recognised as a size or price stays in the description.
    """
    max_price = None
    price_match = None
    for pattern in PRICE_PATTERNS:
        price_match = pattern.search(query)
        if price_match:
            max_price = max(float(number) for number in price_match.groups() if number)
            break

    size = None
    size_match = SIZE_PATTERN.search(query)
    if size_match:
        raw_size = size_match.group(1).lower()
        size = SIZE_WORDS.get(raw_size, raw_size.upper())

    description = query
    for match in (price_match, size_match):
        if match:
            description = description.replace(match.group(0), " ")
    description = FILLER_PATTERN.sub(" ", description)
    description = " ".join(re.sub(r"[,$]", " ", description).split())

    return {"description": description, "size": size, "max_price": max_price}


def _no_results_message(parsed: dict) -> str:
    """Say what was searched and which filter to loosen."""
    message = f"No listings matched \"{parsed['description']}\""
    filters = []
    if parsed["size"]:
        filters.append(f"size {parsed['size']}")
    if parsed["max_price"] is not None:
        filters.append(f"under ${parsed['max_price']:.0f}")
    if filters:
        return (
            f"{message} with {' and '.join(filters)}. "
            f"Try removing the {' or '.join(filters)} filter, or use different keywords."
        )
    return (
        f"{message}. Try different keywords, like a category (jacket, jeans, tee) "
        "or a style (vintage, y2k)."
    )


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

    ─────────────────────────────────────────────────────────────────────────
    TODO — build this, following the branch rule you wrote in Milestone 2.

    ─────────────────────────────────────────────────────────────────────────
    IN UNIT 4 you come back and add two things:

      • Trace calls. One per step. `trace.step("search_listings", inputs=...,
        returned=...)` — see trace.py. Your README needs the output.

      • A handler for ModelUnavailable, so a bad key produces a message rather
        than a stack trace. The import is already at the top of this file.
    """
    # 1. Start a session with new_session().
    session = new_session(query, wardrobe)
    trace.step(
        name="new session",
        inputs=json.dumps({
            "query": query,
            "wardrobe":wardrobe
            }))
    # 2. Count the times round the loop, and call trace.check_iterations(count)
    #  on each one before you go again. It raises when the count passes
    #  MAX_ITERATIONS in config.py — see trace.py.

    count = 0
    trace.check_iterations(count)

    # 3. Parse the query into a description, a size, and a max_price. Regex,
    #  string splitting, or asking the model are all fine — say which you
    #  chose in your README. Put the result in session["parsed"].
    session["parsed"] = parse_query(query)

    # 4. Call search_listings() with what you parsed.
    #  Put the results in session["search_results"].
    #
    #  ⚠️ THIS IS THE BRANCH. If nothing came back:
    #       - put a message in session["error"] saying what the user could
    #         change — "No results" is not that message
    #       - return the session
    #       - do NOT call suggest_outfit with nothing

    parsed = session["parsed"]
    # direct call to search_listings
    # session["search_results"] = search_listings(
    #     parsed["description"],
    #     size=parsed["size"],
    #     max_price=parsed["max_price"],
    # )

    # MCP call to search_listings

    arguments = {
        "description": parsed["description"],
        "size": parsed["size"],
        "max_price": parsed["max_price"]
    }
    session["search_results"] = call_tool(name="search_listings", arguments=arguments)

    trace.step(
        name="search_listings",
        inputs=json.dumps(arguments, indent=2),
        returned=session["search_results"]
    )
    if not session["search_results"]:
        session["error"] = _no_results_message(parsed)
        return session

    # 5. Choose an item — the first result is fine. Put it in
    #  session["selected_item"].

    session["selected_item"] = session["search_results"][0]

    # 6. Call suggest_outfit() with the selected item and the wardrobe.
    #  Put the result in session["outfit_suggestion"].
    session["outfit_suggestion"] = suggest_outfit(
        new_item=session["selected_item"],
        wardrobe=session["wardrobe"],
    )
    trace.step(
        name="outfit_suggestion",
        inputs=json.dumps({
            "new_item": session["selected_item"],
            "wardrobe": session["wardrobe"],
        }),
        returned=session["outfit_suggestion"]
    )

    # 7. Call create_fit_card() with the outfit and the item.
    #  Put the result in session["fit_card"].
    session["fit_card"] = create_fit_card(
        outfit=session["outfit_suggestion"],
        new_item=session["selected_item"]
    )

    trace.step(
        name="create_fit_card",
        inputs=json.dumps({
            "outfit": session["outfit_suggestion"],
            "new_item": session["selected_item"]
        }),
        returned=session["fit_card"]
    )
    # 8. Return the session.
    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
