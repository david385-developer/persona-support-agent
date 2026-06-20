# Webhook Integration Guide

## Overview
CloudFlow webhooks allow real-time notifications when events occur in your workspace.

## Setting Up Webhooks
1. Go to Settings then Developer then Webhooks
2. Click "Add Endpoint"
3. Enter your endpoint URL (must be HTTPS)
4. Select events to subscribe to
5. Save and note the signing secret

## Available Events
- task.created: New task created
- task.updated: Task modified
- task.completed: Task marked complete
- project.created: New project created
- project.archived: Project archived
- user.invited: Team member invited
- user.removed: Team member removed
- comment.added: Comment posted on task
- file.uploaded: File attached to task

## Payload Format
Each webhook payload includes:
- id: Unique event identifier (e.g., evt_abc123)
- type: Event type (e.g., task.completed)
- created_at: ISO 8601 timestamp
- data: Event-specific payload

## Verification
Verify webhook signatures using HMAC-SHA256.
The signature is sent in the X-CloudFlow-Signature header.
Always validate signatures before processing.

## Retry Policy
- Failed deliveries (non-2xx response) are retried up to 5 times
- Retry intervals: 1 min, 5 min, 30 min, 2 hours, 24 hours
- After 5 failures, the endpoint is disabled automatically
- Re-enable manually from the webhook settings

## Best Practices
- Return 200 quickly; process asynchronously
- Implement idempotency using the event id
- Validate signatures before processing
- Use event filtering to reduce unnecessary deliveries