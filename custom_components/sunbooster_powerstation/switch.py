"""Switch entities (AC/DC/USB)."""
from __future__ import annotations
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, PROP_AC_SWITCH, PROP_DC_SWITCH, PROP_USB_SWITCH
from .entity import SunboosterEntity

SWITCHES = (
    (PROP_AC_SWITCH, "AC-Ausgang"),
    (PROP_DC_SWITCH, "DC-Ausgang"),
    (PROP_USB_SWITCH, "USB-Ausgang"),
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    bundle = hass.data[DOMAIN][entry.entry_id]
    coord = bundle["coordinator"]
    api = bundle["api"]
    device_key = bundle["meta"].get("device_key","unknown")
    async_add_entities([SunboosterSwitch(coord, api, device_key, code, name) for code, name in SWITCHES])


class SunboosterSwitch(SunboosterEntity, SwitchEntity):
    def __init__(self, coordinator, api, device_key, code, name):
        super().__init__(coordinator, device_key)
        self._api = api
        self._code = code
        self._attr_name = name
        self._attr_unique_id = f"sunbooster_{device_key}_{code}"

    @property
    def is_on(self):
        v = (self.coordinator.data or {}).get(self._code)
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower() in ("true","1","on")
        return bool(v) if v is not None else None

    async def async_turn_on(self, **kwargs):
        await self._api.write(self._code, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self._api.write(self._code, False)
        await self.coordinator.async_request_refresh()
