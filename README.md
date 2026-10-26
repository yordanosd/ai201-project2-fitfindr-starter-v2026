# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **Search the listings data for items matching a description, and optionally a
    size and a price ceiling.:**
- **Inputs:**

    ```
    - description: string
    - size (Optional): string
    - max_price (Optional): float
  ``` 
<!-- name and type each: `max_price` (float), not "a price" -->
- **Returns:**
    ```
    A list of matching listing dicts, best match first.
  
    Each listing dict has these fields:
        id (string), title (string), description (string), category (string), style_tags (list[string]), size (string),
        condition (string), price (float), colors (list[string]), brand (str or None), platform (string)
    ```

- **When it has nothing:**
     ```
    an empty list, not None
    ```

### `suggest_outfit`

- **What it does:**

    ```
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.
    ```
- **Inputs:**
    ```
    new_item: a listing dict — the item the user is considering.
      {
        "id": "string — unique identifier for this item",
        "name": "string — short description of the piece",
        "category": "string — one of: tops, bottoms, outerwear, shoes, accessories",
        "colors": ["string — list of colors this item contains"],
        "style_tags": ["string — list of style descriptors"],
        "notes": "string (optional) — any notes about fit, how the user styles it, etc."
      }
  
    wardrobe: a wardrobe dict with an 'items' key holding a list of items.
              It may be empty.
      {
        "items": [
          {
          "id": "string — unique identifier for this item",
          "name": "string — short description of the piece",
          "category": "string — one of: tops, bottoms, outerwear, shoes, accessories",
          "colors": ["string — list of colors this item contains"],
          "style_tags": ["string — list of style descriptors"],
          "notes": "string (optional) — any notes about fit, how the user styles it, etc."
        }
      }
    ```
- **Returns:**
    ```
    String:
    A non-empty string with outfit suggestions.
    ```
- **When it has nothing:**
    ```
    With an empty wardrobe, return general styling advice rather than
    raising or returning.
    ```

### `create_fit_card`

- **What it does:**

    ```
    Write a short caption someone would actually post about the find.
    ```
- **Inputs:**
    ```        
  outfit (String):   the outfit suggestion string from suggest_outfit().
  new_item (String): the listing dict for the item.
    ```
- **Returns:**
    ```
   String: A two-to-four sentence caption.
    ```
- **When it has nothing:**
    ```
    If `outfit` is empty or whitespace, return a descriptive message rather
    than raising.
    ```
  
---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->
How the query is parsed: Regex, not the model, in agent.py::parse_query. It uses a predefined set of words and patterns to find a size or price in the query and turns them 
into values the search filter can use (for example, "under $30" becomes max_price = 30). Because the patterns are written by hand, the parser can miss what the user means if 
they phrase it in a way I didn't plan for, like "cheap," "under thirty," or "medium" without the word "size." When that happens, the words stay in the description and search 
runs without that filter.

**What moves through the session:** <!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```
```
❯   python app.py ask '90s track jacket in size M'

  Found:    90s Track Jacket — Navy/White Stripe — $45.0 on poshmark

  Outfit:   Here are two ways to style your new **90s Track Jacket — Navy/White Stripe**:

**Sporty Streetwear**
Pair the 90s Track Jacket — Navy/White Stripe over the white ribbed tank top with the baggy straight-leg jeans, and finish the look with the chunky white sneakers.

**Casual Contrast**
Layer the 90s Track Jacket — Navy/White Stripe over the white ribbed tank top with the wide-leg khaki trousers, and complete the outfit with the chunky white sneakers.

  Fit card: That navy and white champion jacket is so crisp and I scored it on Poshmark for just $45. I threw it on over a white ribbed tank top with some baggy straight-leg jeans and finished the fit with chunky white sneakers. It honestly feels like the ultimate thrifted weekend uniform.

2 model calls this session, 662 prompt + 168 output tokens
```

Matches Nothing
```
❯  python app.py ask 'designer ballgown size XXS under $5'                                 

No listings matched "designer ballgown" with size XXS and under $5. Try removing the size XXS or under $5 filter, or use different keywords.

0 model calls this session
```

```
❯ python agent.py
=== A query the data can match ===
  found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop
  outfit:   **Streetwear Contrast**
Pair the Y2K Baby Tee — Butterfly Print with baggy straight-leg jeans, dark wash, and chunky white sneakers for an effortless early 2000s look.

