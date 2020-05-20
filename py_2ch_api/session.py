from json import JSONDecodeError
from typing import Optional, Dict
from addict import Dict as JSON_Parse
from urllib.parse import urljoin

import requests

from py_2ch_api.exceptions import RequestError


class GenericRequestProvider:
    def __init__(self, base_url: str = "https://2ch.hk", proxies: Dict = None):
        self._base_url = base_url
        self._session = requests.Session()
        self._proxies = proxies

        if self._proxies:
            self._session.proxies.update(self._proxies)

    def __enter__(self):
        if not self._session:
            self._session = requests.Session()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def _request(
        self,
        method: str = None,
        path: str = None,
        extra_headers: Optional[Dict] = None,
        extra_params: Optional[Dict] = None,
        status_code: int = 200,
        **kwargs
    ):
        url = urljoin(self._base_url, path.lstrip("/"))

        headers = kwargs.pop("headers", {})

        headers.update(extra_headers or {})

        headers[
            "User-agent"
        ] = "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0"

        params = kwargs.pop("params", {})
        params.update(extra_params or {})

        timeout = kwargs.pop("timeout", 20)

        r = self._session.request(
            method,
            url,
            headers=headers,
            params=params,
            timeout=timeout,
            **kwargs
        )

        if r.status_code != status_code:
            raise RequestError(r, status_code)

        try:
            return JSON_Parse(r.json())
        except JSONDecodeError:
            return r

    def build_url(self, path: str = None) -> str:
        return urljoin(self._base_url, path.lstrip("/"))

    def get(self, path, **kwargs):
        return self._request("get", path, **kwargs)

    def post(self, path, **kwargs):
        return self._request("post", path, **kwargs)

    def put(self, path, **kwargs):
        return self._request("put", path, **kwargs)

    def patch(self, path, **kwargs):
        return self._request("patch", path, **kwargs)

    def delete(self, path, **kwargs):
        return self._request("delete", path, **kwargs)
