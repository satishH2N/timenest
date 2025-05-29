from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
import uuid

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
    resource_id: str
    start: datetime
    end: datetime
    user_id: str

