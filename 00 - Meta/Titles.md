# Titles

How offices are recorded in this vault, and what the scripts do with them.

A **title** is an article with `type: title`, in the `Titles` folder of the
country it belongs to. It owns the display rules. A person's article says
only which title they held and for how long.

A **role** is a job: engineer, journalist, advisor. Roles live on the person,
never make a holder list, and produce no chronology events.

## On the title article

- `institution` the body the title belongs to.
- `forms` how the title reads for a holder, by sex. The imperial title is
  written `Emperor of the Dripstanian Empire` and shows as `Empress ...` for
  a woman.
- `max_holders` how many people may hold it at once. Leave it out for a body
  with no fixed size, such as an assembly.
- `numbered` whether holders are counted 1, 2, 3. The count restarts in each
  sub-title.
- `subtitles` the split. By place, with `for`, which is a seat: a senate seat
  per state, a governorship per state. By time, with `start_year` and
  `end_year`, which is a period: the same office under a different name after
  a rename. A term that crosses a boundary belongs to the period it overlaps
  most.
- `interludes` years the title was not held in the normal way:
  `regency`, `disputed`, `vacant`, `abolished` or `other`, each with its own
  years and notes. A `disputed` interlude also tells the checker that two
  holders at once in those years are canon, not an error.
- `aliases` every name the title or its sub-titles went by, as plain strings,
  so links to the old names still resolve in Obsidian.

## On the person article

```yaml
titles:
  - title: "[[Senator]]"
    seat: "[[Postia]]"          # only for a title split by place
    start_year: 1970
    end_year: 1974              # "present" while in office; blank means unknown
    appointer:
    parties:
      -
    notes:

roles:
  - role: Engineer
    employer: "[[Troli Ustaras]]"
    start_year: 1982
    end_year: 1987
    notes:
```

There is no `employer` on a title: it comes from the title's `institution`.
The period is never typed; the script works it out from the years.

An occupation that just repeats a title does not belong in `occupation`. One
that repeats a role is fine.

## What the scripts do

- `generate_lists.py` writes the holder list into each title article,
  between the `%% holders:start %%` and `%% holders:end %%` lines. Only what
  lies between them is rewritten. It also reports problems: a term with no
  seat, a term outside every period, more holders at once than the title
  allows, a link to an article that is not a title.
- `generate_chronology.py` writes `CHRONOLOGY.md` and `chronology.json` from
  the same data, interludes included.

Never edit a holder list by hand. Edit the person's article.
