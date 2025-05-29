from __future__ import annotations
from typing import Dict, List

from .models import Tenant, Resource, Appointment


class Storage:
    """Simple in-memory storage used for initial development."""

    def __init__(self) -> None:
        self.tenants: Dict[str, Tenant] = {}
        self.resources: Dict[str, Resource] = {}
        self.appointments: Dict[str, Appointment] = {}

    # Tenant operations
    def add_tenant(self, tenant: Tenant) -> None:
        self.tenants[tenant.id] = tenant

    def get_tenant(self, tenant_id: str) -> Tenant | None:
        return self.tenants.get(tenant_id)

    # Resource operations
    def add_resource(self, resource: Resource) -> None:
        self.resources[resource.id] = resource

    def list_resources(self, tenant_id: str) -> List[Resource]:
        return [r for r in self.resources.values() if r.tenant_id == tenant_id]

    # Appointment operations
    def add_appointment(self, appt: Appointment) -> None:
        self.appointments[appt.id] = appt

    def list_appointments(self, tenant_id: str, resource_id: str) -> List[Appointment]:
        return [
            a
            for a in self.appointments.values()
            if a.tenant_id == tenant_id and a.resource_id == resource_id
        ]
