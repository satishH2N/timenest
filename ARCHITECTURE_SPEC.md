# TimeNest Architecture & Design Specification

## 1. Executive Summary
TimeNest is a multi-tenant SaaS platform providing appointment booking for
service organizations. By delivering scheduling, reminders, and payments from a
single cloud-native solution, TimeNest shortens booking cycles while providing
observability and compliance. Target customers include clinics, consultancies,
and retailers requiring self-service scheduling. The MVP focuses on booking and
multi-tenant management; v1 adds payments and subscriptions, while v2 brings
marketplace integrations and analytics.

## 2. System Context & Requirements
### Actors & Roles
- **Tenant Admin** – configures tenant resources and billing.
- **Resource Manager** – manages calendars for staff or assets.
- **End-User** – books, reschedules, and cancels appointments.
- **Support Agent** – assists with account issues and escalations.

### Functional Requirements
- Self-service booking with real-time availability.
- Notifications via email and SMS.
- Online payments for paid appointments.
- Tenant and resource administration panels.
- Support tooling and full audit history.

### Non-functional Requirements
- **Security & Compliance** – ISO-27001 and SOC 2 alignment.
- **Performance** – p95 API latency under 250ms.
- **Availability** – 99.9% uptime with 15m RTO and 1h RPO.
- **Scalability** – horizontal scaling across tenants.
- **Observability** – metrics, logs, and traces for every request.

## 3. Logical Architecture
```
[Client] -> [Vercel Frontend] -> [API Gateway]
                              -> [Auth Service]
                              -> [Booking Service]
                              -> [Notification Worker]
                              -> [Payments Service]
                              -> [Postgres / Redis]
```

### Data Flow Narrative
1. User loads booking page served from Vercel CDN.
2. API Gateway validates JWT and routes to Booking Service.
3. Booking Service checks calendar rules in Postgres and locks the slot.
4. Payment Service captures payment via third-party API when required.
5. Appointment stored and message queued for Notification Worker.
6. Worker sends confirmation email or SMS and writes to Audit Log.

## 4. Physical & Deployment Architecture
TimeNest uses Vercel for serverless web and API functions. Postgres is hosted on
Neon with high availability and Redis from a managed provider. A dedicated
worker cluster handles notifications.

```
+-----------+        +------------------+
|   Users   |  -->   |  Vercel Edge     |
+-----------+        +------------------+
                        |
  +---------------------+-------------------+
  |      API Routes (Vercel)               |
  +---------------------+-------------------+
                        |
       +-------------------------------+
       | Managed Postgres (Neon)       |
       | Managed Redis                 |
       +-------------------------------+
                        |
         +---------------------------+
         | Notification Workers      |
         +---------------------------+
```

### HA and DR
- Multi-zone deployment on Vercel with a cold standby region.
- Neon Postgres with point-in-time recovery and cross-region replica.
- Redis configured with replication and persistence.
- RPO: 1 hour. RTO: 15 minutes with automated failover.

## 5. Data Model & Persistence
```
@startuml
entity Tenant {
  *id : uuid
  name : string
}
entity Resource {
  *id : uuid
  tenant_id : uuid
  name : string
}
entity CalendarRule {
  *id : uuid
  resource_id : uuid
  rule : jsonb
}
entity RuleException {
  *id : uuid
  resource_id : uuid
  window : tstzrange
}
entity Appointment {
  *id : uuid
  resource_id : uuid
  user_id : uuid
  time : timestamptz
  status : string
}
entity AuditLog {
  *id : uuid
  tenant_id : uuid
  actor_id : uuid
  action : string
  timestamp : timestamptz
}
entity Subscription {
  *id : uuid
  tenant_id : uuid
  plan : string
  status : string
}
Tenant ||--o{ Resource
Resource ||--o{ CalendarRule
Resource ||--o{ RuleException
Resource ||--o{ Appointment
Tenant ||--o{ AuditLog
Tenant ||--o{ Subscription
@enduml
```
Indexes on `resource_id`, `tenant_id`, and appointment timestamps enable fast
lookups. Partitions by tenant aid scalability. Audit logs are retained seven
years for compliance.