**Edgy Retro**
Layer the Vintage black denim jacket over the Y2K Baby Tee — Butterfly Print, and finish with wide-leg khaki trousers and black combat boots.
  fit card: This little butterfly tee brings me right back to middle school in the best way possible. I scored it on Depop for just $18 and it's already my new favorite piece. I love wearing it with baggy straight-leg jeans and chunky white sneakers for an effortless early 2000s look.

=== A query it can't ===
  stopped: No listings matched "designer ballgown" with size XXS and under $5. Try removing the size XXS or under $5 filter, or use different keywords.
  fit_card is None — it should still be None here

The second one should stop before the fit card. If both paths look the same,
the branch isn't doing anything yet.
```

**The three tools, tested one at a time**

**search_listings**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```

```
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_012', 'title': 'Oversized Crewneck Sweatshirt — Vintage Navy', 'description': 'Perfectly faded navy crewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics, clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, 'platform': 'thredUp'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

**suggest_outfit**

```
$ python -c "from tools import suggest_outfit; ..."
python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], []))"
```

```
Here are a couple of general outfit ideas using common basics to help you style your new piece:

**Effortless Casual**
Pair the Vintage Levi's 501 Jeans — Medium Wash with a tucked-in white crewneck tee and classic canvas sneakers for an effortlessly cool, timeless everyday look.

**Streetwear Edge**
Style the Vintage Levi's 501 Jeans — Medium Wash with an oversized black hoodie and chunky loafers to give your outfit a modern, relaxed edge.```

**create_fit_card**
```

**create_fit_card**

```
$ python -c "from tools import create_fit_card; ..."
python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

```

```
These vintage Levi's fit like an absolute dream and I can't believe I found them on Depop for only $38. I'm pairing them with my favorite crisp white sneakers for that classic everyday look. It is honestly so hard to beat a good pair of worn-in denim.
```
---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
- Create the parsing for the user input
- *What came back:*
- 
```
# ── query parsing ─────────────────────────────────────────────────────────────

# "under $30", "below 30", "less than $30", "max $30", "up to 30", "no more than $30",
# and a bare "$30", "$30 max", "$30 or less"
PRICE_PATTERN = re.compile(
    r"\b(?:under|below|less than|max|up to|no more than)\s*\$?\s*(\d+(?:\.\d+)?)"
    r"|\$\s*(\d+(?:\.\d+)?)(?:\s*(?:max|or less))?",
    re.IGNORECASE,
)

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
  
```
- *What I changed:*
It helped me come up with a system to parse the query and use it as a filter.

**Moment 2**

- *What I asked for:*
- Create a prompt for `create_fit_card`.
- *What came back:*
```
FIT_CARD_SYSTEM = (
    "Write a caption someone would post about a thrifted find, in a casual first-person voice. "
    "2 to 4 sentences. No hashtags, no markdown, no intro like 'Here's a caption'. "
    "Use a short, natural name for the item, not the full listing title. "
    "Mention the price and the platform exactly once each, written exactly as given. "
    "Pick one of the outfits and describe that look specifically. "
    "Open with something specific to this item, not a generic opener like 'Just thrifted' or 'Obsessed with'."
)
```
- *What I changed:*
- Added fit card system prompt.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Item suggest_outfit receives matches session["selected_item"] | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions the item's actual price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Every search result is at or below the price limit | 5 of 5 | PASS | PASS | FAIL | FAIL | FAIL | MISSED (2/5) |

Full log: `results/run_2026-10-25_2119_before.md`

Criteria 4 and 5 say "5 different items" and "5 different phrasings", so for those two rows each Try column is a different input:

- **Criterion 4:** Try 1–5 are the cargo pants ($27), baby tee ($18), denim jacket ($42), leather bomber ($75) and canvas sneakers ($20). Each item ran 5 times, and all 25 fit cards contained the item's price.
- **Criterion 5:** Try 1–5 are "under $50", "below 50", "50 max", "50 dollars or less" and "under fifty", each on "denim jacket". Search doesn't call the model, so each phrasing gave the same result on all 5 of its runs.

My first before run (`results/run_2026-10-25_2042_before.md`) tested one item for criterion 4 and one phrasing for criterion 5, and passed everything. It didn't test those criteria as written, so I fixed the scenarios and reran before changing any agent code. The table above is the rerun.

**Real output from one try**, pasted as text, naming the file and function
that produced it:

Produced by `run_eval.py::main`, running `agent.py::run_agent`. Criterion 1, try 1:

```
- Query: vintage graphic tee under $30
- Wardrobe: example
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:
**Streetwear Contrast**
Pair the Y2K Baby Tee — Butterfly Print with baggy straight-leg jeans, dark wash, and finish the look with chunky white sneakers.

