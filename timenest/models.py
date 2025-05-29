from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class Tenant:
    name: str
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class Resource:
    tenant_id: str
    name: str
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class Appointment:
    tenant_id: str
    resource_id: str
    start: datetime
    end: datetime
    user_email: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid4()))
