# API Error Troubleshooting Guide

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
