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
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

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
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



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

```

**Empty search**

```

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



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
