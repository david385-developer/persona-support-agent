# Connectivity Troubleshooting

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
