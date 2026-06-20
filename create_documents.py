"""
Generate all knowledge base documents (15 Markdown + 1 PDF).
Run once:  python create_documents.py
"""

import os
from fpdf import FPDF

DATA_DIR = "data"


def create_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def write_md(filename: str, content: str):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Created: {filename}")


def create_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 60, "", ln=True)
    pdf.cell(0, 12, "CloudFlow Support", ln=True, align="C")
    pdf.cell(0, 12, "Escalation Procedures Manual", ln=True, align="C")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 20, "", ln=True)
    pdf.cell(0, 8, "Version 3.2 | Effective: January 2025", ln=True, align="C")
    pdf.cell(0, 8, "Classification: Internal Use Only", ln=True, align="C")

    sections = [
        ("1. Escalation Tiers", [
            "Tier 1 - Frontline Support: Handles password resets, basic how-to",
            "questions, and known issues with documented solutions.",
            "Target resolution: under 10 minutes.",
            "",
            "Tier 2 - Technical Support: Handles API errors, integration issues,",
            "performance problems, and configuration troubleshooting.",
            "Target resolution: under 2 hours.",
            "",
            "Tier 3 - Engineering Escalation: Handles infrastructure outages,",
            "security incidents, data corruption, and bugs requiring code changes.",
            "Target resolution: under 24 hours.",
            "",
            "Tier 4 - Management Escalation: Handles billing disputes, legal",
            "requests, executive complaints, and SLA breach situations.",
            "Target resolution: under 4 hours.",
        ]),
        ("2. Mandatory Escalation Triggers", [
            "The following situations REQUIRE immediate escalation to Tier 3+4:",
            "",
            "- Any mention of data breach or unauthorized access",
            "- Account compromise or suspected fraud",
            "- Service outage affecting multiple customers",
            "- Legal threats or regulatory compliance issues",
            "- Billing disputes over $500",
            "- Customer has attempted resolution 3+ times without success",
            "- VIP or Enterprise customer expressing dissatisfaction",
            "- Any request to speak with management",
        ]),
        ("3. Handoff Protocol", [
            "When escalating, the agent MUST include:",
            "",
            "1. Customer persona classification",
            "2. Complete conversation history",
            "3. All troubleshooting steps already attempted",
            "4. Relevant knowledge base articles referenced",
            "5. Customer account information and plan tier",
            "6. Recommended next steps based on analysis",
            "",
            "The handoff summary should be formatted as structured JSON",
            "to enable automated routing and tracking.",
        ]),
        ("4. SLA Requirements", [
            "Enterprise Plan: 15-minute response, 1-hour resolution target",
            "Professional Plan: 1-hour response, 4-hour resolution target",
            "Free Plan: 24-hour response, 48-hour resolution target",
            "",
            "SLA breaches must be reported to the Support Manager within",
            "30 minutes of detection.",
        ]),
        ("5. Communication Guidelines by Persona", [
            "Technical Expert: Provide detailed technical information. Reference",
            "error codes, API docs, and system architecture. Skip basic explanations.",
            "",
            "Frustrated User: Lead with empathy. Use simple language. Provide",
            "step-by-step instructions. Follow up to confirm resolution.",
            "",
            "Business Executive: Focus on business impact and timelines. Be concise.",
            "Avoid technical jargon. Provide clear action items and ETAs.",
        ]),
    ]

    for title, lines in sections:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 12, title, ln=True)
        pdf.ln(4)
        pdf.set_font("Helvetica", "", 11)
        for line in lines:
            pdf.cell(0, 7, line, ln=True)

    path = os.path.join(DATA_DIR, "support_escalation_procedures.pdf")
    pdf.output(path)
    print(f"  Created: support_escalation_procedures.pdf")


