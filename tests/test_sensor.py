"""The sensor platform, set up through the config entry alongside calendar."""
import datetime

from custom_components.catholic_calendar.sensor import (
    CatholicCalendarSensor,
    async_setup_entry,
)


async def test_async_setup_entry_adds_one_sensor_named_after_the_entry(hass):
    entry = type("Entry", (), {"title": "My Parish Calendar", "entry_id": "abc123"})()
    added: list = []

    await async_setup_entry(hass, entry, lambda entities, **_: added.extend(entities))

    assert len(added) == 1
    sensor = added[0]
    assert isinstance(sensor, CatholicCalendarSensor)
    assert sensor.name == "My Parish Calendar"
    assert sensor.unique_id == "abc123"


async def test_async_setup_entry_falls_back_to_a_default_name(hass):
    entry = type("Entry", (), {"title": None, "entry_id": "abc123"})()
    added: list = []

    await async_setup_entry(hass, entry, lambda entities, **_: added.extend(entities))

    assert added[0].name == "Catholic Calendar"


async def test_sensor_shares_a_device_with_the_calendar_entity(hass):
    entry = type("Entry", (), {"title": "Catholic Calendar", "entry_id": "abc123"})()
    added: list = []

    await async_setup_entry(hass, entry, lambda entities, **_: added.extend(entities))

    assert added[0].device_info["identifiers"] == {("catholic_calendar", "abc123")}


def test_native_value_is_todays_date():
    sensor = CatholicCalendarSensor(name="Catholic Calendar", unique_id="abc123")
    assert sensor.native_value == datetime.datetime.now().date()


def test_update_loads_this_year_and_next_and_sorts_by_grade():
    sensor = CatholicCalendarSensor(name="Catholic Calendar", unique_id="abc123")
    sensor.update()

    today = datetime.datetime.now().date()
    assert today.year in sensor._years_loaded
    assert (today + datetime.timedelta(weeks=52)).year in sensor._years_loaded

    grades = [f["liturgical_grade"] for f in sensor._todays_festivities]
    assert grades == sorted(grades, reverse=True)
    for festivity in sensor._todays_festivities:
        assert "liturgical_grade_desc" in festivity


def test_update_is_idempotent_for_already_loaded_years():
    sensor = CatholicCalendarSensor(name="Catholic Calendar", unique_id="abc123")
    sensor.update()
    festivity_count_by_date = len(sensor._festivities)
    sensor.update()
    assert len(sensor._festivities) == festivity_count_by_date
