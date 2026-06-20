# API Troubleshooting Guide

## Authentication Issues

### Error 401: Unauthorized
Cause: Invalid or expired API key.
Resolution:
1. Verify your API key at Settings then API Keys
2. Ensure the key has not been revoked
3. Check that you are using the correct header format:
   Authorization: Bearer sk_live_xxxxxxxxxxxxx
4. Regenerate the key if needed (old key becomes invalid immediately)

### Error 403: Forbidden
Cause: Insufficient permissions for the requested resource.
Resolution:
- Verify the API key scope includes the required permissions
- Admin-level endpoints require admin scope
- Check IP allowlist if enabled

## Rate Limiting

### Error 429: Too Many Requests
Cause: Exceeded rate limits.

Limits by plan:
- Free: 60 requests per minute, 10,000 per day
- Pro: 300 requests per minute, 100,000 per day
- Enterprise: 1,000 requests per minute, 1,000,000 per day

Resolution:
- Implement exponential backoff
- Use bulk endpoints where available
- Check X-RateLimit-Remaining header
- Request a limit increase for enterprise plans

## Common Errors

### Error 400: Bad Request
- Validate JSON payload against the schema
- Check Content-Type header (must be application/json)
- Ensure required fields are present

### Error 500: Internal Server Error
- Retry after 30 seconds
- Check status.cloudflow.io
- If persistent, contact support with the X-Request-Id header

## Webhooks
If webhook deliveries are failing:
1. Verify endpoint returns 2xx status
2. Check SSL certificate validity
3. Ensure endpoint responds within 30 seconds
4. Review webhook logs at Settings then Webhooks then Delivery Log

## SDKs
Official SDKs available for: Python, Node.js, Go, Java, Ruby
Repository: github.com/cloudflow/sdk