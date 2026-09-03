"""LiturgicalGrade is a plain lookup table; verify every grade resolves."""
from custom_components.catholic_calendar.liturgical_grade import LiturgicalGrade


def test_every_named_grade_has_a_description():
    for grade in (
        LiturgicalGrade.WEEKDAY,
        LiturgicalGrade.COMMEMORATION,
        LiturgicalGrade.MEMORIAL_OPT,
        LiturgicalGrade.MEMORIAL,
        LiturgicalGrade.FEAST,
        LiturgicalGrade.FEAST_LORD,
        LiturgicalGrade.SOLEMNITY,
        LiturgicalGrade.HIGHER_SOLEMNITY,
    ):
        description = LiturgicalGrade.descr(grade)
        assert isinstance(description, str)
        assert description


def test_unknown_grade_returns_none():
    assert LiturgicalGrade.descr(99) is None


def test_grades_are_ordered_low_to_high():
    assert (
        LiturgicalGrade.WEEKDAY
        < LiturgicalGrade.COMMEMORATION
        < LiturgicalGrade.MEMORIAL_OPT
        < LiturgicalGrade.MEMORIAL
        < LiturgicalGrade.FEAST
        < LiturgicalGrade.FEAST_LORD
        < LiturgicalGrade.SOLEMNITY
        < LiturgicalGrade.HIGHER_SOLEMNITY
    )
