# Security Policy

## Reporting a vulnerability

Do not open a public issue containing exploit details, credentials, private
addresses, or logs. Use GitHub's private vulnerability-reporting feature for
this repository. If private reporting is unavailable, open a minimal issue
asking the maintainer to establish a private channel; omit technical details.

Include the affected version/commit, prerequisites, impact, a minimal
reproduction, and suggested remediation.

## Response targets

These are project targets, not an SLA: acknowledge critical/high reports in
three business days, establish severity and containment in seven, and publish
a coordinated fix as soon as safely validated. Lower-severity issues are
prioritized by exploitability and impact.

## Supported version

Only the latest published release and the default branch receive security
fixes.

## Security boundaries

Catholic Calendar is a Home Assistant custom integration, not a sandbox. It
runs in the same Python process as Home Assistant Core and any other
integration, so it cannot prevent a malicious integration from reading its
data or interfering with its execution. On every calendar refresh it makes
outbound HTTPS requests to `catholic-daily-reflections.com` (a daily
reflections RSS feed) and links event descriptions to `bible.usccb.org` and
`open.spotify.com`; it does not authenticate to those services and sends no
Home Assistant data to them beyond the request itself. A failure or
compromise of those third-party endpoints affects calendar event content, not
Home Assistant's own state.
