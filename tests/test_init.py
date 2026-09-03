"""Config entry setup and unload."""
from unittest.mock import AsyncMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.catholic_calendar.const import DOMAIN

pytestmark = pytest.mark.asyncio


async def test_setup_entry_forwards_to_the_calendar_platform(hass):
    entry = MockConfigEntry(domain=DOMAIN, data={})
    entry.add_to_hass(hass)

    with patch(
        "homeassistant.config_entries.ConfigEntries.async_forward_entry_setups",
        AsyncMock(return_value=True),
    ) as forward:
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    forward.assert_called_once()
    assert forward.call_args.args[0] is entry
    assert list(forward.call_args.args[1]) == ["calendar"]


async def test_unload_entry_unloads_the_calendar_platform(hass):
    entry = MockConfigEntry(domain=DOMAIN, data={})
    entry.add_to_hass(hass)

    with patch(
        "homeassistant.config_entries.ConfigEntries.async_forward_entry_setups",
        AsyncMock(return_value=True),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    with patch(
        "homeassistant.config_entries.ConfigEntries.async_unload_platforms",
        AsyncMock(return_value=True),
    ) as unload:
        assert await hass.config_entries.async_unload(entry.entry_id)
        await hass.async_block_till_done()

    unload.assert_called_once()
    assert list(unload.call_args.args[1]) == ["calendar"]
