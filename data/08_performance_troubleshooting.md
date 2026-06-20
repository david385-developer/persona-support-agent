# Performance Troubleshooting

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
