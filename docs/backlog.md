# Backlog

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
