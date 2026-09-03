"""The legacy YAML sensor platform.

See docs/backlog.md: this platform is never forwarded through the config
entry (__init__.py only forwards "calendar"), so it only runs for a user who
still has a YAML `sensor: - platform: catholic_calendar` entry. Tested here
independent of that open question, since the code is still shipped and
still runs when invoked that way.
"""
import datetime

from custom_components.catholic_calendar.sensor import CatholicCalendarSensor


async def test_async_setup_platform_adds_one_sensor_with_the_configured_name(hass):
    from custom_components.catholic_calendar.sensor import async_setup_platform

    added: list = []
    await async_setup_platform(
        hass,
        {"name": "My Feed"},
        lambda entities, **_: added.extend(entities),
    )

    assert len(added) == 1
    assert added[0].name == "My Feed"


def test_native_value_is_todays_date():
    sensor = CatholicCalendarSensor(name="Catholic Calendar")
    assert sensor.native_value == datetime.datetime.now().date()


def test_update_loads_this_year_and_next_and_sorts_by_grade():
    sensor = CatholicCalendarSensor(name="Catholic Calendar")
    sensor.update()

    today = datetime.datetime.now().date()
    assert today.year in sensor._years_loaded
    assert (today + datetime.timedelta(weeks=52)).year in sensor._years_loaded

    grades = [f["liturgical_grade"] for f in sensor._todays_festivities]
    assert grades == sorted(grades, reverse=True)
    for festivity in sensor._todays_festivities:
        assert "liturgical_grade_desc" in festivity


def test_update_is_idempotent_for_already_loaded_years():
    sensor = CatholicCalendarSensor(name="Catholic Calendar")
    sensor.update()
    festivity_count_by_date = len(sensor._festivities)
    sensor.update()
    assert len(sensor._festivities) == festivity_count_by_date
