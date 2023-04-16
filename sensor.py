"""Platform for calendar integration"""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
)

from .const import DOMAIN
from .coordinator import AdhanCoordinator

from datetime import datetime

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="Fajr",
        name="Fajr",
    ),
    SensorEntityDescription(
        key="Sunrise",
        name="Sunrise",
    ),
    SensorEntityDescription(
        key="Dhuhr",
        name="Dhuhr",
    ),
    SensorEntityDescription(
        key="Asr",
        name="Asr",
    ),
    SensorEntityDescription(
        key="Maghrib",
        name="Maghrib",
    ),
    SensorEntityDescription(
        key="Isha",
        name="Isha",
    ),
    SensorEntityDescription(
        key="Midnight",
        name="Midnight",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup prayer time sensors"""
    coordinator: AdhanCoordinator = hass.data[DOMAIN]
    async_add_entities(PrayerTime(coordinator, desc) for desc in SENSOR_TYPES)


class PrayerTime(SensorEntity):
    """Representation of a prayer time event"""

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: AdhanCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the Prayer Time sensor."""
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = description.key

    @property
    def native_value(self) -> datetime:
        """Return the state of the sensor."""
        return getattr(self.coordinator.timings.timings, self.entity_description.key)
