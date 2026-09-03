# Backlog

- 2026-09-03: No test suite exists (`tests/` is absent). Blocks wiring
  `test.yml`, `release.yml`, and `prepare-release.yml` from the trooperthorn
  release baseline; see `docs/decisions.md`. Needs
  `pytest-homeassistant-custom-component` coverage of `config_flow.py`,
  `__init__.py`, and at least the event-generation path in `calendar.py`
  before those three workflows can be added honestly.
- 2026-09-03: `sensor.py` still uses the legacy YAML `PLATFORM_SCHEMA` /
  `async_setup_platform` pattern, but `__init__.py` only forwards the config
  entry to `PLATFORMS = ["calendar"]`. The sensor platform never loads
  through the UI config flow that `manifest.json` declares
  (`"config_flow": true`); it is currently dead code unless a user still has
  a YAML `sensor: - platform: catholic_calendar` entry from before the
  config flow was added. Needs a decision: forward it through the config
  entry as a proper platform, or remove it.
- 2026-09-03: `calendar.py`'s RSS fetch does `if not channel:` on an
  `xml.etree.ElementTree` `Element` after `root.find('channel')`. An
  `Element` with no child elements is falsy even when found, which is a
  documented Python footgun (`DeprecationWarning` in newer stdlib versions);
  should be `if channel is None:`.
