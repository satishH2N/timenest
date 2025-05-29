from datetime import datetime, timedelta

from timenest.models import Tenant, Resource, Appointment
from timenest.service import BookingService


def test_booking_success():
    svc = BookingService()
    tenant = Tenant(id="t1", name="Tenant")
    resource = Resource(id="r1", tenant_id="t1", name="Room")
    svc.add_tenant(tenant)
    svc.add_resource(resource)
    appt = Appointment(
        id="a1",
        tenant_id="t1",
        resource_id="r1",
        start=datetime.now(),
        end=datetime.now() + timedelta(hours=1),
        user_email="a@example.com",
    )
    svc.book_appointment(appt)
    assert len(svc.appointments) == 1


def test_booking_conflict():
    svc = BookingService()
    tenant = Tenant(id="t1", name="Tenant")
    resource = Resource(id="r1", tenant_id="t1", name="Room")
    svc.add_tenant(tenant)
    svc.add_resource(resource)
    now = datetime.now()
    appt1 = Appointment(
        id="a1",
        tenant_id="t1",
        resource_id="r1",
        start=now,
        end=now + timedelta(hours=1),
        user_email="a@example.com",
    )
    svc.book_appointment(appt1)
    appt2 = Appointment(
        id="a2",
        tenant_id="t1",
        resource_id="r1",
        start=now + timedelta(minutes=30),
        end=now + timedelta(hours=1, minutes=30),
        user_email="b@example.com",
    )
    try:
        svc.book_appointment(appt2)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected conflict")
