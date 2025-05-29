from dataclasses import dataclass
from datetime import datetime


@dataclass
class Tenant:
    id: str
    name: str


@dataclass
class Resource:
    id: str
    tenant_id: str
    name: str


@dataclass
class Appointment:
    id: str
    tenant_id: str
    resource_id: str
    start: datetime
    end: datetime
    user_email: str
