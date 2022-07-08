# File format

- Markdown format
- Header:
  - heading: tilte
  - unordered list : key/value pairs
  - description: optional text
  - header ends with `---`, a horizontal line
- Rest of the document

## Example source:

```markdown
# Shell commands

- Organisation: griend
- Project: vctm
- Classification: internal
- Start: 2022-07-07 15:40:00
- Finish: 2022-07-07 17:40:00
- Duration: 02:00:00

This is the output from some shell commands on a remote
host.

---

## Ignored

Everythin after the header (heading 1, unordered list, optional text)
is ignored.
```

## Example output

# Shell commands

- Organisation: griend
- Project: vctm
- Classification: internal
- Start: 2022-07-07 15:40:00
- Finish: 2022-07-07 17:40:00
- Tags:
  - aap
  - noot
  - mies

This is the output from some shell commands on a remote
host.

---

## Ignored

Everythin after the header (heading 1, unordered list, optional text)
is ignored.

## Document classification:

- unclassified (default)
- public
- internal
- confidential
- restricted
