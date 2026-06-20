# SSO Setup Guide (SAML 2.0 and OAuth)

## Supported Identity Providers
- Okta
- Azure Active Directory
- Google Workspace
- OneLogin
- PingIdentity
- Custom SAML 2.0 providers

## Prerequisites
- Enterprise plan subscription
- Admin access to CloudFlow workspace
- Admin access to your identity provider

## SAML 2.0 Setup

### Step 1: Configure CloudFlow
1. Go to Settings then Security then Single Sign-On
2. Click "Enable SAML"
3. Note the following CloudFlow values:
   - Entity ID: https://app.cloudflow.io/saml/metadata
   - ACS URL: https://app.cloudflow.io/saml/acs
   - SLO URL: https://app.cloudflow.io/saml/slo

### Step 2: Configure Identity Provider
Create a new SAML application in your IdP with:
- Entity ID: Copy from CloudFlow
- ACS URL: Copy from CloudFlow
- Attribute Mapping:
  - email maps to user email
  - firstName maps to first name
  - lastName maps to last name
  - groups maps to team or role (optional)

### Step 3: Upload Metadata
1. Download the IdP metadata XML
2. Upload it to CloudFlow in Settings then Security then SSO
3. Click "Test Connection"
4. If successful, click "Enable for All Users"

## User Provisioning
- Just-In-Time (JIT): Users created on first SSO login
- SCIM: Automatic provisioning and deprovisioning (Enterprise)
- Manual: Admins invite users who then authenticate via SSO

## Troubleshooting
- Invalid SAML Response: Verify certificate and ACS URL match
- User not found: Ensure JIT provisioning is enabled or user is pre-created
- Clock skew: Sync server time; CloudFlow allows 5-minute skew
- Infinite redirect: Check that the IdP login URL is correct