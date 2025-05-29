from __future__ import annotations

import argparse
from datetime import datetime

from .services import BookingService


def main() -> None:
    parser = argparse.ArgumentParser(description="TimeNest CLI")
    parser.add_argument("tenant", help="Tenant name")
    parser.add_argument("resource", help="Resource name")
    parser.add_argument("start", help="Start time (YYYY-mm-ddTHH:MM)")
    parser.add_argument("end", help="End time (YYYY-mm-ddTHH:MM)")
    parser.add_argument("user", help="User ID")
    args = parser.parse_args()

    service = BookingService()
    tenant = service.add_tenant(args.tenant)
    resource = service.add_resource(tenant.id, args.resource)
    start = datetime.fromisoformat(args.start)
    end = datetime.fromisoformat(args.end)
    appointment = service.book(resource.id, start, end, args.user)
    print(f"Booked appointment {appointment.id} for resource {resource.name}")


if __name__ == "__main__":
    main()
