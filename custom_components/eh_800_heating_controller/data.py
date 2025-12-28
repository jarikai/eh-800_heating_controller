"""Custom types for eh-800_heating_controller."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import OumanEH800ApiClient
    from .coordinator import EH800Coordinator


type EH800ConfigEntry = ConfigEntry[EH800Data]


@dataclass
class EH800Data:
    """Data for the EH800 integration."""

    client: OumanEH800ApiClient
    coordinator: EH800Coordinator
    integration: Integration
