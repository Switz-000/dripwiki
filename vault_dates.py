#!/usr/bin/env python3
"""
vault_dates.py
The one reader of the vault's date forms, shared by generate_chronology.py,
generate_lists.py and check_frontmatter.py.

Every date in the vault is Gregorian and takes one of four forms (see the
Dates section of 00 - Meta/Style Guide.md):

    yyyy          1950          a year
    mm/yyyy       03/1976       a month
    dd/mm/yyyy    05/01/1955    a day
    dd/mm         21/08         a day that recurs every year, such as a holiday

Run this file directly for a self-check:   python vault_dates.py
"""

import calendar
import re
from dataclasses import dataclass

YEAR, MONTH, DAY, YEARLY = "year", "month", "day", "yearly"

# A yearly date is read against a year that begins on 01/01 in both calendars
# and has no leap day. 1950 is that year.
REFERENCE_YEAR = 1950

_YEAR_RE   = re.compile(r"-?\d+")
_MONTH_RE  = re.compile(r"(\d{2})/(\d{4})")
_DAY_RE    = re.compile(r"(\d{2})/(\d{2})/(\d{4})")
_YEARLY_RE = re.compile(r"(\d{2})/(\d{2})")


@dataclass(frozen=True)
class VaultDate:
    year: int | None        # None for a yearly date
    month: int | None
    day: int | None
    precision: str
    stored: str             # the form to write back out

    @property
    def sort_key(self) -> tuple:
        """(year, month, day). A missing part counts as 0, so a bare year
        sorts before any dated entry in the same year."""
        return (self.year if self.year is not None else 0, self.month or 0, self.day or 0)

    def __str__(self) -> str:
        return self.stored


def _real_day(day: int, month: int, year: int) -> bool:
    return 1 <= month <= 12 and 1 <= day <= calendar.monthrange(year, month)[1]


def parse(value):
    """Return the value as a VaultDate, or None if it is not one of the four forms.

    Booleans are rejected explicitly: YAML reads `yes`/`true` as True, and
    str(True) is not a year. Only integers and strings are read, so a value
    YAML has already turned into something else (a float, or a date object
    from an ISO `1955-01-05`) is never mistaken for a date.
    """
    if isinstance(value, VaultDate):
        return value
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return VaultDate(value, None, None, YEAR, str(value))
    if not isinstance(value, str):
        return None
    s = value.strip()
    if not s:
        return None

    if _YEAR_RE.fullmatch(s):
        return VaultDate(int(s), None, None, YEAR, str(int(s)))

    m = _DAY_RE.fullmatch(s)
    if m:
        d, mo, y = (int(g) for g in m.groups())
        return VaultDate(y, mo, d, DAY, s) if y >= 1 and _real_day(d, mo, y) else None

    m = _MONTH_RE.fullmatch(s)
    if m:
        mo, y = (int(g) for g in m.groups())
        return VaultDate(y, mo, None, MONTH, s) if y >= 1 and 1 <= mo <= 12 else None

    m = _YEARLY_RE.fullmatch(s)
    if m:
        d, mo = (int(g) for g in m.groups())
        return VaultDate(None, mo, d, YEARLY, s) if _real_day(d, mo, REFERENCE_YEAR) else None

    return None


def year_of(value):
    """The year as an int, or None. For callers that only need a year."""
    d = parse(value)
    return d.year if d else None


def _selfcheck() -> int:
    import datetime

    good = {
        1950: (1950, None, None, YEAR, "1950"),
        -200: (-200, None, None, YEAR, "-200"),
        "1950": (1950, None, None, YEAR, "1950"),
        " 1966 ": (1966, None, None, YEAR, "1966"),
        "-200": (-200, None, None, YEAR, "-200"),
        "03/1976": (1976, 3, None, MONTH, "03/1976"),
        "05/01/1955": (1955, 1, 5, DAY, "05/01/1955"),
        "29/02/1956": (1956, 2, 29, DAY, "29/02/1956"),
        "21/08": (None, 8, 21, YEARLY, "21/08"),
    }
    bad = [None, "", "   ", True, False, 1950.0, datetime.date(1955, 1, 5),
           "5/1/1955", "05/1/1955", "3/1976", "13/1976", "00/1976", "32/01/1955",
           "31/02/1955", "29/02/1955", "29/02", "21/8", "1955-01-05", "~1959",
           "circa 1740", "1954-1956", "1815–1823", "5 January 1955", "January 1955",
           "12 Vereny 101 AS", "101 AS", "Disappeared 1977", "05/01/55", [1950], {"y": 1950}]
    failures = []
    for value, want in good.items():
        got = parse(value)
        if got is None or (got.year, got.month, got.day, got.precision, got.stored) != want:
            failures.append(f"parse({value!r}) gave {got!r}")
    for value in bad:
        if parse(value) is not None:
            failures.append(f"parse({value!r}) should be None, gave {parse(value)!r}")

    order = ["05/01/1955", 1955, "03/1955", "01/1955", 1954, "04/01/1955"]
    got = [str(d) for d in sorted((parse(v) for v in order), key=lambda d: d.sort_key)]
    want = ["1954", "1955", "01/1955", "04/01/1955", "05/01/1955", "03/1955"]
    if got != want:
        failures.append(f"sort order gave {got}")
    if year_of("05/01/1955") != 1955 or year_of("21/08") is not None or year_of("x") is not None:
        failures.append("year_of is wrong")

    for f in failures:
        print("FAIL", f)
    print(f"vault_dates: {len(good) + len(bad) + 2} checks, {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(_selfcheck())
