from datetime import datetime, timedelta

from timenest.services import BookingService


def test_successful_booking():
    service = BookingService()
    tenant = service.add_tenant("Acme")
    resource = service.add_resource(tenant.id, "Room 1")
    start = datetime.now()
    end = start + timedelta(hours=1)
    appt = service.book(resource.id, start, end, "user1")
    assert appt in service.list_appointments(resource.id)


def test_conflicting_booking():
    service = BookingService()
    tenant = service.add_tenant("Acme")
    resource = service.add_resource(tenant.id, "Room 1")
    start = datetime.now()
    end = start + timedelta(hours=1)
    service.book(resource.id, start, end, "user1")
    try:
        service.book(resource.id, start + timedelta(minutes=30), end + timedelta(minutes=30), "user2")
        assert False, "Expected ValueError"
    except ValueError:
        pass
