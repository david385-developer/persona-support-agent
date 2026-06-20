# Two-Factor Authentication (2FA)

## Overview
Two-factor authentication adds an extra layer of security to your CloudFlow account by requiring a second form of verification beyond your password.

## Enabling 2FA

### Step 1: Access Security Settings
1. Go to Settings then Account then Security
2. Click "Enable Two-Factor Authentication"

### Step 2: Choose Method
- Authenticator App (Recommended): Google Authenticator, Authy, 1Password, Microsoft Authenticator
- SMS: Text message to verified phone number (less secure)
- Hardware Key: YubiKey or other FIDO2 device (most secure)

### Step 3: Setup
For authenticator app:
1. Scan the QR code with your app
2. Enter the 6-digit code to verify
3. Save the backup recovery codes (store securely)

## Recovery Codes
- 10 one-time recovery codes generated during setup
- Each code can be used once
- Store in a password manager or secure location
- Download as PDF or print
- Regenerate codes anytime from security settings

## Lost Access
If you lose your 2FA device:
1. Use a recovery code to log in
2. Immediately set up 2FA on a new device
3. If no recovery codes: Contact support with identity verification
4. Account recovery takes 24-48 hours with manual verification

## Organization-Wide 2FA (Enterprise)
Admins can enforce 2FA for all team members:
1. Go to Settings then Security then Organization Security
2. Toggle "Require 2FA for all members"
3. Set grace period (default: 7 days)
4. Members without 2FA will be locked out after grace period

## API Keys and 2FA
- API keys bypass 2FA (they are the second factor)
- Short-lived tokens (OAuth) require 2FA during authorization
- Service accounts (Enterprise) do not require 2FA