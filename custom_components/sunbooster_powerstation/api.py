"""Sunbooster Proxy API client."""
from __future__ import annotations
import logging
from typing import Any
import aiohttp

_LOGGER = logging.getLogger(__name__)


class SunboosterApiError(Exception):
    pass


class SunboosterAuthError(SunboosterApiError):
    pass


class SunboosterApi:
    def __init__(self, session: aiohttp.ClientSession, proxy_url: str, customer_key: str):
        self._session = session
        self._base = proxy_url.rstrip("/")
        self._key = customer_key

    @property
    def _headers(self) -> dict[str, str]:
        return {"X-Sunbooster-Key": self._key, "User-Agent": "sunbooster-ha/1.0"}

    async def verify(self) -> dict:
        url = f"{self._base}/v1/auth/verify"
        async with self._session.get(url, headers=self._headers, timeout=aiohttp.ClientTimeout(total=15)) as r:
            data = await r.json(content_type=None)
            if r.status == 401:
                raise SunboosterAuthError(data.get("detail", "Invalid key"))
            if r.status >= 400:
                raise SunboosterApiError(f"Verify failed: {r.status} {data}")
            return data

    async def get_status(self, lookback_minutes: int = 30) -> dict:
        url = f"{self._base}/v1/device/status"
        async with self._session.get(
            url,
            headers=self._headers,
            params={"lookback_minutes": lookback_minutes},
            timeout=aiohttp.ClientTimeout(total=20),
        ) as r:
            data = await r.json(content_type=None)
            if r.status == 401:
                raise SunboosterAuthError(data.get("detail", "Unauthorized"))
            if r.status >= 400:
                raise SunboosterApiError(f"Status failed: {r.status} {data}")
            return data.get("state", {}) or {}

    async def write(self, code: str, value: Any) -> dict:
        url = f"{self._base}/v1/device/write"
        async with self._session.post(
            url, headers=self._headers, json={"code": code, "value": value},
            timeout=aiohttp.ClientTimeout(total=20),
        ) as r:
            data = await r.json(content_type=None)
            if r.status >= 400:
                raise SunboosterApiError(f"Write failed: {r.status} {data}")
            return data

    async def write_many(self, properties: dict[str, Any]) -> dict:
        url = f"{self._base}/v1/device/write_many"
        async with self._session.post(
            url, headers=self._headers, json={"properties": properties},
            timeout=aiohttp.ClientTimeout(total=20),
        ) as r:
            data = await r.json(content_type=None)
            if r.status >= 400:
                raise SunboosterApiError(f"WriteMany failed: {r.status} {data}")
            return data
