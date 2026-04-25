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
        GridChargePowerSetpoint(coord, api, device_key),
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


class GridChargePowerSetpoint(SunboosterEntity, NumberEntity):
    _attr_name = "Netz-Ladeleistung (MIG)"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_native_min_value = 0
    _attr_native_max_value = 800
    _attr_native_step = 50
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
        watts = max(0, min(800, int(round(value / 50.0)) * 50))
        enum_val = MIG_WATT_TO_ENUM.get(watts)
        if enum_val is None:
            _LOGGER.warning("No MIG enum mapping for %sW", watts)
            return
        await self._api.write(PROP_MIG_CONNECTION, enum_val)
        await self.coordinator.async_request_refresh()
