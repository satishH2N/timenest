from __future__ import annotations

from datetime import datetime
from typing import Dict, List
import uuid

from .models import Tenant, Resource, Appointment

class BookingService:
    def __init__(self) -> None:
        self.tenants: Dict[str, Tenant] = {}
        self.resources: Dict[str, Resource] = {}
        self.appointments: List[Appointment] = []

    def add_tenant(self, name: str) -> Tenant:
        tenant = Tenant(id=str(uuid.uuid4()), name=name)
        self.tenants[tenant.id] = tenant
        return tenant

    def add_resource(self, tenant_id: str, name: str) -> Resource:
        if tenant_id not in self.tenants:
            raise ValueError("Tenant not found")
        resource = Resource(id=str(uuid.uuid4()), tenant_id=tenant_id, name=name)
        self.resources[resource.id] = resource
        return resource

    def book(self, resource_id: str, start: datetime, end: datetime, user_id: str) -> Appointment:
        if start >= end:
            raise ValueError("Invalid time range")
        for appt in self.appointments:
            if appt.resource_id == resource_id and not (end <= appt.start or start >= appt.end):
                raise ValueError("Slot unavailable")
        appointment = Appointment(
            id=str(uuid.uuid4()),
            resource_id=resource_id,
            start=start,
            end=end,
            user_id=user_id,
        )
        self.appointments.append(appointment)
        return appointment

    def list_appointments(self, resource_id: str) -> List[Appointment]:
        return [a for a in self.appointments if a.resource_id == resource_id]
