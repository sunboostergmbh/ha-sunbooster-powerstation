"""Config flow for Sunbooster Powerstation."""
from __future__ import annotations
import logging
from typing import Any
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigEntry, OptionsFlow
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SunboosterApi, SunboosterAuthError, SunboosterApiError
from .const import (
    DOMAIN, CONF_PROXY_URL, CONF_CUSTOMER_KEY, CONF_SCAN_INTERVAL,
    DEFAULT_PROXY_URL, DEFAULT_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class SunboosterConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            session = async_get_clientsession(self.hass)
            api = SunboosterApi(session, user_input[CONF_PROXY_URL], user_input[CONF_CUSTOMER_KEY])
            try:
                meta = await api.verify()
            except SunboosterAuthError:
                errors["base"] = "invalid_key"
            except SunboosterApiError as e:
                _LOGGER.error("Setup error: %s", e)
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(f"sunbooster_{meta.get('device_key')}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"Sunbooster {meta.get('device_key', 'Powerstation')}",
                    data=user_input,
                )

        schema = vol.Schema({
            vol.Required(CONF_CUSTOMER_KEY): str,
            vol.Required(CONF_PROXY_URL, default=DEFAULT_PROXY_URL): str,
            vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(entry: ConfigEntry) -> OptionsFlow:
        return SunboosterOptionsFlow(entry)


class SunboosterOptionsFlow(OptionsFlow):
    def __init__(self, entry: ConfigEntry) -> None:
        self.entry = entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        cur = self.entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        schema = vol.Schema({vol.Optional(CONF_SCAN_INTERVAL, default=cur): int})
        return self.async_show_form(step_id="init", data_schema=schema)
