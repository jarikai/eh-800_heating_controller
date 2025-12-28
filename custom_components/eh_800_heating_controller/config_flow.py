"""Adds config flow for Blueprint."""

from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
)
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from slugify import slugify

from .api import (
    OumanEH800ApiClient,
    OumanEH800ApiClientAuthenticationError,
    OumanEH800ApiClientCommunicationError,
    OumanEH800ApiClientError,
)
from .const import (
    CONF_IP,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    LOGGER,
    SENSOR_DESCRIPTIONS,
)

_LOGGER = logging.getLogger(__name__)


class OumanEH800FlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for OumanEH800."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    ip=user_input[CONF_IP],
                    username=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD],
                )
            except OumanEH800ApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except OumanEH800ApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except OumanEH800ApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(unique_id=slugify(user_input[CONF_IP]))
                self._abort_if_unique_id_configured()
                # Add update_interval to the data
                user_input[CONF_SCAN_INTERVAL] = user_input.get(CONF_SCAN_INTERVAL, 5)
                return self.async_create_entry(
                    title=user_input[CONF_IP],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_IP,
                        default=(user_input or {}).get(CONF_IP, ""),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.URL,
                        ),
                    ),
                    vol.Required(
                        CONF_USERNAME,
                        default=(user_input or {}).get(CONF_USERNAME, ""),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Required(CONF_PASSWORD, default=""): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD,
                        ),
                    ),
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=(user_input or {}).get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=1,
                            max=60,
                            step=1,
                            unit_of_measurement="minutes",
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle reconfiguration of the integration."""
        # Get the config entry from the context
        config_key = self.context.get("entry_id")
        if config_key is None:
            return self.async_abort(reason="missing_config_entry")

        config_entry = self.hass.config_entries.async_get_entry(config_key)
        if config_entry is None:
            return self.async_abort(reason="invalid_config_entry")
        self.config_entry = config_entry

        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    ip=user_input[CONF_IP],
                    username=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD],
                )
            except OumanEH800ApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except OumanEH800ApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except OumanEH800ApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                # Update the config entry with new data
                updated_data = {**self.config_entry.data, **user_input}
                self.hass.config_entries.async_update_entry(
                    self.config_entry, data=updated_data
                )
                await self.hass.config_entries.async_reload(self.config_entry.entry_id)
                return self.async_abort(reason="reconfigure_successful")

        # Pre-fill the form with existing data
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_IP,
                        default=self.config_entry.data.get(CONF_IP, ""),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.URL,
                        ),
                    ),
                    vol.Optional(
                        CONF_USERNAME,
                        default=self.config_entry.data.get(CONF_USERNAME, ""),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Optional(CONF_PASSWORD, default=""): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD,
                        ),
                    ),
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.data.get(CONF_SCAN_INTERVAL, 5),
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=1,
                            max=60,
                            step=1,
                            unit_of_measurement="minutes",
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_credentials(self, ip: str, username: str, password: str) -> None:
        """Validate credentials."""
        client = OumanEH800ApiClient(
            ip=ip,
            username=username,
            password=password,
            session=async_create_clientsession(self.hass),
            hass=self.hass,
        )
        keys = list(SENSOR_DESCRIPTIONS.keys())
        await client.fetch_all(session=async_create_clientsession(self.hass), keys=keys)
