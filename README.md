# skill-check

A checker for Agent Skills (`SKILL.md` folders). It finds the mistakes that stop a skill loading or make it work in only one assistant: frontmatter that strict YAML parsers reject, vendor tool names and paths, missing fallbacks and broken links. One Python file, standard library only, a non-zero exit code for CI.

Why it exists: one unquoted colon in a `description` makes some tools skip the skill without a clear message, and we found that most popular skills never say what to do when a tool is missing. The two studies behind the rules, with data:
- [How portable are the most-installed agent skills?](https://proskillpacks.github.io/study/portability/) (17 of 69 contain a fallback phrase)
- [What the most-installed agent skills actually do](https://proskillpacks.github.io/study/top-skills/)

Tool page: https://proskillpacks.github.io/tools/skill-check/

## Use it

**GitHub Action.** Add this to `.github/workflows/skill-check.yml`:

```yaml
name: skill-check
on: [push, pull_request]
jobs:
  skill-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: proskillpacks/skill-check@v1
```

Inputs: `path` (folder to scan, default `.`), `strict` (`true` fails on warnings too, default `false`), `ignore` (comma-separated rule IDs, for example `SC008,SC013`). The action prints the table, writes a job summary, and fails the job on errors.

**One line locally.** Python 3, nothing to install:

```
python3 skill_check.py path/
```

Flags: `--strict` (warnings fail too), `--json` (machine-readable), `--quiet` (hide clean skills and info lines), `--ignore SC008,SC013`.

**pre-commit.**

```yaml
repos:
  - repo: https://github.com/proskillpacks/skill-check
    rev: v1.1.0
    hooks:
      - id: skill-check
```

## Example output
A real run on our own free skills repository (proskillpacks/skills), developers folder, 2026-10-04:

```
$ python3 skill_check.py skills/developers --quiet
skill                           errors  warnings  lines  scripts
accessibility-quick-audit            0         0     39  -
changelog-from-commits               0         0     39  -
pr-description-and-review-prep       0         0     43  -
readme-first-run-check               0         0     39  -
skill-portability-check              0         0     45  Python
test-gap-finder                      0         0     41  -

6 skill(s): 0 error(s), 0 warning(s)
```

And a failing fixture from this repo:

```
$ python3 skill_check.py fixtures/bad-yaml-colon/SKILL.md --quiet
bad-yaml-colon  (fixtures/bad-yaml-colon/SKILL.md)
  ERROR  [SC002] frontmatter: line 3: description: unquoted ': ' inside the value (strict YAML reads it as a nested mapping). Quote the value or reword
  warn   [SC013] the text relies on a tool or the network ('git log') but never says what to do when it is missing (for example 'if you have no shell, ask the user to paste it')

1 skill(s): 1 error(s), 1 warning(s)
```

## Rules
Errors fail the run. Warnings fail it only with `--strict`. Info lines never fail it.

| ID | Level | What it reports |
|---|---|---|
| SC001 | error | No frontmatter, or frontmatter never closed |
| SC002 | error | Frontmatter a strict YAML parser rejects (unquoted `: ` or ` #` in a value, bad indentation, duplicate key, unclosed quote) |
| SC003 | error | Missing `name` |
| SC004 | error | `name` not lowercase letters, digits and hyphens, over 64 characters, or different from the folder name |
| SC005 | error | Missing `description` |
| SC006 | error | `description` over 1024 characters |
| SC007 | warning | `description` under 40 characters |
| SC008 | warning | `description` does not say when to use the skill |
| SC009 | warning | A frontmatter key outside the public spec, or a tool-specific key such as `allowed-tools` |
| SC010 | warning | Vendor tool names (WebFetch, Skill tool, `Bash(...)`, `mcp__` and others) |
| SC011 | warning | Vendor paths (`.claude/`, `.cursor/`, `.codex/`, `.gemini/`, `$CLAUDE_*`) |
| SC012 | warning | `$ARGUMENTS` or `$0`-style text some tools substitute |
| SC013 | warning | The text relies on the web, a shell or a script and never says what to do when it is missing |
| SC014 | warning | Body over 500 lines |
| SC015 | error | A broken relative markdown link |
| SC016 | warning | Mentions a `scripts/`, `references/` or `assets/` file that is not there |
| SC017 | warning | The description says the skill writes text for other people to read (a reply, email, quote, page, summary and so on) but nothing in the skill says what to do with input that is unsure or unconfirmed |
| SC100 | info | A spec key (`license`, `compatibility`, `metadata`) that not every tool reads |
| SC101 | info | Agent products named in the text |
| SC102 | info | Body between 200 and 500 lines |
| SC103 | info | Bundled script languages |

## Ignore a rule
- For one run or one workflow: `--ignore SC008,SC013`, or the `ignore:` input of the action.
- For a whole folder, such as test fixtures: put an empty file named `.skill-check-ignore` in it. The folder and everything below it is skipped.

## Limits
- It reads files. It does not run your skill, so it cannot tell whether the instructions work or whether a tool would load the skill.
- The rules follow the public [Agent Skills spec](https://agentskills.io/specification) and our own studies. A warning is a portability risk, not a guarantee of breakage.
- The pattern lists (vendor tools, products, paths, fallback phrases) are not exhaustive and a phrase test cannot judge whether a fallback is any good.
- It never says a skill is valid or portable. It says what it found.

## Tests
`python3 tests/run_tests.py` runs the checker over four fixtures (one good, three bad) and checks the results, `--strict`, `--ignore` and the ignore file. The workflow in `.github/workflows/test.yml` runs that, and runs the action itself on a good fixture, a bad fixture and with `strict`.

## Licence
MIT. See LICENSE.

Made by Pro Skill Packs. Free skills: https://github.com/proskillpacks/skills
