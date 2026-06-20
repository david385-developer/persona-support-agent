# API Rate Limits

## Default Limits

### Free Plan
- 60 requests per minute
- 10,000 requests per day
- 10 requests per second burst limit

### Pro Plan
- 300 requests per minute
- 100,000 requests per day
- 50 requests per second burst limit

### Enterprise Plan
- 1,000 requests per minute
- 1,000,000 requests per day
- 200 requests per second burst limit

## Rate Limit Headers
Every API response includes:
- X-RateLimit-Limit: Maximum requests allowed
- X-RateLimit-Remaining: Requests left in current window
- X-RateLimit-Reset: Unix timestamp when the window resets

## Handling Rate Limits
When rate limited (HTTP 429):
1. Read the Retry-After header
2. Wait that many seconds
3. Retry the request
4. Implement exponential backoff for multiple retries

## Best Practices
- Implement exponential backoff with jitter
- Cache responses where possible
- Use webhooks instead of polling
- Batch operations using bulk endpoints
- Monitor your usage via the API dashboard

## Endpoint-Specific Limits
Some endpoints have additional limits:
- File uploads: 10 per hour
- Bulk operations: 5 per minute
- Export requests: 1 per hour
- Password resets: 3 per hour per account

## Requesting Higher Limits
- Enterprise customers: Contact your account manager
- Pro customers: Submit request via support
- Evaluation based on usage patterns and plan