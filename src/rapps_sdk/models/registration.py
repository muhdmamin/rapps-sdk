from typing import Optional
from pydantic import BaseModel, Field, HttpUrl

class ServiceInfo(BaseModel):
    service_name: str = Field(..., alias="serviceName")
    service_type: str = Field(..., alias="serviceType") 
    callback_uri: HttpUrl = Field(..., alias="callbackUri")
    description: Optional[str] = None

class RegisteredService(ServiceInfo):
    id: str
