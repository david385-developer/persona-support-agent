# Password Reset Guide

## Overview
CloudFlow provides multiple methods for resetting your password.

## Method 1: Email Reset
1. Navigate to the login page at https://app.cloudflow.io/login
2. Click "Forgot Password"
3. Enter your registered email address
4. Check your inbox for a reset link (valid for 24 hours)
5. Click the link and set a new password

Requirements:
- Password must be at least 12 characters
- Must include uppercase, lowercase, number, and special character
- Cannot reuse the last 5 passwords

## Method 2: Admin Reset
Workspace administrators can reset passwords for team members:
1. Go to Settings then Team Management
2. Select the user
3. Click "Reset Password"
4. The user will receive a temporary password via email

## Method 3: SSO Users
If your organization uses SSO (SAML or OAuth), password resets must be done through your identity provider (Okta, Azure AD, Google Workspace). CloudFlow does not manage passwords for SSO-enabled accounts.

## Troubleshooting
- Reset email not arriving: Check spam folder. Ensure noreply@cloudflow.io is whitelisted.
- Link expired: Request a new reset link. Links expire after 24 hours.
- Account locked: After 5 failed attempts, accounts lock for 30 minutes. Contact support if the issue persists.
- SSO conflict: If you see "SSO-managed account," reset through your identity provider.

## API Endpoint
For programmatic password resets (enterprise plans):
POST /api/v2/users/{user_id}/reset-password
Authorization: Bearer {admin_api_key}
Response: 200 OK with reset link in response body.