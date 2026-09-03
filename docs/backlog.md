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
- 2026-09-03: `prepare-release.yml` (zero-touch CalVer version-bump PRs) is
  not wired in. It needs `RELEASE_AUTOMATION_CLIENT_ID` and
  `RELEASE_AUTOMATION_PRIVATE_KEY` from a GitHub App installed on this repo;
  see `docs/decisions.md`. Until then, cut a release by running
  `python -m scripts.set_version --next-from-tags --timezone America/Chicago`
  on a branch, committing the version bump, and merging it.
