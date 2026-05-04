"""Number entities (charge power setpoint)."""
from __future__ import annotations
import logging
from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, PROP_CHARGE_POWER, PROP_MIG_CONNECTION, MIG_WATT_TO_ENUM, MIG_ENUM_TO_WATT
from .entity import SunboosterEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    bundle = hass.data[DOMAIN][entry.entry_id]
    coord = bundle["coordinator"]
    api = bundle["api"]
    device_key = bundle["meta"].get("device_key", "unknown")
    async_add_entities([
        ChargePowerSetpoint(coord, api, device_key),
        GridFeedInPowerSetpoint(coord, api, device_key),
    ])


class ChargePowerSetpoint(SunboosterEntity, NumberEntity):
    _attr_name = "Max. Ladeleistung"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_native_min_value = 0
    _attr_native_max_value = 1600
    _attr_native_step = 50
    _attr_mode = NumberMode.SLIDER

    def __init__(self, coordinator, api, device_key):
        super().__init__(coordinator, device_key)
        self._api = api
        self._attr_unique_id = f"sunbooster_{device_key}_charge_power_setpoint"

    @property
    def native_value(self):
        v = (self.coordinator.data or {}).get(PROP_CHARGE_POWER)
        try:
            return round(float(v))
        except (TypeError, ValueError):
            return None

    async def async_set_native_value(self, value: float) -> None:
        watts = max(0, min(1600, round(value)))
        await self._api.write(PROP_CHARGE_POWER, watts)
        await self.coordinator.async_request_refresh()


class GridFeedInPowerSetpoint(SunboosterEntity, NumberEntity):
    _attr_name = "Netz-Einspeisung max (MIG)"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_native_min_value = 0
    _attr_native_max_value = 800
    _attr_native_step = 100  # Acceleronix MIG enum is defined in 50W steps from 100W up; use 100 step to avoid landing on the unmapped 50W slot.
    _attr_mode = NumberMode.SLIDER

    def __init__(self, coordinator, api, device_key):
        super().__init__(coordinator, device_key)
        self._api = api
        self._attr_unique_id = f"sunbooster_{device_key}_mig_power_setpoint"

    @property
    def native_value(self):
        e = (self.coordinator.data or {}).get(PROP_MIG_CONNECTION)
        if e is None:
            return None
        return MIG_ENUM_TO_WATT.get(str(e))

    async def async_set_native_value(self, value: float) -> None:
        # Snap to nearest 50W
        requested = max(0, min(800, round(value)))
        # Acceleronix only accepts a discrete set of grid feed-in steps. If the
        # caller landed between two valid steps (e.g. 50 W from a slider with a
        # finer step), snap to the closest mapped value instead of dropping the
        # write with a warning. This makes the entity tolerant to UI rounding
        # and to any future MIG_WATT_TO_ENUM additions.
        valid_watts = sorted(MIG_WATT_TO_ENUM.keys())
        watts = min(valid_watts, key=lambda w: abs(w - requested))
        if watts != requested:
            _LOGGER.debug(
                "Snapped MIG setpoint %sW to nearest supported value %sW",
                requested, watts,
            )
        enum_val = MIG_WATT_TO_ENUM[watts]
        await self._api.write(PROP_MIG_CONNECTION, enum_val)
        await self.coordinator.async_request_refresh()
