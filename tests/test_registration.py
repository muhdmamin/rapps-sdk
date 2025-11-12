import httpx
import respx

from rapps_sdk import Client, ApiKey
from rapps_sdk.models.registration import ServiceInfo

BASE = "https://nonrtric.example.com"
REG = "/registry/v1/services"

@respx.mock
def test_register_get_list_delete():
    # POST /services
    respx.post(f"{BASE}{REG}").mock(
        return_value=httpx.Response(
            201,
            json={
                "id": "svc_123",
                "serviceName": "example_rapp",
                "serviceType": "rApp",
                "callbackUri": "https://myapp.example.com/callback",
                "description": "demo",
            },
        )
    )

    # GET /services/svc_123
    respx.get(f"{BASE}{REG}/svc_123").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "svc_123",
                "serviceName": "example_rapp",
                "serviceType": "rApp",
                "callbackUri": "https://myapp.example.com/callback",
                "description": "demo",
            },
        )
    )

    # GET /services
    respx.get(f"{BASE}{REG}").mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "id": "svc_123",
                    "serviceName": "example_rapp",
                    "serviceType": "rApp",
                    "callbackUri": "https://myapp.example.com/callback",
                    "description": "demo",
                }
            ],
        )
    )

    # DELETE /services/svc_123
    respx.delete(f"{BASE}{REG}/svc_123").mock(return_value=httpx.Response(204))

    with Client(BASE, ApiKey("demo-key")) as c:
        info = ServiceInfo(
            serviceName="example_rapp",
            serviceType="rApp",
            callbackUri="https://myapp.example.com/callback",
            description="demo",
        )

        created = c.api.registration.register(info)
        assert created.id == "svc_123"

        fetched = c.api.registration.get(created.id)
        assert fetched.service_name == "example_rapp"

        listed = c.api.registration.list()
        assert any(s.id == "svc_123" for s in listed)

        # should not raise
        c.api.registration.deregister("svc_123")
