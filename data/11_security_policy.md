# Security Policy

## Data Encryption
- In transit: TLS 1.3 for all connections
- At rest: AES-256 encryption for all stored data
- Backups: Encrypted with separate key management

## Access Controls
- Role-based access control (RBAC)
- Minimum 4 roles: Viewer, Member, Admin, Owner
- Custom roles available on Enterprise plan
- IP allowlisting for API access (Enterprise)
- Session timeout: 24 hours (configurable)

## Authentication Security
- Password requirements enforced (12+ characters, complexity rules)
- bcrypt hashing with salt for stored passwords
- Account lockout after 5 failed attempts (30-minute cooldown)
- Optional 2FA via TOTP (Google Authenticator, Authy)
- SSO via SAML 2.0 or OAuth 2.0 (Enterprise)

## Compliance
- SOC 2 Type II certified
- GDPR compliant (EU data processing agreement available)
- CCPA compliant
- HIPAA BAA available (Enterprise)
- ISO 27001 certified
- Annual penetration testing by third-party security firm

## Incident Response
- 24/7 security monitoring
- Automated threat detection
- Incident response time: under 1 hour for critical issues
- Customer notification within 72 hours for data breaches
- Post-incident reports published within 30 days

## Vulnerability Reporting
Report security vulnerabilities to security@cloudflow.io:
- Response within 24 hours
- Bug bounty program available
- Hall of fame for responsible disclosure

## Data Residency
- Default: US-East (Virginia)
- Options: EU (Frankfurt), APAC (Singapore), AU (Sydney)
- Data residency selection available on Enterprise plan
- No cross-region data transfer without explicit consent