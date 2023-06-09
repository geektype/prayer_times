"""The Prayer Times integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .coordinator import AdhanCoordinator


from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Prayer Times from a config entry."""

    # hass.data.setdefault(DOMAIN, {})
    _LOGGER.info("Setting up Adhan API client")
    coordinator = AdhanCoordinator(hass, hass.config.latitude, hass.config.longitude)
    hass.data[DOMAIN] = coordinator
    await hass.data[DOMAIN].fetch_timings()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data.pop(DOMAIN)

    return unload_ok
