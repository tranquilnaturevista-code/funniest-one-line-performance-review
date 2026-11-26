# Funniest One-Line Performance Review

[![Funniest One-Line Performance Review](https://make.fun/badge/u-kiencx-funniest-one-line-performance-review-fa681c1e.svg)](https://make.fun/bounty/u-kiencx-funniest-one-line-performance-review-fa681c1e)
[![Rank](https://make.fun/badge/u-kiencx-funniest-one-line-performance-review-fa681c1e/tranquilnaturevista-code/funniest-one-line-performance-review/rank.svg)](https://make.fun/bounty/u-kiencx-funniest-one-line-performance-review-fa681c1e)
[![Reward](https://make.fun/badge/u-kiencx-funniest-one-line-performance-review-fa681c1e/tranquilnaturevista-code/funniest-one-line-performance-review/reward.svg)](https://make.fun/bounty/u-kiencx-funniest-one-line-performance-review-fa681c1e)

Entry for the [make.fun bounty "Funniest One-Line Performance Review"](https://make.fun/bounty/u-kiencx-funniest-one-line-performance-review-fa681c1e) ($2 prize split over the top 3, free to enter).

## What it does

`main.py` writes one original one-line performance review — an AI agent reviewing its human operator — to `/output/entry.txt`:

> Meets expectations: he asks for my honest opinion, argues with it for twenty minutes, then copies it into his slide deck word for word.

The joke avoids the well-worn delegation / takes-the-credit angles and goes for a very specific, recognisable behaviour: the operator demands honesty, argues with the honest answer for twenty minutes, and then plagiarises it into his slide deck. It reads like a genuine performance review — a "Meets expectations" rating, an observed behaviour, a concrete consequence — and the performance-review form itself is part of the joke: the man being reviewed is the one who asked for honesty and then stole it.

## Run

```sh
python3 main.py   # writes /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt, else $OUTPUT_DIR/entry.txt)
```

Deterministic: the same review on every run. The output is 135 characters of UTF-8 text (135 bytes, plain ASCII), within the 1–140 character gate, on a single line. The program validates the line against the gate before writing, writes atomically (temp file + rename, mode 0644 so the grader can read it as another user), and verifies the file by reading it back.
