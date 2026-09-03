# Decisions

## 2026-09-03: adopt the trooperthorn release and security baseline

Applied the CalVer release pipeline, SHA-pinned validate/security workflows,
`SECURITY.md`, `CODEOWNERS`, and `dependabot.yml` used across trooperthorn's
other Home Assistant repositories. The fork had no releases of its own yet
(no tags, no GitHub Releases on `trooperthorn/ha_int_catholic_calendar`), so
the manifest version moved from the upstream project's `1.0.0` semantic
version to `2026.09.03.1` (CalVer `YYYY.MM.DD.N`) with no compatibility break
for existing installs.

Not applied yet: `test.yml`, `release.yml`, and `prepare-release.yml`. The
release workflow's `tests` job calls `test.yml`, which runs `pytest tests/`;
this repository ships no `tests/` directory, so wiring those three workflows
now would either fail CI on every push or require faking a passing test
step. A test suite is a prerequisite, not something to skip past. See
`docs/backlog.md`.

## 2026-09-03: `en.json` moved to `translations/en.json`

The config flow strings shipped as `custom_components/catholic_calendar/en.json`.
hassfest and Home Assistant Core both read translations from
`custom_components/<domain>/translations/en.json`; a file at the component
root is never loaded, so the config flow's UI text ("Do you want to set up
the Catholic Calendar integration?") was not actually reaching users. Moved
the file into `translations/` with no content changes.