**Casual Vintage**
Tuck the Y2K Baby Tee — Butterfly Print into wide-leg khaki trousers, add the brown leather belt, and layer the vintage black denim jacket on top with black combat boots.

Fit card:
This butterfly tee is giving me all the middle school nostalgia I didn't know I needed. I scored it on Depop for just $18 and it's practically brand new. I'm wearing it tucked into wide-leg khaki trousers with a brown leather belt, finished off with a vintage black denim jacket and black combat boots.

Trace:
[1] new session
      in:  {"query": "vintage graphic tee under $30", "wardrobe": {"items": [{"id": "w_001", "name": "Baggy straight-leg …
[2] search_listings
      in:  {   "description": "vintage graphic tee",   "size": null,   "max_price": 30.0 }
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] outfit_suggestion
      in:  {"new_item": {"id": "lst_002", "title": "Y2K Baby Tee — Butterfly Print", "description": "Super cute earl…
      out: **Streetwear Contrast** Pair the Y2K Baby Tee — Butterfly Print with baggy straight-leg jeans, dark wash, and …
[4] create_fit_card
      in:  {"outfit": "**Streetwear Contrast**\nPair the Y2K Baby Tee — Butterfly Print with baggy straight-leg jean…
      out: This butterfly tee is giving me all the middle school nostalgia I didn't know I needed. I scored it on Depop f…
      
  Outfit:   **Streetwear Contrast**
Pair the Y2K Baby Tee — Butterfly Print with baggy straight-leg jeans, dark wash, and chunky white sneakers for an effortless early 2000s look.

**Edgy Retro**
Layer the Vintage black denim jacket over the Y2K Baby Tee — Butterfly Print, and finish with wide-leg khaki trousers and black combat boots.

  Fit card: This butterfly tee fits like an absolute dream and I still can't believe I found it on Depop for just $18. I paired it with baggy straight-leg jeans in a dark wash and chunky white sneakers to lean fully into the nostalgic early 2000s energy. It is definitely going to be my new summer go-to.
```

Criterion 5, "50 max", try 1 (FAIL), from `results/run_2026-10-25_2119_before.md`:

```
- Query: denim jacket 50 max
- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 8

[2] search_listings
      in:  {   "description": "denim jacket 50 max",   "size": null,   "max_price": null }
      out: 8 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +5 more
```

`max_price` is `null`, so search ran with no limit and returned 8 results instead of 7. The extra one is the $75 leather bomber.

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | A matching query completes all three tools | 4 of 5 | MET (5/5) | Every try for "vintage graphic tee under $30" ran search, suggest_outfit and create_fit_card, and ended with a fit card. |
| 2 | An impossible query stops before the second tool | 5 of 5 | MET (5/5) | Every try for "designer ballgown size XXS under $5" got `[]` from search and stopped before suggest_outfit, with a message naming the size and price filters to remove. |
| 3 | Item suggest_outfit receives matches session["selected_item"] | 5 of 5 | MET (5/5) | In every trace, the top search result and the `new_item` that reached suggest_outfit were both `lst_007`, and every fit card described that same cropped denim jacket. |
| 4 | Fit card mentions the item's actual price | 5 of 5 | MET (5/5) | I searched each full fit card in the results file for that item's price ("$27", "$18", "$42", "$75", "$20"). All 25 cards across the 5 items had it. |
| 5 | Every search result is at or below the price limit | 5 of 5 | MISSED (2/5) | For each phrasing I checked the parsed `max_price` in the trace and the prices of every result. "under $50" and "below 50" returned 7 results, all $24–$45. "50 max", "50 dollars or less" and "under fifty" parsed to `max_price = null` and each returned the $75 leather bomber. |

**Diagnoses**

**Criterion 5 missed on 3 of 5 phrasings, and all 3 have the same cause.** The miss happened in the query parsing step (`agent.py::parse_query`), not in search. The price regex only knew phrasings where a keyword comes before the number ("under 50") or a "$" is attached to it ("$50 max"). "50 max" and "50 dollars or less" put the keyword after a bare number, and "under fifty" writes the number as a word. None of them matched, so `parse_query` returned `max_price = None`, and search treats `None` as "no limit". Search itself worked: it applied exactly the limit it was given, which was none. The failure is silent. The user still sees a $42 jacket at the top, but the $75 bomber is in their results even though they asked for 50 max.

**A second parsing bug that criterion 5 can't see.** "between $20 and $50" (a diagnostic run) parsed as `max_price = 20`, because the regex took the first dollar amount. Search found nothing under $20 and stopped with "No listings matched". Criterion 5 only checks that nothing is *over* the limit, and an empty result passes that. So this bug passes my criterion while hiding every jacket from $20 to $50. It's the same step and the same kind of cause (the price regex reading the query wrong), so I treat it as part of one problem.

**Criteria 1–4 held, as expected.** Criteria 2 and 3 are plain code (an `if` check and passing a dictionary), so 5 of 5 is what they should do. Criterion 4 is the only one that depends on model output, and it held on all 5 items.

**How I got here.** My first before run passed everything, but it tested criterion 4 on one item and criterion 5 on one phrasing. I fixed the scenarios to match what the criteria say and reran without touching the agent, and that rerun is where the miss appeared.

**Were my targets too low?** Criterion 1 is the one I'd tighten. I allowed 4 of 5 because keyword search can miss plurals and synonyms, but I tested it with "vintage graphic tee", three words that appear in the listings exactly as typed. That query was never going to miss. A fair test would use the phrasings I said would break it, like "graphic tees" or "trainers". My search already handles plurals, so I'd expect plurals to pass and synonyms to fail.

Criteria 2, 3 and 5 are about plain code (an `if` check, dictionary passing and a numeric comparison), so 5 of 5 is the right target, and passing them is what I expected. Criterion 4 is the only one that depends on model output, and it held 5 of 5, but only on one item.



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
❯ python app.py ask 'vintage graphic tee' --trace
[1] new session
      in:  {"query": "vintage graphic tee", "wardrobe": {"items": [{"id": "w_001", "name": "Baggy straight-leg jeans, dar…
[2] search_listings
      in:  {   "description": "vintage graphic tee",   "size": null,   "max_price": null }
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] outfit_suggestion
      in:  {"new_item": {"id": "lst_002", "title": "Y2K Baby Tee \u2014 Butterfly Print", "description": "Super cute earl…
      out: **Streetwear Contrast** Pair the Y2K Baby Tee — Butterfly Print with baggy straight-leg jeans, dark wash, and …
[4] create_fit_card
      in:  {"outfit": "**Streetwear Contrast**\nPair the Y2K Baby Tee \u2014 Butterfly Print with baggy straight-leg jean…
      out: This little pink butterfly tee is honestly the cutest thing I’ve scored all month. I found it on Depop for jus…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Streetwear Contrast**
Pair the Y2K Baby Tee — Butterfly Print with baggy straight-leg jeans, dark wash, and chunky white sneakers for an effortless early 2000s look.

**Edgy Retro**
Layer the Vintage black denim jacket over the Y2K Baby Tee — Butterfly Print, and finish with wide-leg khaki trousers and black combat boots.

  Fit card: This little pink butterfly tee is honestly the cutest thing I’ve scored all month. I found it on Depop for just $18 and it fits like an absolute dream. I’m thinking of wearing it with baggy straight-leg jeans in a dark wash and some chunky white sneakers for the ultimate early 2000s look.

1 model calls this session, 1 served from cache, 239 prompt + 70 output tokens
```

**Empty search**

```
❯ python app.py ask '' --trace --empty-wardrobe 
(running with an empty wardrobe)
Ask for something, or press Enter on an empty line to quit.

> 
0 model calls this session
```

**Empty Wardrobe**
```
❯ python app.py ask 'vintage graphic tee' --trace --empty-wardrobe
(running with an empty wardrobe)
[1] new session
      in:  {"query": "vintage graphic tee", "wardrobe": {"items": []}}
[2] search_listings
      in:  {   "description": "vintage graphic tee",   "size": null,   "max_price": null }
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] outfit_suggestion
      in:  {"new_item": {"id": "lst_002", "title": "Y2K Baby Tee \u2014 Butterfly Print", "description": "Super cute earl…
      out: Here are a couple of general ideas for how you could style your new **Y2K Baby Tee — Butterfly Print** using b…
[4] create_fit_card
      in:  {"outfit": "Here are a couple of general ideas for how you could style your new **Y2K Baby Tee \u2014 Butterfl…
      out: Found the cutest little butterfly tee on Depop for just $18. I am definitely styling it the sweet and sporty w…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Here are a couple of general ideas for how you could style your new **Y2K Baby Tee — Butterfly Print** using basic wardrobe staples:

**90s Casual**
Pair the Y2K Baby Tee — Butterfly Print with your favorite mid-rise straight-leg blue jeans and white canvas sneakers for an effortless everyday look.

**Sweet and Sporty**
Tuck the Y2K Baby Tee — Butterfly Print into a pleated white tennis skirt and finish the outfit with chunky platform sandals.

  Fit card: Found the cutest little butterfly tee on Depop for just $18. I am definitely styling it the sweet and sporty way by tucking it into a pleated white tennis skirt and finishing the whole outfit with chunky platform sandals. It has the prettiest pink and purple details that just scream early 2000s nostalgia.

1 model calls this session, 1 served from cache, 262 prompt + 65 output tokens
```

**Model Unavailable**
```
[1] new session
      in:  {"query": "vintage graphic tee", "wardrobe": {"items": [{"id": "w_001", "name": "Baggy straight-leg jeans, dar…
[2] search_listings
      in:  {   "description": "vintage graphic tee",   "size": null,   "max_price": null }
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] outfit_suggestion
      in:  {"new_item": {"id": "lst_002", "title": "Y2K Baby Tee \u2014 Butterfly Print", "description": "Super cute earl…
      out: **Streetwear Contrast** Pair the Y2K Baby Tee — Butterfly Print with baggy straight-leg jeans, dark wash, and …
1 model calls this session, 1 served from cache

ModelUnavailable: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

No criterion missed, but my tests only covered the easy version of each one. These are the cases I haven't tested properly, or that I checked by hand and found broken.

**Price phrasings beyond "under $X".** The run only used "under $50". I checked a few other ways a user might write a price by calling `agent.py::parse_query` directly:

| Query | Parsed `max_price` | Problem |
|---|---|---|
| `denim jacket between $20 and $40` | 20 | A range reads as its *lower* number, so every item from $20 to $40 is filtered out |
| `denim jacket $20-$40` | 20 | Same as above |
| `denim jacket 50 max` | None | "max" after a number without "$" isn't recognised, so no price limit is applied |
| `denim jacket under thirty` | None | Numbers written as words aren't recognised |
| `cheap denim jacket` | None | Vague price words aren't recognised |

The range case is the worst, because it fails silently: the user gets fewer results and nothing says why. The fix would be a range pattern that takes the upper number, checked before the single-price pattern. Criterion 5 should be retested with these phrasings, which is what "5 different phrasings" in the criterion was meant to cover.

**A listing with no price.** Every listing in `data/listings.json` has a price today, so this never came up. But if one were `None`, `tools.py::create_fit_card` would crash formatting it (`TypeError: unsupported format string passed to NoneType.__format__`), and the price filter in `search_listings` would crash comparing it. Real resale data has gaps like this, the same way most listings have no brand. The fix would be to skip unpriced listings when a price limit is set, and leave the price out of the fit card prompt when it's missing. Criterion 4 would then need to say what a card should do when there's no price to mention.

**Vague queries that match but don't suit the wardrobe.** Every test query was a specific item ("cargo pants", "denim jacket") that pairs easily with the example wardrobe. I haven't tested vague queries like "something cute" or "a going-out top", which match listings by loose keywords, or items the wardrobe has nothing to go with, like a dress when the wardrobe is all jeans, tees and sneakers. In those cases I'd expect search to return a weak match, and `suggest_outfit` to either force a strange outfit or invent pieces the user doesn't own, despite the prompt rule against it. None of my criteria check for invented pieces, so this would need its own test.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [X] criteria.md has five numbered criteria, each with a target
       [X] Each criterion has a reason underneath it
       [X] All five unit 3 sections above have real content
       [X] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [X] Planning Loop names the branch rule and agent.py::run_agent
       [X] Sample Run: one full query plus the three per-tool tests, as text
       [X] At least four new commits
       [X] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [X] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [X] Run Log — Before, five criteria, five tries each
       [X] Real output pasted underneath, naming file and function
       [X] A verdict on every criterion
       [X] A diagnosis for every miss, naming a place AND a mechanism
       [X] Loop Trace, with the MCP call visible in it
       [X] All three failure modes triggered and handled
       [X] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
