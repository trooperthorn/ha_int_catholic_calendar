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

### Add the calendar
The calendar is set up through the Home Assistant UI: **Settings > Devices &
Services > Add Integration**, then search for "Catholic Calendar". Only one
instance is allowed. It takes no configuration.

### Add the sensor (optional, YAML)
The sensor is a separate legacy YAML platform and is not part of the UI
config flow above. Add it to `<config directory>/configuration.yaml`:

```yaml
sensor:
  - platform: catholic_calendar
    name: Catholic Calendar
```

**Configuration variables:**

key | description
:--- | :---
**platform (Required)** | The platform name
**name (Required)** | Name your feed

See `docs/README.md` for design notes, decisions, and open items.
