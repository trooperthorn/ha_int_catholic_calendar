"""RSS feed parsing in isolation, with the network call mocked out."""
import contextlib
import datetime
from unittest.mock import patch

import pytest

from custom_components.catholic_calendar.calendar import CatholicCalendar

pytestmark = pytest.mark.asyncio

SAMPLE_FEED = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Catholic Daily Reflections</title>
    <item>
      <title>Reflecting on Grace</title>
      <link>https://catholic-daily-reflections.com/2026/09/03/reflecting-on-grace/</link>
      <pubDate>Thu, 03 Sep 2026 04:00:00 +0000</pubDate>
      <description>&lt;p&gt;A reflection.&lt;/p&gt;</description>
    </item>
  </channel>
</rss>
"""


class _FakeResponse:
    def __init__(self, data: bytes) -> None:
        self._data = data

    def read(self) -> bytes:
        return self._data


async def test_fetch_rss_reflections_parses_title_link_and_date(hass):
    entity = CatholicCalendar(name="x", unique_id="y", hass=hass)

    with patch(
        "urllib.request.urlopen",
        return_value=contextlib.nullcontext(_FakeResponse(SAMPLE_FEED)),
    ):
        reflections = await entity._fetch_rss_reflections()

    assert list(reflections.keys()) == [datetime.date(2026, 9, 3)]
    entry = reflections[datetime.date(2026, 9, 3)]
    assert entry["title"] == "Reflecting on Grace"
    assert entry["link"] == (
        "https://catholic-daily-reflections.com/2026/09/03/reflecting-on-grace/"
    )


async def test_fetch_rss_reflections_returns_empty_on_network_error(hass):
    entity = CatholicCalendar(name="x", unique_id="y", hass=hass)

    with patch("urllib.request.urlopen", side_effect=OSError("network down")):
        reflections = await entity._fetch_rss_reflections()

    assert reflections == {}
