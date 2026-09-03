"""Config flow: single instance, no configuration required."""
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.catholic_calendar.const import DOMAIN

pytestmark = pytest.mark.asyncio


async def test_user_flow_creates_an_entry_with_no_input(hass):
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )
    assert result["type"] == "form"
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
    assert result["type"] == "create_entry"
    assert result["title"] == "Catholic Calendar"
    assert result["data"] == {}


async def test_a_second_instance_is_rejected(hass):
    existing = MockConfigEntry(domain=DOMAIN, data={})
    existing.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )
    assert result["type"] == "abort"
    assert result["reason"] == "single_instance_allowed"
