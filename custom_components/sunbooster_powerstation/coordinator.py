"""DataUpdateCoordinator for Sunbooster Powerstation."""
from __future__ import annotations
import logging
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .api import SunboosterApi, SunboosterApiError, SunboosterAuthError

_LOGGER = logging.getLogger(__name__)


class SunboosterCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, api: SunboosterApi, scan_interval: int = 30):
        super().__init__(
            hass, _LOGGER, name="sunbooster_powerstation",
            update_interval=timedelta(seconds=scan_interval),
        )
        self.api = api

    async def _async_update_data(self):
        try:
            return await self.api.get_status(lookback_minutes=30)
        except SunboosterAuthError as e:
            raise UpdateFailed(f"Auth error: {e}") from e
        except SunboosterApiError as e:
            raise UpdateFailed(f"API error: {e}") from e
