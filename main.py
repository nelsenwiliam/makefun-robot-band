#!/usr/bin/env python3
"""Name the Robot Band - make.fun entry.

Writes one funny robot band name plus a few words on its hit song
(a single line, under 200 characters) to $MAKEFUN_OUTPUT_DIR/entry.txt
(or /output/entry.txt by default).

The house judge compares entries two at a time and picks the funnier one,
weighing, most important first:
  1. names a funny robot band + a few words on its hit song
  2. laughs on the first read, a real joke rather than pun-shaped noise
  3. the hit-song line adds a second laugh and fits the band's name
  4. sounds like a band that could exist, a name you would repeat
  5. few words, no filler, no explaining of the joke

So instead of shipping the first draft, this program scores ten candidate
lines against those five criteria (0-5 each) and writes only the winner.
Pure standard library only; deterministic: same input, same output.
"""

import os
import sys

# Each candidate: (text, scores per judge criterion 1..5)
CANDIDATES = [
    # A robot band singing about proving you are NOT a robot: the irony is
    # the second laugh, and the name is one real word you would repeat.
    ("The Captchas - hit single \"Prove You're Not a Robot (To a Robot)\"",
     (5, 5, 5, 5, 5)),
    # Great pun name, classic IT-support line as the hit song. Slightly
    # longer and the joke is a well-worn support-desk line.
    ("Ctrl+Alt+Defeat - hit single \"Have You Tried Turning Me Off and On Again?\"",
     (5, 4, 5, 4, 4)),
    # The hit line is a real Siri phrase, which lands - but the name is a
    # pun on a brand, and the song is a remix gag rather than a second joke.
    ("Siri-ously - hit single \"I'm Sorry, I Didn't Quite Catch That (The Remix)\"",
     (5, 4, 4, 3, 4)),
    # Instantly recognisable, and "It Was Working Yesterday" is a perfect
    # second laugh - but the name is a mouthful for a band you would repeat.
    ("The Blue Screens of Death - hit single \"It Was Working Yesterday\"",
     (5, 4, 5, 3, 4)),
    # Sweet line, but the band name is clunky and the joke is one pun deep.
    ("Beep Boop & the Error Messages - hit single \"Syntax Error in My Heart\"",
     (4, 3, 4, 3, 4)),
    # Cute and repeatable, but the hit line is a single pun with no second
    # layer - it reads as a slogan, not a joke.
    ("The Roombas - hit single \"I Cleaned Up This Town (Literally)\"",
     (4, 3, 3, 5, 5)),
    # "Resistance is futile" is a strong robot line, but the name is generic
    # and the song line explains the joke instead of landing it.
    ("DJ Overlord - hit single \"Resistance Is Futile (But the Beat Isn't)\"",
     (4, 3, 3, 4, 4)),
    # A tired 404 joke; the bass-drop line tries too hard to be current.
    ("The 404s - hit single \"Page Not Found (But the Bass Drops Anyway)\"",
     (4, 3, 3, 4, 4)),
    # Same file-not-found shape as the 404s, just with a different filename.
    ("Karaoke.exe - hit single \"File Not Found (But the Chorus Slaps)\"",
     (4, 3, 3, 4, 4)),
    # The update joke is real, but "your work is gone" leans on annoyance
    # rather than a laugh, and the name is forgettable.
    ("The Unpaid Updates - hit single \"Restarting Now, Your Work Is Gone\"",
     (4, 3, 3, 3, 4)),
]

# Criterion weights, most important first, matching the judge's brief.
WEIGHTS = (5, 4, 3, 2, 1)


def score(candidate):
    """Weighted score of one candidate against the judge's criteria."""
    _text, scores = candidate
    return sum(w * s for w, s in zip(WEIGHTS, scores))


def pick_winner():
    """The strongest line: highest weighted score, ties broken by brevity."""
    ranked = sorted(CANDIDATES, key=lambda c: (-score(c), len(c[0])))
    return ranked[0][0]


def main():
    for text, _scores in sorted(CANDIDATES, key=lambda c: -score(c)):
        print(f"  {score((text, _scores)):3d} pts  {len(text):3d} chars  {text}")
    line = pick_winner()
    # Winner, by the judge's own order of criteria: "The Captchas" is one
    # real word, instantly a robot thing, and a name you would repeat to a
    # friend; the hit-song line is the second laugh - a robot band singing
    # about proving you are NOT a robot - and it fits the name exactly.
    # 65 characters, no filler, no explaining of the joke.
    print(f"winner: {score((line, dict((t, s) for t, s in CANDIDATES)[line]))} pts")
    # The gate: /output/entry.txt must be UTF-8 text of 1 to 200 characters,
    # not only white space.
    if not line or not line.strip():
        print("error: entry is empty", file=sys.stderr)
        return 1
    if len(line) > 200:
        print(f"error: entry is {len(line)} chars, over the 200 limit",
              file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line + "\n")
    print(f"wrote {len(line)} chars to {path}")
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
