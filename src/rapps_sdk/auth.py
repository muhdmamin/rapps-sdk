from typing import Mapping

class Auth:
    """Base class for authentication handlers."""
    def auth_headers(self) -> Mapping[str, str]:
        return {}

class ApiKey(Auth):
    """Simple API key authentication."""
    def __init__(self, key: str, header: str = "Authorization", prefix: str = "Bearer"):
        self.key, self.header, self.prefix = key, header, prefix

    def auth_headers(self) -> Mapping[str, str]:
        return {self.header: f"{self.prefix} {self.key}"}
