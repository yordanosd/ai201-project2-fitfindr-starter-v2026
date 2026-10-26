"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
    # TODO: add what your criteria 3, 4 and 5 need.
    #
    # Set "criterion" to the number in criteria.md that the scenario tests.
    # "criterion": None means a diagnostic run — useful to have, but it isn't
    # one of your five, and run_eval.py marks it as such in the table.
    #
    # For a state criterion, any normal query works — what you're checking is
    # what ends up in the session, not what the user typed.
    #
    # For a fit-card criterion, you probably want the SAME query listed more
    # than once, or several different items, depending on what your criterion
    # actually says.
    {
        # suggest_outfit receives the same id as session["selected_item"]. Criterion 3.
        "name": "selected item reaches suggest_outfit",
        "query": "denim jacket under $50",
        "wardrobe": "example",
        "criterion": 3,
    },
    # Fit card mentions the item's actual price. Criterion 4 says 5 different
    # items, so one scenario per item.
    {
        "name": "fit card shows item price — cargo pants ($27)",
        "query": "cargo pants under $40",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        "name": "fit card shows item price — baby tee ($18)",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        "name": "fit card shows item price — denim jacket ($42)",
        "query": "denim jacket under $50",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        "name": "fit card shows item price — leather bomber ($75)",
        "query": "leather bomber",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        "name": "fit card shows item price — canvas sneakers ($20)",
        "query": "sneakers size US 9",
        "wardrobe": "example",
        "criterion": 4,
    },
    # Every search result is at or under the limit. Criterion 5 says 5
    # different phrasings, so one scenario per phrasing. Without a limit,
    # "denim jacket" also returns a $75 leather bomber, so a missed limit shows.
    {
        "name": "max price — 'under $50'",
        "query": "denim jacket under $50",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        "name": "max price — 'below 50'",
        "query": "denim jacket below 50",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        "name": "max price — '50 max'",
        "query": "denim jacket 50 max",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        "name": "max price — '50 dollars or less'",
        "query": "denim jacket 50 dollars or less",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        "name": "max price — 'under fifty'",
        "query": "denim jacket under fifty",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        # A price range. Criterion 5 can't see this bug (0 results has nothing
        # over the limit), so it's a diagnostic run.
        "name": "price range — 'between $20 and $50'",
        "query": "denim jacket between $20 and $50",
        "wardrobe": "example",
        "criterion": None,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
