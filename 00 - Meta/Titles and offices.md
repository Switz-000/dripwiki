# Titles and offices

The register that `generate_lists.py` reads. An office listed here gets an
automatic list article in `Lists/` once three or more different people hold
it, counted from the `offices` field of person articles. An office that is not
listed here never gets a list, however many people hold it.

To add an office, add an entry to the block below. The `name` must match the
`title` written in the person articles exactly (capitalisation and wikilink
brackets are ignored).

- `name`: the office as written in `offices[].title`.
- `list`: the title of the generated list article.
- `kind`: `seat` (one holder at a time, numbered list) or `membership` (many
  holders at once, such as a senate seat; unnumbered roll). Defaults to `seat`.
- `formerly`: earlier names of the same office. Holders under any of these
  names join the same list.
- `summary`, `era`, `tags`: frontmatter for the generated article.

Never edit the files in `Lists/`. They are rewritten on every push; change the
person articles instead.

```yaml
offices:
  - name: President of Susia
    list: List of presidents of Susia
    kind: seat
    summary: Presidents of Susia in order of taking office.
    era:
      - republican-era
    tags:
      - politics/governance
      - politics/elections
  - name: President of Susia
    list: List of presidents of Susia
    kind: seat
    summary: Presidents of Susia in order of taking office.
    era:
      - republican-era
    tags:
      - politics/governance
      - politics/elections
```
