"""Base entity for Sunbooster Powerstation."""
from __future__ import annotations
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN
from .coordinator import SunboosterCoordinator


class SunboosterEntity(CoordinatorEntity[SunboosterCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coordinator: SunboosterCoordinator, device_key: str):
        super().__init__(coordinator)
        self._device_key = device_key

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_key)},
            name=f"Sunbooster Powerstation {self._device_key}",
            manufacturer="Sunbooster",
            model="Powerstation (Acceleronix)",
            sw_version="1.0.0",
        )
