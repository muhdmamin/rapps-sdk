from typing import Mapping
from .auth import Auth
from .transport import Transport 
from .api import Registration

class Client:
    """Main SDK entry point."""
    def __init__(self, base_url: str, auth: Auth, *, default_headers: Mapping[str, str] | None = None):
        headers = {"User-Agent": "rapps-sdk/0.1.0", **(default_headers or {}), **auth.auth_headers()}

        # transport creation
        self._transport: Transport = Transport(base_url=base_url, headers=headers)

        # set resources that depend on it
        self.api = type("ApiNamespace", (), {})()
        self.api.registration = Registration(self._transport)

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *exc) -> None:
        self.close()
