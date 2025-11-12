import httpx
import time

from .errors import APIError
from .errors import RateLimitError
from .errors import AuthError

DEFAULT_TIMEOUT = httpx.Timeout(10.0, connect=5.0)

class Transport:
    """Handles HTTP requests and responses."""
    def __init__(self, base_url: str, headers: dict[str, str], timeout: httpx.Timeout | None = None):
        self._client = httpx.Client(base_url=base_url, headers=headers, timeout=timeout or DEFAULT_TIMEOUT)

    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        backoff = 0.25
        for attempt in range(5):
            resp = self._client.request(method, url, **kwargs)
            if resp.status_code in (429, 500, 502, 503, 504) and attempt < 4:
                time.sleep(backoff)
                backoff *= 2
                continue
            return self._handle(resp)
         #  after retries, handle the last response
        assert resp is not None
        return self._handle(resp)

    def _handle(self, resp: httpx.Response) -> httpx.Response:
        if 200 <= resp.status_code < 300:
            return resp
        try:
            data = resp.json()
        except Exception:
            data = None
        code = (data or {}).get("error", {}).get("code")
        message = (data or {}).get("error", {}).get("message", resp.text)
        req_id = resp.headers.get("x-request-id")
        if resp.status_code == 401:
            raise AuthError(resp.status_code, code, message, request_id=req_id)
        if resp.status_code == 429:
            raise RateLimitError(resp.status_code, code, message, request_id=req_id)
        raise APIError(resp.status_code, code, message, request_id=req_id)

    def close(self):
        """Close the HTTP client."""
        self._client.close()
