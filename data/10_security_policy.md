# CloudFlow Security Policy

## Encryption
- In Transit: TLS 1.3 for all web and API traffic
- At Rest: AES-256 for all stored data
- Backups: Encrypted with separate key management

## Authentication
- Passwords hashed with bcrypt (cost factor 12)
- 2FA available for all users (required for Enterprise)
- SSO via SAML 2.0 and OpenID Connect
- Sessions expire after 24 hours of inactivity
- API keys can be scoped to permissions and IP ranges

## Infrastructure
- Hosted on AWS with SOC 2 Type II compliance
- Quarterly penetration testing
- Automated vulnerability scanning
- DDoS protection via Cloudflare
- Network segmentation between customers

## Compliance
- SOC 2 Type II: Annual audit
- GDPR: Full compliance
- HIPAA: Available for Enterprise with BAA
- ISO 27001: Certified
- CCPA: Compliant

## Incident Response
- Triage within 1 hour
- Customer notification within 24 hours
- Post-incident report within 5 business days
- 24/7 security team for critical incidents

## Data Retention
- Active data: While account is active
- Deleted accounts: Removed after 30 days
- Workflow logs: 90 days (Pro), 1 year (Enterprise)
- Audit logs: 1 year
- Backups: 30 days
