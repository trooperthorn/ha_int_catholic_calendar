"""The calendar entity: event loading, filtering, and HTML cleanup.

_fetch_rss_reflections is patched to return no reflections in every test
here so the suite never makes a real network call and stays deterministic;
its own parsing logic is covered separately in test_rss_reflections.py.
"""
import datetime
from unittest.mock import AsyncMock, patch

import pytest

from custom_components.catholic_calendar.calendar import (
    CatholicCalendar,
    async_setup_entry,
)


def _entity(hass) -> CatholicCalendar:
    return CatholicCalendar(name="Catholic Calendar", unique_id="entry-1", hass=hass)


@pytest.fixture(autouse=True)
def no_rss(hass):
    with patch(
        "custom_components.catholic_calendar.calendar.CatholicCalendar._fetch_rss_reflections",
        AsyncMock(return_value={}),
    ):
        yield


async def test_async_setup_entry_adds_one_entity_named_after_the_entry(hass):
    entry = type("Entry", (), {"title": "My Parish Calendar", "entry_id": "abc123"})()
    added: list = []

    await async_setup_entry(hass, entry, lambda entities, **_: added.extend(entities))

    assert len(added) == 1
    entity = added[0]
    assert isinstance(entity, CatholicCalendar)
    assert entity.name == "My Parish Calendar"
    assert entity.unique_id == "abc123"


async def test_async_setup_entry_falls_back_to_a_default_name(hass):
    entry = type("Entry", (), {"title": None, "entry_id": "abc123"})()
    added: list = []

    await async_setup_entry(hass, entry, lambda entities, **_: added.extend(entities))

    assert added[0].name == "Catholic Calendar"


async def test_load_year_populates_and_sorts_events(hass):
    entity = _entity(hass)
    await entity.async_load_year(2026)

    assert 2026 in entity._years_loaded
    assert entity._events
    starts = [event.start for event in entity._events]
    assert starts == sorted(starts)
    christmas = [e for e in entity._events if e.summary == "Christmas"]
    assert len(christmas) == 1
    assert christmas[0].start == datetime.date(2026, 12, 25)
    assert christmas[0].end == datetime.date(2026, 12, 26)


async def test_load_year_is_idempotent(hass):
    entity = _entity(hass)
    await entity.async_load_year(2026)
    count_after_first_load = len(entity._events)
    await entity.async_load_year(2026)
    assert len(entity._events) == count_after_first_load


async def test_event_property_returns_the_first_future_event(hass):
    entity = _entity(hass)
    entity._events = [
        _fake_event(datetime.date(2020, 1, 1)),
        _fake_event(datetime.date(2099, 1, 1)),
        _fake_event(datetime.date(2099, 6, 1)),
    ]
    assert entity.event.start == datetime.date(2099, 1, 1)


async def test_event_property_returns_none_with_no_events(hass):
    entity = _entity(hass)
    assert entity.event is None


async def test_async_get_events_filters_to_the_requested_range(hass):
    entity = _entity(hass)
    await entity.async_load_year(2026)

    events = await entity.async_get_events(
        hass,
        datetime.datetime(2026, 12, 25),
        datetime.datetime(2026, 12, 25),
    )
    assert {e.summary for e in events} == {"Christmas"}


def test_clean_html_strips_tags_and_decodes_entities():
    entity = CatholicCalendar(name="x", unique_id="y", hass=None)
    raw = "<p>Grace &amp; peace&#8217;s here<br>Line two</p>"
    cleaned = entity._clean_html(raw)
    assert "<" not in cleaned
    assert "&amp;" not in cleaned
    assert "Grace & peace's here" in cleaned
    assert "Line two" in cleaned


def test_clean_html_handles_empty_input():
    entity = CatholicCalendar(name="x", unique_id="y", hass=None)
    assert entity._clean_html("") == ""
    assert entity._clean_html(None) == ""


def _fake_event(start: datetime.date):
    return type("Event", (), {"start": start})()
