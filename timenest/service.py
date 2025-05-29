from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

from .models import Tenant, Resource, Appointment


@dataclass
class BookingService:
    tenants: Dict[str, Tenant] = field(default_factory=dict)
    resources: Dict[str, Resource] = field(default_factory=dict)
    appointments: List[Appointment] = field(default_factory=list)

    def add_tenant(self, tenant: Tenant) -> None:
        if tenant.id in self.tenants:
            raise ValueError(f"Tenant {tenant.id} already exists")
        self.tenants[tenant.id] = tenant

    def add_resource(self, resource: Resource) -> None:
        if resource.id in self.resources:
            raise ValueError(f"Resource {resource.id} already exists")
        if resource.tenant_id not in self.tenants:
            raise ValueError("Tenant does not exist")
        self.resources[resource.id] = resource

    def book_appointment(self, appt: Appointment) -> None:
        if appt.tenant_id not in self.tenants:
            raise ValueError("Tenant does not exist")
        if appt.resource_id not in self.resources:
            raise ValueError("Resource does not exist")
        for existing in self.appointments:
            if (
                existing.tenant_id == appt.tenant_id
                and existing.resource_id == appt.resource_id
                and not (appt.end <= existing.start or appt.start >= existing.end)
            ):
                raise ValueError("Conflicting appointment")
        self.appointments.append(appt)

    def find_appointments(self, tenant_id: str, resource_id: str) -> List[Appointment]:
        return [
            a
            for a in self.appointments
            if a.tenant_id == tenant_id and a.resource_id == resource_id
        ]
