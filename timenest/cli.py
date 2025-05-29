import argparse
from datetime import datetime

from .storage import Storage
from .service import (
    create_tenant,
    create_resource,
    create_appointment,
    BookingError,
)

store = Storage()


def main() -> None:
    parser = argparse.ArgumentParser(description="TimeNest CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    tenant_p = sub.add_parser("create-tenant")
    tenant_p.add_argument("name")

    res_p = sub.add_parser("create-resource")
    res_p.add_argument("tenant_id")
    res_p.add_argument("name")

    appt_p = sub.add_parser("create-appointment")
    appt_p.add_argument("tenant_id")
    appt_p.add_argument("resource_id")
    appt_p.add_argument("start")
    appt_p.add_argument("end")
    appt_p.add_argument("user_email")

    args = parser.parse_args()

    try:
        if args.cmd == "create-tenant":
            tenant = create_tenant(store, args.name)
            print(f"tenant {tenant.id} created")
        elif args.cmd == "create-resource":
            res = create_resource(store, args.tenant_id, args.name)
            print(f"resource {res.id} created")
        elif args.cmd == "create-appointment":
            start = datetime.fromisoformat(args.start)
            end = datetime.fromisoformat(args.end)
            appt = create_appointment(
                store,
                args.tenant_id,
                args.resource_id,
                start,
                end,
                args.user_email,
            )
            print(f"appointment {appt.id} created")
    except BookingError as e:
        print(f"error: {e}")


if __name__ == "__main__":
    main()
