# Error Codes Reference

## HTTP Status Codes

### 2xx Success
- 200 OK: Request succeeded
- 201 Created: Resource created
- 204 No Content: Success, no response body

### 4xx Client Errors
- 400 Bad Request: Invalid request body or parameters
- 401 Unauthorized: Missing or invalid authentication
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource does not exist
- 409 Conflict: Resource conflict (e.g., duplicate name)
- 422 Unprocessable Entity: Validation error
- 429 Too Many Requests: Rate limit exceeded

### 5xx Server Errors
- 500 Internal Server Error: Unexpected server failure
- 502 Bad Gateway: Upstream service unavailable
- 503 Service Unavailable: System maintenance or overload

## Application Error Codes

### Authentication (AUTH prefix)
- AUTH_001: Invalid API key
- AUTH_002: Expired token
- AUTH_003: Insufficient scope
- AUTH_004: IP not in allowlist
- AUTH_005: MFA required

### Validation (VAL prefix)
- VAL_001: Missing required field
- VAL_002: Invalid email format
- VAL_003: String exceeds max length
- VAL_004: Invalid date format (use ISO 8601)
- VAL_005: Invalid enum value

### Resource (RES prefix)
- RES_001: Resource not found
- RES_002: Resource already exists
- RES_003: Resource locked by another user
- RES_004: Resource quota exceeded
- RES_005: Resource in use, cannot delete

### Workflow (WF prefix)
- WF_001: Invalid workflow definition
- WF_002: Circular dependency detected
- WF_003: Step timeout exceeded
- WF_004: External service integration failed
- WF_005: Workflow execution limit reached

## Resolving Common Issues
1. Always check the error_code field in the response body
2. Include the X-Request-Id when contacting support
3. Review API documentation for expected request formats
4. Check system status at status.cloudflow.io before reporting outages