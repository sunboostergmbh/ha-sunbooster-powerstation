"""Sensors for Sunbooster Powerstation."""
from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Callable
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower, UnitOfTime, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, PROP_BATTERY, PROP_TOTAL_INPUT, PROP_TOTAL_OUTPUT, PROP_AC_OUTPUT, PROP_DC_OUTPUT, PROP_USB_OUTPUT, PROP_CHARGE_POWER, PROP_REMAIN_TIME, PROP_REMAIN_CHARGE_TIME, PROP_DEVICE_STATUS, CHARGE_MODE_LABELS, PROP_CHARGE_MODE
from .entity import SunboosterEntity


@dataclass(frozen=True)
class SBSensorDesc(SensorEntityDescription):
    convert: Callable | None = None


def _to_int(v):
    try:
        return int(v)
    except Exception:
        try:
            return int(float(v))
        except Exception:
            return None


def _to_float(v):
    try:
        return float(v)
    except Exception:
        return None


def _device_status_text(v):
    m = {"0": "standby", "1": "discharging", "2": "charging", "3": "fault"}
    return m.get(str(v), str(v) if v is not None else None)


def _charge_mode_text(v):
    return CHARGE_MODE_LABELS.get(str(v), str(v) if v is not None else None)


SENSORS: tuple[SBSensorDesc, ...] = (
    SBSensorDesc(key=PROP_BATTERY, name="Akku-Stand", native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY, state_class=SensorStateClass.MEASUREMENT, convert=_to_int),
    SBSensorDesc(key=PROP_TOTAL_INPUT, name="Eingangsleistung gesamt", native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER, state_class=SensorStateClass.MEASUREMENT, convert=_to_int),
    SBSensorDesc(key=PROP_TOTAL_OUTPUT, name="Ausgangsleistung gesamt", native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER, state_class=SensorStateClass.MEASUREMENT, convert=_to_int),
    SBSensorDesc(key=PROP_AC_OUTPUT, name="AC-Ausgang", native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER, state_class=SensorStateClass.MEASUREMENT, convert=_to_int),
    SBSensorDesc(key=PROP_DC_OUTPUT, name="DC-Ausgang", native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER, state_class=SensorStateClass.MEASUREMENT, convert=_to_int),
    SBSensorDesc(key=PROP_USB_OUTPUT, name="USB-Ausgang", native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER, state_class=SensorStateClass.MEASUREMENT, convert=_to_int),
    SBSensorDesc(key=PROP_CHARGE_POWER, name="Aktuelle Ladeleistung", native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER, state_class=SensorStateClass.MEASUREMENT, convert=_to_int),
    SBSensorDesc(key=PROP_REMAIN_TIME, name="Verbleibende Zeit (Entladen)", native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT, convert=_to_int),
    SBSensorDesc(key=PROP_REMAIN_CHARGE_TIME, name="Verbleibende Zeit (Laden)", native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT, convert=_to_int),
    SBSensorDesc(key=PROP_DEVICE_STATUS, name="Gerätestatus", convert=_device_status_text),
    SBSensorDesc(key=PROP_CHARGE_MODE, name="Lademodus", convert=_charge_mode_text),
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    bundle = hass.data[DOMAIN][entry.entry_id]
    coord = bundle["coordinator"]
    device_key = bundle["meta"].get("device_key", "unknown")
    async_add_entities(SunboosterSensor(coord, device_key, d) for d in SENSORS)


class SunboosterSensor(SunboosterEntity, SensorEntity):
    entity_description: SBSensorDesc

    def __init__(self, coordinator, device_key, desc: SBSensorDesc):
        super().__init__(coordinator, device_key)
        self.entity_description = desc
        self._attr_unique_id = f"sunbooster_{device_key}_{desc.key}"

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        raw = data.get(self.entity_description.key)
        if raw is None:
            return None
        if self.entity_description.convert:
            return self.entity_description.convert(raw)
        return raw
