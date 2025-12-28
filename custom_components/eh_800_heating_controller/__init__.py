"""
Custom integration to integrate EH-800 Heating Controller with Home Assistant.

For more details about this integration, please refer to
https://github.com/jarikai/eh-800_heating_controller
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import aiohttp

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import EH800ConfigEntry

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.loader import async_get_loaded_integration

from .api import OumanEH800ApiClient
from .const import CONF_IP, SENSOR_DESCRIPTIONS
from .coordinator import EH800Coordinator
from .data import EH800Data

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: EH800ConfigEntry,
) -> bool:
    """Set up the component from a config entry."""
    _LOGGER.debug("init.py async_setup_entry launched")
    ip = entry.data[CONF_IP]

    connector = aiohttp.TCPConnector(limit_per_host=1, force_close=True)
    session = aiohttp.ClientSession(
        connector=connector, timeout=aiohttp.ClientTimeout(total=120)
    )
    # Build a list of keys that we actually want to expose
    keys = list(SENSOR_DESCRIPTIONS.keys())
    # Create the API client
    client = OumanEH800ApiClient(
        hass=hass,
        ip=ip,
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        session=session,
    )

    coordinator = EH800Coordinator(hass, client, keys, entry, session=session)
    # Store data for this config entry
    entry.runtime_data = EH800Data(
        client=client,
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()

    # Register all the sensors
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: EH800ConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: EH800ConfigEntry,
) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
