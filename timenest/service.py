from datetime import datetime

from .models import Tenant, Resource, Appointment
from .storage import Storage


class BookingError(Exception):
    pass


def create_tenant(store: Storage, name: str) -> Tenant:
    tenant = Tenant(name=name)
    store.add_tenant(tenant)
    return tenant


def create_resource(store: Storage, tenant_id: str, name: str) -> Resource:
    if not store.get_tenant(tenant_id):
        raise BookingError("tenant not found")
    resource = Resource(tenant_id=tenant_id, name=name)
    store.add_resource(resource)
    return resource


def create_appointment(
    store: Storage,
    tenant_id: str,
    resource_id: str,
    start: datetime,
    end: datetime,
    user_email: str | None = None,
) -> Appointment:
    if start >= end:
        raise BookingError("invalid time range")
    # ensure tenant and resource exist
    if not store.get_tenant(tenant_id):
        raise BookingError("tenant not found")
    resources = store.list_resources(tenant_id)
    if not any(r.id == resource_id for r in resources):
        raise BookingError("resource not found")

    # check for overlap
    for existing in store.list_appointments(tenant_id, resource_id):
        if not (end <= existing.start or start >= existing.end):
            raise BookingError("timeslot unavailable")

    appt = Appointment(
        tenant_id=tenant_id,
        resource_id=resource_id,
        start=start,
        end=end,
        user_email=user_email,
    )
    store.add_appointment(appt)
    return appt
