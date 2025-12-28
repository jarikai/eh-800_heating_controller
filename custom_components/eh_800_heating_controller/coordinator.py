"""DataUpdateCoordinator for eh-800_heating_controller."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

if TYPE_CHECKING:
    import aiohttp
    from homeassistant.core import HomeAssistant

    from .api import OumanEH800ApiClient
    from .data import EH800ConfigEntry


_LOGGER = logging.getLogger(__name__)


class EH800Coordinator(DataUpdateCoordinator):
    """Fetch data from the EH800 once per scan interval."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: OumanEH800ApiClient,
        keys: list,
        entry: EH800ConfigEntry,
        session: aiohttp.ClientSession,
    ) -> None:
        """Create coordinator."""
        self._session = session
        self._entry = entry
        self.ip = client.ip
        self.keys = keys
        self.client = client
        self.hass = hass
        update_interval_timedelta = timedelta(seconds=self.get_interval())

        super().__init__(
            hass,
            _LOGGER,
            name="Ouman EH800 Coordinator",
            update_interval=update_interval_timedelta,
            always_update=True,
        )

    async def _async_update_data(self) -> Any:
        """Fetch data from EH800."""
        try:
            return await self.client.fetch_all(self._session, self.keys)
        except Exception as exc:
            _LOGGER.exception("Unable to update EH800:")
            raise UpdateFailed from exc

    # coordinator.py

    def get_interval(self) -> float:
        """Return the configured interval in seconds or None."""
        interval = self._entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        try:
            # It is a string from the UI, cast it to int.
            return int(interval) * 60
        except (TypeError, ValueError):
            _LOGGER.warning(
                "Invalid scan_interval %s, falling back to default", interval
            )
            return DEFAULT_SCAN_INTERVAL * 60