## 6. API Design
Below is a shortened OpenAPI 3.0 spec.
```yaml
openapi: 3.0.3
info:
  title: TimeNest API
  version: 1.0.0
servers:
  - url: https://api.timenest.com
paths:
  /v1/appointments:
    post:
      summary: Book appointment
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AppointmentCreate'
      responses:
        '201':
          description: Created
        '409':
          description: Slot unavailable
    get:
      summary: List appointments
      parameters:
        - in: query
          name: page
          schema:
            type: integer
        - in: query
          name: per_page
          schema:
            type: integer
      responses:
        '200':
          description: OK
  /v1/tenants/{tenantId}/resources:
    get:
      summary: List resources
      parameters:
        - in: path
          name: tenantId
          required: true
          schema:
            type: string
      responses:
        '200':
          description: OK
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    AppointmentCreate:
      type: object
      properties:
        resource_id:
          type: string
        start:
          type: string
          format: date-time
        end:
          type: string
          format: date-time
      required: [resource_id, start, end]
security:
  - bearerAuth: []
```
All endpoints are rate limited to 100 requests per minute per IP. Idempotency
keys may be provided via the `Idempotency-Key` header to guarantee safe retries.

## 7. Security & Compliance
- **ISO-27001**
  - A.9 Access Control – RBAC and least privilege for all actors; MFA for admins.
  - A.12 Operations – change management via CI/CD, anti-malware, monitoring,
    and backups.
  - A.18 Compliance – data retention, legal, and audit obligations.
- **SOC 2 Trust Services Criteria**
  - Security – WAF, IDS/IPS, vulnerability scanning, patch management.
  - Availability – autoscaling infrastructure and multi-region failover.
  - Confidentiality – strong encryption at rest and in transit.
  - Privacy – consent management and data subject request workflows.
- TLS 1.2+ for all network traffic and AES‑256 encryption for stored data.
- Secrets in Vercel encrypted variables rotated quarterly.
- Quarterly penetration testing and continuous vulnerability scans.
- Immutable audit logs restricted to support personnel only.

## 8. Observability & Operations
- **Metrics** collected via Prometheus or Datadog: latency, error rates, queue
  depth.
- **Tracing** with OpenTelemetry exported to Jaeger.
- **Logs** aggregated to ELK or Splunk with 30‑day retention.
- Alerts integrate with PagerDuty; on-call runbooks define escalation.
- **CI/CD** pipeline using GitHub Actions:
```yaml
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install deps
        run: npm ci
      - name: Lint
        run: npm run lint
      - name: Unit tests
        run: npm test
      - name: Security Scan
        uses: github/codeql-action/init@v2
```
- Canary deployments route a small percent of traffic before full rollout.
- Rollbacks triggered via GitHub Actions on failing health checks.

## 9. Scalability & Performance
- Vercel functions auto-scale based on request load.
- Postgres read replicas serve read heavy workloads.
- Redis caches calendar rules and popular appointments with TTL.
- Capacity planning aims for p95 latency 250ms at 1000 QPS per tenant.
- Target cache hit ratio is 80% to reduce database pressure.

## 10. Business Continuity & DR
- Nightly Postgres backups to object storage.
- Weekly restore tests validate backup integrity.
- Cross-region replication for Postgres and Redis.
- DR scripts restore the platform within 15 minutes using IaC.

## 11. Governance & Roadmap
- **MVP** – core booking, multi-tenant support, and notifications.
- **v1** – payments integration, subscription management, and audit logs.
- **v2** – marketplace integrations and analytics dashboards.
Regular security and compliance audits accompany each release. Capacity
expansion occurs monthly based on usage metrics.
