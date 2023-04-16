"""Adhan client Coordinator"""

from homeassistant.core import HomeAssistant

import adhan


class AdhanCoordinator:
    """Adhan Coordinator"""

    def __init__(self, hass: HomeAssistant, lat: float, lon: float) -> None:
        self._hass = hass
        self._client = adhan.Client(latitude=lat, longitude=lon)

        self.timings: adhan.Prayer

    async def fetch_timings(self):
        """Fetch the adahn times for the day"""
        self.timings = await self._hass.async_add_executor_job(self._client.get_day)
