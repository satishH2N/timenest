import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime, timedelta

import timenest


def test_create_appointment_success():
    store = timenest.Storage()
    tenant = timenest.create_tenant(store, "Acme")
    resource = timenest.create_resource(store, tenant.id, "Room 1")
    start = datetime.now()
    end = start + timedelta(hours=1)
    appt = timenest.create_appointment(
        store,
        tenant.id,
        resource.id,
        start,
        end,
        "user@example.com",
    )
    assert appt.id in store.appointments


def test_create_appointment_overlap():
    store = timenest.Storage()
    tenant = timenest.create_tenant(store, "Acme")
    resource = timenest.create_resource(store, tenant.id, "Room 1")
    start = datetime.now()
    end = start + timedelta(hours=1)
    timenest.create_appointment(store, tenant.id, resource.id, start, end)
    try:
        timenest.create_appointment(store, tenant.id, resource.id, start, end)
    except timenest.BookingError:
        assert True
    else:
        assert False, "expected BookingError"
