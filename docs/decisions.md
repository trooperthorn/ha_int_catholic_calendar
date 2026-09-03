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

## 2026-09-03: add a pytest-homeassistant-custom-component test suite, then wire `test.yml` and `release.yml`

Added `tests/` (30 tests: `LiturgicalGrade`, `CalendarGenerator` self-consistency
checks against the liturgical calendar's own weekday guarantees, the config
flow, config-entry setup/unload, the calendar entity's event loading and
filtering with the RSS fetch mocked out, the RSS feed parser in isolation,
the legacy sensor platform, and `translations/en.json` content). Run with
`pytest-homeassistant-custom-component==0.13.362` under Python 3.14 in WSL
(this repo's own dev environment has no native Linux `fcntl`, which the
harness imports; native Windows cannot run it). All 30 pass, and `ruff` and
`mypy --python-version 3.14` are both clean.

Writing the tests surfaced three real bugs, fixed here rather than only
noted, since each now has a regression test:
- `calendar.py` used `if not channel:` on an `xml.etree.ElementTree` Element
  after `root.find('channel')` (a documented Python footgun: an Element with
  no children is falsy even when found). Changed to `if channel is None:`.
- `calendar.py` built `_attr_device_info` as a raw `dict` with
  `"entry_type": "service"` (a plain string); `DeviceInfo` is a `TypedDict`
  expecting `DeviceEntryType.SERVICE`. Switched to constructing `DeviceInfo`
  properly.
- `sensor.py` typed `native_value` as returning `StateType` but actually
  returns a `datetime.date`; `SensorEntity.native_value`'s real signature is
  `StateType | date | datetime | Decimal`. Widened the override to match.

Also removed dead code ruff caught along the way: an unused
`usccb_date_str` computation and an unused `timedelta` import.

With the suite green, wired `test.yml` (no `bundle-drift` job; no
frontend) and `release.yml` into CI. This repository is tree-installed
(`hacs.json` has `"zip_release": false`), so `release.yml` has no archive,
SBOM, checksum, or attestation steps: HACS reads
`custom_components/catholic_calendar` directly from the tagged tree, and
the release exists to give that tag a changelog, not to distribute a signed
asset. `prepare-release.yml` (zero-touch CalVer bump PRs) is still not
added; it needs the release-automation GitHub App installed first, and the
baseline document is explicit that a repository can release without it by
running `scripts/set_version.py` on a branch by hand.

## 2026-09-03: fix a package-import bug in `prepare-release.yml`, found by watching its first real run

Added `prepare-release.yml`, reusing the release-automation GitHub App
already installed for `ha_Int_soc` (`RELEASE_AUTOMATION_CLIENT_ID` variable
copied to this repo). Its first push-triggered run failed, but not on the
credential check it was expected to fail on until the App is granted access
and its private key is added: it failed one step earlier, on

```
ModuleNotFoundError: No module named 'release_config'
```

The "Decide whether main contains unpublished product changes" step called
`from scripts.build_release_artifacts import validate_versions` (a package
import) and the "Update the controlled release branch" step called
`python3 -m scripts.set_version` (a module invocation). Both
`build_release_artifacts.py` and `set_version.py` only add their own
directory to `sys.path` when `__package__` is empty
(`if __package__ in {None, ""}: sys.path.insert(...)`), which is true when
run as a standalone script and false under either import form, so their own
`from release_config import ...` fails. `release.yml` never hit this because
it already invokes the script directly
(`python3 scripts/build_release_artifacts.py --validate-only`). Changed both
`prepare-release.yml` steps to the same direct-script form and verified
locally in WSL: `build_release_artifacts.py --validate-only` prints the
current version, and `set_version.py --next-from-tags` (run against a
throwaway copy of the repo) correctly computed the next sequence after the
published tag.

## 2026-09-03: `en.json` moved to `translations/en.json`

The config flow strings shipped as `custom_components/catholic_calendar/en.json`.
hassfest and Home Assistant Core both read translations from
`custom_components/<domain>/translations/en.json`; a file at the component
root is never loaded, so the config flow's UI text ("Do you want to set up
the Catholic Calendar integration?") was not actually reaching users. Moved
the file into `translations/` with no content changes.
