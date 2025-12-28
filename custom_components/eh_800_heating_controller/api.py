"""Sample API Client."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

import aiohttp

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


_LOGGER = logging.getLogger(__name__)


class OumanEH800ApiClientError(Exception):
    """Exception to indicate a general API error."""


class OumanEH800ApiClientCommunicationError(
    OumanEH800ApiClientError,
):
    """Exception to indicate a communication error."""


class OumanEH800ApiClientAuthenticationError(
    OumanEH800ApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise OumanEH800ApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class OumanEH800ApiClient:
    """Ouman EH800 API Client."""

    def __init__(
        self,
        ip: str,
        username: str,
        password: str,
        session: aiohttp.ClientSession,
        hass: HomeAssistant,
    ) -> None:
        """EH800 API Client."""
        self._ip = ip
        self._username = username
        self._password = password
        self._session = session
        self._hass = hass

    async def fetch_value(self, session: aiohttp.ClientSession, key: str) -> str:
        """Return the raw value of one endpoint."""
        url = f"http://{self._ip}/request?{key}"
        _LOGGER.debug("URL in fetch_value: %s", url)
        for attempt in range(3):
            try:
                async with session.get(
                    url, timeout=aiohttp.ClientTimeout(total=120)
                ) as resp:
                    resp.raise_for_status()
                    return (await resp.text()).strip()
            except aiohttp.ClientConnectionError:
                _LOGGER.warning(
                    "Connection to %s refused, retry %d/2", self.ip, attempt + 1
                )
            await asyncio.sleep(2**attempt)

        _LOGGER.error("Failed to read %s after 3 retries", key)
        return "ERROR"

    async def fetch_all(self, session: aiohttp.ClientSession, keys: list) -> Any:
        """Run all fetches concurrently and return a dict {key: value}."""
        results = {}
        for key in keys:
            value = await self.fetch_value(key=key, session=session)
            replase_str: str = "request?" + key
            result_r = str(value).replace(replase_str, "")
            result_r = result_r.replace(";", "")
            result_r = result_r.replace("=", "")
            result_r = result_r.replace("\x00", "")
            results[key] = result_r
            _LOGGER.debug("Value: %s : %s", key, result_r)
            # Optional: give the device a tiny break
            await asyncio.sleep(0.1)
        return results

    @property
    def ip(self) -> str | None:
        """IP address of the client."""
        return self._ip
