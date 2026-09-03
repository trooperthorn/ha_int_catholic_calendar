# ha_int_catholic_calendar
Adds a Catholic Calendar sensor and calendar to home assistant.

Based off of https://github.com/Liturgical-Calendar/LiturgicalCalendarAPI for determining calendar logic.

## Support
[![coffee](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://www.buymeacoffee.com/jmacri)

## Getting Started

### Install component
Add as a custom HACS repository
OR
Copy `/custom_components/catholic_calendar/` to the following directory in Home Assistant:
`<config directory>/custom_components/catholic_calendar/`

### Add the integration
The calendar and sensor are both set up together through the Home Assistant
UI: **Settings > Devices & Services > Add Integration**, then search for
"Catholic Calendar". Only one instance is allowed. It takes no
configuration.

See `docs/README.md` for design notes, decisions, and open items.
