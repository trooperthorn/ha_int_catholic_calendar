"""CalendarGenerator produces the liturgical calendar for a given year.

These are self-consistency checks (weekday relationships the liturgical
calendar guarantees by definition) rather than a re-derivation of the Easter
algorithm, so they catch real regressions without duplicating the logic
under test.
"""
import datetime

from custom_components.catholic_calendar.calendar_generator import CalendarGenerator


def _festivities_named(festivities_by_date: dict, name: str) -> list[dict]:
    return [
        festivity
        for festivities in festivities_by_date.values()
        for festivity in festivities
        if festivity["name"] == name
    ]


def test_generate_festivities_returns_a_dict_keyed_by_date():
    result = CalendarGenerator(2026).generate_festivities()
    assert isinstance(result, dict)
    assert result
    for key, value in result.items():
        assert isinstance(key, datetime.datetime)
        assert isinstance(value, list)
        assert value


def test_christmas_and_epiphany_are_fixed_dates():
    result = CalendarGenerator(2026).generate_festivities()
    christmas = _festivities_named(result, "Christmas")
    epiphany = _festivities_named(result, "Epiphany")
    assert len(christmas) == 1
    assert christmas[0]["date"] == datetime.datetime(2026, 12, 25)
    assert len(epiphany) == 1
    assert epiphany[0]["date"] == datetime.datetime(2026, 1, 6)


def test_easter_triduum_falls_on_the_correct_weekdays():
    result = CalendarGenerator(2026).generate_festivities()
    easter = _festivities_named(result, "Easter Sunday")[0]["date"]
    holy_thursday = _festivities_named(result, "Holy Thursday")[0]["date"]
    good_friday = _festivities_named(result, "Good Friday")[0]["date"]
    easter_vigil = _festivities_named(result, "Easter Vigil")[0]["date"]

    assert easter.weekday() == 6  # Sunday
    assert holy_thursday == easter - datetime.timedelta(days=3)
    assert holy_thursday.weekday() == 3  # Thursday
    assert good_friday == easter - datetime.timedelta(days=2)
    assert good_friday.weekday() == 4  # Friday
    assert easter_vigil == easter - datetime.timedelta(days=1)


def test_pentecost_and_ascension_are_relative_to_easter():
    result = CalendarGenerator(2026).generate_festivities()
    easter = _festivities_named(result, "Easter Sunday")[0]["date"]
    ascension = _festivities_named(result, "Ascension")[0]["date"]
    pentecost = _festivities_named(result, "Pentecost")[0]["date"]

    assert ascension == easter + datetime.timedelta(days=39)
    assert pentecost == easter + datetime.timedelta(days=49)
    assert pentecost.weekday() == 6  # Sunday


def test_generation_is_deterministic_across_runs():
    first = CalendarGenerator(2026).generate_festivities()
    second = CalendarGenerator(2026).generate_festivities()
    assert set(first.keys()) == set(second.keys())