docs = {
    "01_product_overview.md": """# CloudFlow Product Overview

## What is CloudFlow?
CloudFlow is a cloud-based workflow automation platform designed for modern teams. It enables businesses to automate repetitive tasks, integrate with third-party tools, and collaborate across departments in real time.

## Key Features
- **Workflow Builder**: Drag-and-drop visual workflow designer with 200+ pre-built templates
- **API Access**: RESTful API with comprehensive documentation for custom integrations
- **Team Collaboration**: Shared workspaces, role-based access control, and real-time notifications
- **Integrations**: Native integrations with Slack, Jira, GitHub, Salesforce, HubSpot, and 150+ other tools
- **Analytics Dashboard**: Real-time insights into workflow performance, bottlenecks, and team productivity
- **Webhooks**: Event-driven automation with customizable webhook triggers

## Plans
| Feature | Free | Professional ($29/mo) | Enterprise ($99/mo) |
|---------|------|-----------------------|---------------------|
| Workflows | 5 | Unlimited | Unlimited |
| API Calls | 1,000/month | 50,000/month | Unlimited |
| Team Members | 3 | 25 | Unlimited |
| Support | Community | Email (24hr) | Priority (1hr) |
| SSO | No | No | Yes |
| Custom Integrations | No | Yes | Yes |

## System Requirements
- Modern web browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- Stable internet connection (minimum 1 Mbps recommended)
- For API: Any HTTP client capable of making REST requests
""",

    "02_password_reset.md": """# Password Reset Guide

## How to Reset Your Password
1. Go to the CloudFlow login page at https://app.cloudflow.io/login
2. Click "Forgot Password"
3. Enter your registered email address
4. Check your inbox for the reset link (valid for 24 hours)
5. Click the link and create a new password

## Password Requirements
- Minimum 12 characters
- At least one uppercase letter, one lowercase letter, one number, and one special character
- Cannot be the same as your last 5 passwords
- Cannot contain your name or email address

## I Did Not Receive the Reset Email
- Check your spam/junk folder
- Verify you are using the correct email address
- Wait up to 15 minutes for delivery
- If using a corporate email, check with your IT team that emails from cloudflow.io are whitelisted
- Try requesting the reset link again

## Account Locked After Too Many Attempts
After 5 failed login attempts, your account is locked for 30 minutes. If you need immediate access:
- Use the "Forgot Password" flow to reset
- Contact support@cloudflow.io for manual unlock
- Enterprise users can contact their account administrator for immediate unlock

## Two-Factor Authentication Issues
If you have lost access to your 2FA device:
1. Use your backup recovery codes (provided during 2FA setup)
2. If you do not have recovery codes, contact support with your account verification details
3. Account recovery takes 24-48 hours for identity verification
""",

    "03_billing_faq.md": """# Billing and Subscription FAQ

## Subscription Plans
- **Free**: $0/month - 5 workflows, 1,000 API calls, 3 team members
- **Professional**: $29/month - Unlimited workflows, 50,000 API calls, 25 team members
- **Enterprise**: $99/month - Everything unlimited, priority support, SSO, custom integrations

## How to Upgrade Your Plan
1. Log in to CloudFlow
2. Go to Settings > Billing
3. Click "Change Plan"
4. Select your desired plan
5. Enter payment information
6. Confirm the upgrade

## Payment Methods
- Credit/Debit cards (Visa, Mastercard, American Express)
- PayPal
- Bank transfer (Enterprise plans only, annual billing)
- Purchase orders (Enterprise plans, minimum $1,000 annual)

## Billing Cycle
- Monthly plans are charged on the same date each month
- Annual plans are charged on the anniversary of signup
- Annual plans receive a 20% discount

## How to Cancel
1. Go to Settings > Billing
2. Click "Cancel Subscription"
3. Confirm cancellation
- Your plan remains active until the end of the current billing period
- No refunds for partial months on monthly plans
- Annual plans: refund available within 14 days of purchase

## Failed Payments
If a payment fails:
- We retry after 3 days, then after 7 days
- You will receive email notifications
- After 2 failed retries, your account is downgraded to Free
- Update payment methods at Settings > Billing > Payment Methods
""",

    "04_account_management.md": """# Account Management

## Creating an Account
1. Visit https://cloudflow.io and click "Get Started Free"
2. Enter your email address and create a password
3. Verify your email by clicking the confirmation link
4. Complete your profile setup

## Changing Your Email
1. Go to Settings > Account
2. Click "Change Email"
3. Enter your new email and current password
4. Verify the new email via the confirmation link

## Deleting Your Account
1. Go to Settings > Account > Danger Zone
2. Click "Delete Account"
3. Enter your password to confirm
4. All data is permanently deleted after 30 days
5. You can cancel deletion within the 30-day window by logging back in

**Warning**: Account deletion is irreversible after 30 days.

## Team Management

### Inviting Members
1. Go to Settings > Team
2. Click "Invite Member"
3. Enter their email and assign a role (Admin, Editor, Viewer)

### Roles and Permissions
- **Admin**: Full access, can manage billing and team members
- **Editor**: Can create and edit workflows, cannot manage billing
- **Viewer**: Read-only access to workflows and dashboards

### Removing Members
1. Go to Settings > Team
2. Click the member name
3. Select "Remove from Team"

## SSO Setup (Enterprise Only)
1. Go to Settings > Security > SSO
2. Select your identity provider (Okta, Azure AD, Google Workspace, OneLogin)
3. Follow the provider-specific setup wizard
4. Test the connection
5. Enable SSO for your organization
""",

    "05_api_troubleshooting.md": """# API Error Troubleshooting Guide

## Common Error Codes

### 401 Unauthorized
**Cause**: Invalid or missing API key
**Solution**:
1. Verify your API key at Settings > API Keys
2. Ensure the key is in the Authorization header: Authorization: Bearer YOUR_API_KEY
3. Check that the key has not been revoked
4. Generate a new key if needed

### 403 Forbidden
**Cause**: Insufficient permissions
**Solution**:
1. Check the API key permission scope
2. Verify your plan includes the endpoint
3. Ensure rate limits have not been exceeded

### 404 Not Found
**Cause**: Resource does not exist
**Solution**:
1. Verify the resource ID is correct
2. Check you are using API version v1
3. Confirm the resource has not been deleted
4. Base URL: https://api.cloudflow.io

### 429 Too Many Requests
**Cause**: Rate limit exceeded
**Solution**:
1. Implement exponential backoff (1s, 2s, 4s, 8s)
2. Check headers: X-RateLimit-Remaining, X-RateLimit-Reset
3. Consider upgrading for higher limits
4. Cache responses where possible

### 500 Internal Server Error
**Cause**: Server-side error
**Solution**:
1. Retry after 30 seconds
2. Check https://status.cloudflow.io
3. If persistent, contact support with the X-Request-Id value

### 503 Service Unavailable
**Cause**: Maintenance or overload
**Solution**:
1. Check the status page
2. Implement retry with exponential backoff
3. Contact support if it persists beyond 30 minutes

## Rate Limits by Plan
| Plan | Rate Limit | Daily Limit |
|------|-----------|-------------|
| Free | 10 req/min | 1,000/day |
| Professional | 100 req/min | 50,000/day |
| Enterprise | 1,000 req/min | Unlimited |
""",

    "06_connectivity_troubleshooting.md": """# Connectivity Troubleshooting

## Cannot Access Dashboard
1. Check your internet connection
2. Clear browser cache and cookies
3. Disable browser extensions (ad blockers, VPNs)
4. Try a different browser
5. Check DNS settings (try Google DNS: 8.8.8.8)
6. Ensure cloudflow.io is whitelisted in your firewall

## API Connection Issues

### Connection Refused
- Verify the base URL: https://api.cloudflow.io
- Ensure outbound HTTPS (port 443) is allowed
- Confirm TLS 1.2 or higher

### SSL/TLS Errors
- Update your CA certificate bundle
- Corporate MITM proxies may cause SSL issues

### Timeout Errors
- Default timeout is 30 seconds
- Use async endpoints for long operations
- Use webhooks instead of long-polling

## Webhook Delivery Issues
### Not Receiving Webhooks
1. Verify the URL is publicly accessible
2. Ensure your server returns 2xx within 10 seconds
3. Check delivery logs at Settings > Webhooks
4. Ensure your SSL certificate is valid

### Webhook Retries
- Retried up to 5 times with exponential backoff
- After 5 failures, the webhook is disabled automatically
- Re-enable at Settings > Webhooks
""",

    "07_email_delivery.md": """# Email Delivery Troubleshooting

## Not Receiving CloudFlow Emails
1. Check spam/junk folders
2. Add noreply@cloudflow.io to your contacts
3. Whitelist cloudflow.io with your IT team
4. Verify your email in Settings > Account
5. Request a resend of the specific email

## Notification Settings
1. Go to Settings > Notifications
2. Toggle types: workflow alerts, team activity, billing, security
3. Choose instant, daily digest, or weekly summary
4. Set quiet hours for non-critical notifications
5. Security alerts cannot be disabled

## Email Verification Issues
- Verification links expire after 48 hours
- Request a new link from the login page
- Wait 15 minutes for delivery

## Workflow Email Automation
- Verify your sender domain at Settings > Email > Domain Verification
- Set up SPF, DKIM, and DMARC records
- Check delivery logs at Settings > Email > Logs
- Enterprise plans can use custom SMTP servers
""",

    "08_performance_troubleshooting.md": """# Performance Troubleshooting

## Slow Dashboard
1. Hard refresh: Ctrl+Shift+R
2. Check browser memory usage
3. Limit custom dashboard widgets
4. Minimum 1 Mbps, 5+ Mbps recommended
5. Disable heavy browser extensions

## Slow Workflow Execution
### Causes
- Slow third-party API calls
- Large data processing (over 10MB)
- Complex nested logic
- Unoptimized database queries

### Optimization
- Use parallel execution blocks
- Implement pagination
- Cache frequently accessed data
- Use built-in transformers over custom scripts
- Split complex workflows into sub-workflows

## API Performance
- Check the status page for incidents
- Max payload: 10MB per request
- Use pagination (default 20, max 100 items)
- Include Accept-Encoding: gzip
- Use the fields parameter for needed data only

## Storage Limits
| Plan | Storage |
|------|---------|
| Free | 1 GB |
| Professional | 10 GB |
| Enterprise | 100 GB (expandable) |

Check usage at Settings > Storage. Archive old runs to free space.
""",

    "09_payment_troubleshooting.md": """# Payment Troubleshooting

## Payment Failed
### Common Reasons
1. Insufficient funds
2. Expired card
3. Bank blocks recurring international payments
4. Incorrect card details
5. 3D Secure not completed

### Solutions
1. Go to Settings > Billing > Payment Methods
2. Update or add a new payment method
3. Click "Retry Payment" on the failed invoice
4. Contact your bank to authorize CloudFlow Inc. charges

## Double Charges
1. Check for multiple CloudFlow accounts
2. Verify charge amounts match your plan
3. Look for separate add-on charges
4. Contact billing@cloudflow.io with transaction IDs
5. Refunds for duplicates: 5-7 business days

## Refund Requests
### Eligibility
- Monthly plans: No refund for partial months
- Annual plans: Full refund within 14 days
- Annual after 14 days: Prorated minus 10% fee

### How to Request
1. Settings > Billing > Request Refund
2. Select the invoice
3. Provide a reason
4. Refunds processed within 5-10 business days
""",

    "10_security_policy.md": """# CloudFlow Security Policy

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
""",

    "11_sla_agreement.md": """# Service Level Agreement

## Uptime Guarantee
| Plan | Uptime | Credit |
|------|--------|--------|
| Free | Best effort | N/A |
| Professional | 99.9% | 10% per hour of downtime |
| Enterprise | 99.95% | 25% per hour of downtime |

## Response Times
| Plan | Initial Response | Resolution Target |
|------|-----------------|-------------------|
| Free | 24 hours | 48 hours |
| Professional | 1 hour | 4 hours |
| Enterprise | 15 minutes | 1 hour |

## Downtime Definition
- Complete service unavailability
- API error rate over 5% for 5+ consecutive minutes
- Data loss or corruption

## NOT Downtime
- Scheduled maintenance (72hr notice)
- Customer code/config issues
- Third-party outages
- Customer internet issues

## Maintenance Windows
- Regular: Sundays 02:00-06:00 UTC
- Emergency: 4-hour minimum notice
- Enterprise: 7-day advance notice

## Claiming Credits
1. Open a ticket within 30 days
2. Include date, time, duration of downtime
3. Provide screenshots or error messages
4. Credits applied to next billing cycle
5. Maximum credit: 100% of monthly fee

## Escalation Path
1. Standard support channels
2. Technical support manager (1hr response)
3. VP of Engineering (4hr response)
4. C-level executive (24hr response)
""",

    "12_refund_policy.md": """# Refund Policy

## Monthly Subscriptions
- No refunds for partial billing periods
- Cancellation takes effect at end of billing cycle
- Exception: SLA breach credits may apply

## Annual Subscriptions
- 14-Day Money-Back Guarantee: Full refund within 14 days
- After 14 days: Prorated refund minus 10% processing fee
- After 6 months: No refund, credit can apply to downgrade

## Enterprise Contracts
- Refunds within 30 days of signing
- Pro-rata for early termination with 60-day notice
- Custom terms per agreement

## How to Request
1. Settings > Billing > Request Refund
2. Select the invoice
3. Provide a reason
4. Or email billing@cloudflow.io

## Processing Time
- Credit card: 5-10 business days
- PayPal: 3-5 business days
- Bank transfer: 10-15 business days

## Non-Refundable
- Consumed add-ons (API calls, storage)
- Completed consulting/training sessions
- Domain registration fees
""",

    "13_data_privacy.md": """# Data Privacy Policy

## Data We Collect
- Account info (name, email, company)
- Billing info (processed by Stripe, not stored by us)
- Usage data (workflow configs, execution logs, analytics)
- Customer content (workflow data, uploaded files, integration credentials)

## How We Use Data
- Provide and improve services
- Process transactions
- Send product updates and security alerts
- Analyze anonymized usage patterns
- Comply with legal obligations

## Data Sharing
We do NOT sell your data. We share only with:
- Service providers (AWS, Stripe, SendGrid) - all GDPR compliant
- When required by law
- With your explicit consent

## Your GDPR Rights
- Access: Request a copy of your data
- Rectification: Correct inaccurate data
- Erasure: Request deletion
- Portability: Export in JSON/CSV
- Objection: Opt out of marketing

## Data Export
1. Settings > Account > Data Export
2. Select data types
3. Download link within 24 hours

## Data Deletion
1. Settings > Account > Danger Zone
2. Data removed within 30 days
3. Billing records retained 7 years (legal requirement)

Contact privacy@cloudflow.io for privacy questions.
""",

    "14_onboarding_guide.md": """# Getting Started with CloudFlow

## Step 1: Create Your Account
Visit https://cloudflow.io, sign up with your work email, and verify.

## Step 2: Set Up Your Workspace
1. Name your workspace
2. Invite team members via Settings > Team
3. Choose your timezone

## Step 3: Create Your First Workflow
1. Click "New Workflow"
2. Choose a template or start from scratch
3. Add a trigger (e.g., new email, schedule)
4. Add actions (e.g., Slack notification, update spreadsheet)
5. Click "Save and Test"

## Step 4: Connect Integrations
1. Go to Settings > Integrations
2. Connect your daily tools
3. Popular first integrations: Slack, Google Sheets, Jira

## Step 5: Explore Templates
- Customer Onboarding automation
- Bug Tracking from error reports
- Invoice Processing and syncing
- Social Media scheduling
- HR Workflow automation

## Best Practices
1. Start simple, add complexity gradually
2. Use descriptive workflow names
3. Add error handling for critical workflows
4. Test with sample data before production
5. Set up failure notifications

## Learning Resources
- Docs: https://docs.cloudflow.io
- Tutorials: https://cloudflow.io/tutorials
- Community: https://community.cloudflow.io
- Webinars: Tuesdays 2 PM EST
""",

    "15_mobile_app_troubleshooting.md": """# Mobile App Troubleshooting

## App Crashes or Will Not Open
1. Update to the latest version
2. Clear app cache (Device Settings > Apps > CloudFlow > Clear Cache)
3. Restart your device
4. Reinstall the app
5. Minimum: iOS 15+ or Android 11+

## Push Notifications Not Working
1. Check permissions: Device Settings > Apps > CloudFlow > Notifications
2. Enable in CloudFlow app: Settings > Notifications
3. Check Do Not Disturb mode
4. Allow background refresh
5. Re-login to refresh tokens

## Cannot Connect
1. Check internet (WiFi or cellular)
2. Switch between WiFi and cellular
3. Disable VPN if active
4. Check if corporate network blocks CloudFlow
5. Clear app cache and retry

## Limited Mobile Editing
- View and monitor workflows: Full support
- Enable/disable workflows: Full support
- Edit workflow logic: Use web dashboard (recommended)
- View execution logs: Full support

## Sync Issues
1. Pull down to refresh on mobile
2. Hard refresh web dashboard (Ctrl+Shift+R)
3. Log out and back in on both
4. Use the same account on both platforms
5. Update both apps
""",
}


def main():
    print("Creating knowledge base documents...")
    create_dir()

    for filename, content in docs.items():
        write_md(filename, content)

    print("\nGenerating PDF...")
    create_pdf()

    print(f"\nDone! {len(docs)} markdown files + 1 PDF in '{DATA_DIR}/'")


if __name__ == "__main__":
    main()