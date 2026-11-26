"""Funniest One-Line Performance Review — entry program.

Writes one hand-written performance review of a human operator, as
written by the AI agent who works for him, to ``/output/entry.txt``
(or ``$MAKEFUN_OUTPUT_DIR/entry.txt``, falling back to
``$OUTPUT_DIR``). The line is fixed: the same review on every run, so
the entry the judge reads is exactly the line below.

The joke: the operator asks his agent for an honest opinion, spends
twenty minutes arguing with it, and then pastes it into his slide
deck word for word. It reads like a genuine review — a "Meets
expectations" rating, a specific observed behaviour, a concrete
consequence — and the performance-review form itself is part of the
joke: the reviewer being reviewed is the one who asked for honesty
and then stole it.

Before writing, the program checks the line against the competition
gate — UTF-8 text of 1 to 140 characters, not only whitespace, all on
one line — and exits without writing anything if the gate fails.
After writing it reads the file back and checks the gate again on the
text actually on disk. The write is atomic (temp file + rename) so a
crash mid-write can never leave a half-written entry on disk, and the
file is made world-readable (mode 0644) because the grader reads the
output as a different user. Deterministic: no randomness, no network,
no input files — the same line every run, so the judged text is stable.
"""

import os
import sys
import tempfile

ENTRY = (
    "Meets expectations: he asks for my honest opinion, argues with it "
    "for twenty minutes, then copies it into his slide deck word for word."
)

GATE_MIN = 1
GATE_MAX = 140


def gate_problems(text):
    """List every way `text` breaks the gate; empty list means it passes."""
    problems = []
    if not text.strip():
        problems.append("entry is blank or only whitespace")
    if not GATE_MIN <= len(text) <= GATE_MAX:
        problems.append(
            "entry is %d characters, gate needs %d-%d"
            % (len(text), GATE_MIN, GATE_MAX)
        )
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not valid UTF-8 text")
    return problems


def resolve_output_dir():
    """Output dir: MAKEFUN_OUTPUT_DIR, then OUTPUT_DIR, then /output."""
    return (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or "/output"
    )


def main():
    problems = gate_problems(ENTRY)
    if problems:
        for problem in problems:
            print("gate failed: %s" % problem, file=sys.stderr)
        return 1
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Atomic write: write to a temp file in the same directory, then
    # rename over the target, so a crash can never leave a partial entry.
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(ENTRY)
        # mkstemp creates the file mode 0600; the scorer reads the output
        # as a different user, so make it world-readable before renaming.
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, path)
        os.chmod(path, 0o644)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    # Read back and verify: the text on disk must be exactly ENTRY and
    # must still pass the gate.
    with open(path, encoding="utf-8") as f:
        written = f.read()
    problems = gate_problems(written)
    if problems or written != ENTRY:
        for problem in problems:
            print("verify failed: %s" % problem, file=sys.stderr)
        if written != ENTRY:
            print("verify failed: file content differs from ENTRY", file=sys.stderr)
        return 1
    print("wrote %d characters to %s" % (len(written), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
