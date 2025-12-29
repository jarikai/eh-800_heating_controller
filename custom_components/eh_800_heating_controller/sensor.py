"""Sensor platform for eh-800_heating_controller."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_IP, DEVICE_NAME, DOMAIN, SENSOR_DESCRIPTIONS
from .coordinator import EH800Coordinator

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .data import EH800ConfigEntry


PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: EH800ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up sensors from a config entry."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    coordinator = entry.runtime_data.coordinator
    coordinator.ip = entry.data[CONF_IP]

    async def add_sensor(key: str) -> None:
        """Create a sensor entity for *key* and add it."""
        static_entities = []
        entity = EH800Sensor(coordinator, key)
        static_entities.append(entity)
        async_add_entities(static_entities)

    await asyncio.gather(*(add_sensor(k) for k in coordinator.data))
    return True


class EH800Sensor(CoordinatorEntity[EH800Coordinator]):
    """Representation of a single sensor on the EH800."""

    def __init__(self, coordinator: EH800Coordinator, key: str) -> None:
        """Sensor initialization."""
        super().__init__(coordinator)
        self.key = key
        self._value = coordinator.data[key]
        self._description = SENSOR_DESCRIPTIONS[key]
        self._attr_unique_id = f"{coordinator.ip}_{key}"  # unique & never changes

    @property
    def name(self) -> str | None:
        """The name of the sensor."""
        return f"{DEVICE_NAME} {self._description['name']}"

    @property
    def icon(self) -> str | None:
        """Icon of the sensor."""
        return self._description.get("icon")

    @property
    def device_class(self) -> str | None:
        """Device class of the sensor."""
        return self._description.get("device_class")

    @property
    def unit_of_measurement(self) -> str | None:
        """Device class of the sensor."""
        return self._description.get("unit_of_measurement")

    @property
    def state_class(self) -> str | None:
        """State class of the sensor."""
        return self._description.get("state_class")

    @property
    def state(self) -> str:
        """State of the EH800 sensor."""
        return self._value

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        confentry = self.coordinator.config_entry
        if confentry:
            return DeviceInfo(
                identifiers={(DOMAIN, confentry.entry_id)},
                name=DEVICE_NAME,
                manufacturer="Jari Kaipio",
                model=DEVICE_NAME,
                configuration_url=f"http://{self.coordinator.ip}/",
                entry_type=DeviceEntryType.SERVICE,
            )
        return None

    async def async_added_to_hass(self) -> None:
        """Add the sensor to a logical EH800 device."""
        _LOGGER.debug("sensor.py async_added_to_hass launched")
        # Tell the coordinator to call our _handle_coordinator_update whenever
        # it publishes new data.
        self.async_on_remove(
            self.coordinator.async_add_listener(
                self._handle_coordinator_update, self._context
            )
        )
        # Immediately write the state so that the UI is updated at least once.
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update data when the coordinator publishes a new payload."""
        # Convert the status that the coordinator sent into the entity state.
        self._value = self.coordinator.data[self.key]
        # Update the “available” flag if the payload for this port exists.
        self._attr_available = self.state is not None
        _LOGGER.debug(
            "Sensors _handle_coordinator_update called, %s values: %s",
            self.name,
            self.coordinator.data[self.key],
        )

        self.force_update = True
        self.async_write_ha_state()
