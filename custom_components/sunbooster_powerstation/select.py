"""Select entity (charge mode)."""
from __future__ import annotations
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, PROP_CHARGE_MODE, CHARGE_MODE_LABELS
from .entity import SunboosterEntity

LABEL_TO_VAL = {v: k for k, v in CHARGE_MODE_LABELS.items()}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    bundle = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ChargeModeSelect(bundle["coordinator"], bundle["api"], bundle["meta"].get("device_key","unknown"))])


class ChargeModeSelect(SunboosterEntity, SelectEntity):
    _attr_name = "Lademodus"
    _attr_options = list(CHARGE_MODE_LABELS.values())

    def __init__(self, coordinator, api, device_key):
        super().__init__(coordinator, device_key)
        self._api = api
        self._attr_unique_id = f"sunbooster_{device_key}_charge_mode_select"

    @property
    def current_option(self):
        v = (self.coordinator.data or {}).get(PROP_CHARGE_MODE)
        return CHARGE_MODE_LABELS.get(str(v))

    async def async_select_option(self, option: str) -> None:
        val = LABEL_TO_VAL.get(option)
        if val is None:
            return
        await self._api.write(PROP_CHARGE_MODE, val)
        await self.coordinator.async_request_refresh()
