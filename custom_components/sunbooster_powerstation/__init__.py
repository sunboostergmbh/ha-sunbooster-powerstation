"""The Sunbooster Powerstation integration."""
from __future__ import annotations
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SunboosterApi, SunboosterAuthError
from .const import DOMAIN, CONF_PROXY_URL, CONF_CUSTOMER_KEY, CONF_SCAN_INTERVAL, DEFAULT_PROXY_URL, DEFAULT_SCAN_INTERVAL
from .coordinator import SunboosterCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR, Platform.NUMBER, Platform.SELECT, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    proxy_url = entry.data.get(CONF_PROXY_URL, DEFAULT_PROXY_URL)
    customer_key = entry.data[CONF_CUSTOMER_KEY]
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))

    session = async_get_clientsession(hass)
    api = SunboosterApi(session, proxy_url, customer_key)

    try:
        meta = await api.verify()
    except SunboosterAuthError as e:
        _LOGGER.error("Auth failed: %s", e)
        return False
    _LOGGER.info("Sunbooster verified for device %s", meta.get("device_key"))

    coordinator = SunboosterCoordinator(hass, api, scan_interval)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
        "meta": meta,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
