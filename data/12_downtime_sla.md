# Downtime and SLA Policy

## SLA Commitments

### Free Plan
- Uptime: Best effort
- Downtime credit: None

### Pro Plan
- Uptime SLA: 99.9%
- Downtime credit: 10% per hour of downtime

### Enterprise Plan
- Uptime SLA: 99.99%
- Downtime credit: 25% per hour of downtime

## What Counts as Downtime
- Complete service unavailability
- Error rates exceeding 5% of requests
- Response times exceeding 10 seconds (average over 5 minutes)
- Excluded: Scheduled maintenance, force majeure, customer-side issues

## Scheduled Maintenance
- Windows: Tuesdays 02:00-06:00 UTC
- Notification: 7 days in advance via email and in-app banner
- Frequency: Maximum once per month
- Emergency maintenance: May occur with shorter notice

## Status Page
Monitor real-time status at: status.cloudflow.io
- Component-level status (API, Dashboard, Webhooks, SSO)
- Incident history and post-mortems
- Subscribe to notifications (email, Slack, SMS)

## Incident Communication
1. Investigating: Acknowledged within 15 minutes
2. Identified: Root cause identified, ETA provided
3. Monitoring: Fix deployed, monitoring for stability
4. Resolved: Full resolution confirmed

## Claiming Credits
1. Submit request within 30 days of the incident
2. Include affected dates and times
3. Submit via Settings then Billing then SLA Credit Request
4. Credits applied within 2 billing cycles
5. Maximum credit: 100% of monthly bill