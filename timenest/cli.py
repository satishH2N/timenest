import argparse
from datetime import datetime
import uuid

from .models import Tenant, Resource, Appointment
from .service import BookingService


def main(argv=None):
    parser = argparse.ArgumentParser(description="TimeNest CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    tenant_p = sub.add_parser("add-tenant")
    tenant_p.add_argument("name")

    resource_p = sub.add_parser("add-resource")
    resource_p.add_argument("tenant_id")
    resource_p.add_argument("name")

    book_p = sub.add_parser("book")
    book_p.add_argument("tenant_id")
    book_p.add_argument("resource_id")
    book_p.add_argument("start")
    book_p.add_argument("end")
    book_p.add_argument("email")

    args = parser.parse_args(argv)
    service = BookingService()

    if args.cmd == "add-tenant":
        tenant = Tenant(id=str(uuid.uuid4()), name=args.name)
        service.add_tenant(tenant)
        print(f"Added tenant {tenant}")
    elif args.cmd == "add-resource":
        resource = Resource(
            id=str(uuid.uuid4()), tenant_id=args.tenant_id, name=args.name
        )
        service.add_resource(resource)
        print(f"Added resource {resource}")
    elif args.cmd == "book":
        appt = Appointment(
            id=str(uuid.uuid4()),
            tenant_id=args.tenant_id,
            resource_id=args.resource_id,
            start=datetime.fromisoformat(args.start),
            end=datetime.fromisoformat(args.end),
            user_email=args.email,
        )
        service.book_appointment(appt)
        print(f"Booked {appt}")


if __name__ == "__main__":
    main()
