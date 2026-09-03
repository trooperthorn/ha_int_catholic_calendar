# Backlog

- 2026-09-03: `sensor.py` still uses the legacy YAML `PLATFORM_SCHEMA` /
  `async_setup_platform` pattern, but `__init__.py` only forwards the config
  entry to `PLATFORMS = ["calendar"]`. The sensor platform never loads
  through the UI config flow that `manifest.json` declares
  (`"config_flow": true`); it is currently dead code unless a user still has
  a YAML `sensor: - platform: catholic_calendar` entry from before the
  config flow was added. Needs a decision: forward it through the config
  entry as a proper platform, or remove it. Covered by `tests/test_sensor.py`
  either way, so a change here has a regression check.
- 2026-09-03: `calendar.py`'s event description links to a generic USCCB
  daily-readings page (`https://bible.usccb.org/bible/readings/`) rather
  than the specific day's readings, even though the code computes the
  event's date. It's unverified whether USCCB's URL scheme supports a
  date-specific link (their site would need checking), so this was left as
  a cosmetic/content gap rather than guessed at.
- 2026-09-03: `prepare-release.yml` is now added, reusing the release-automation
  GitHub App already installed for `ha_Int_soc` (`RELEASE_AUTOMATION_CLIENT_ID`
  set on this repo). It still needs two things only Sean can do: grant that
  App access to this repository at github.com/settings/installations, and
  add its private key as the `RELEASE_AUTOMATION_PRIVATE_KEY` secret. Until
  both exist, the workflow's credential check fails fast with a clear error
  on every Release completion; a release can still be cut manually with
  `python scripts/set_version.py --next-from-tags --timezone America/Chicago`
  on a branch, committing the version bump, and merging it. (The first real
  run actually failed one step earlier than the credential check, on a
  `python3 -m scripts.build_release_artifacts` package-import bug; fixed the
  same day, see `docs/decisions.md`.)
