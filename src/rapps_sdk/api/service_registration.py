from typing import List
from ..transport import Transport
from ..models.registration import ServiceInfo, RegisteredService

# to be replaced with the real Non-RT RIC path when given.
REGISTRY_BASE = "/registry/v1/services"

class Registration:
    """Service Registration & Discovery API."""

    def __init__(self, transport: Transport):
        self._t = transport

    def register(self, info: ServiceInfo) -> RegisteredService:
        payload = info.model_dump(by_alias=True, mode="json")
        resp = self._t.request("POST", REGISTRY_BASE, json=payload)
        return RegisteredService.model_validate(resp.json())

    def get(self, service_id: str) -> RegisteredService:
        resp = self._t.request("GET", f"{REGISTRY_BASE}/{service_id}")
        return RegisteredService.model_validate(resp.json())

    def list(self) -> List[RegisteredService]:
        resp = self._t.request("GET", REGISTRY_BASE)
        return [RegisteredService.model_validate(i) for i in resp.json()]

    def deregister(self, service_id: str) -> None:
        self._t.request("DELETE", f"{REGISTRY_BASE}/{service_id}")
