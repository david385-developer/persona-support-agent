# Data Export Guide

## Overview
CloudFlow allows you to export your data at any time for backup, migration, or analysis purposes.

## Export Options

### Via UI
1. Go to Settings then Data Management then Export
2. Select data types to export:
   - Projects and tasks
   - Comments and attachments
   - User data
   - Time tracking data
   - Custom fields
3. Choose format (CSV, JSON, or PDF)
4. Click "Generate Export"
5. Download link is emailed when ready (typically under 5 minutes)

### Via API
GET /api/v2/export/{data_type}?format=json&from=2024-01-01&to=2024-12-31
Authorization: Bearer {api_key}

### Automated Exports (Enterprise)
- Schedule daily, weekly, or monthly exports
- Delivery to S3, Google Cloud Storage, or Azure Blob
- Configure at Settings then Data Management then Scheduled Exports

## Export Formats
- CSV: Universal spreadsheet format, ideal for analysis
- JSON: Structured format for programmatic use
- PDF: Formatted reports for documentation
- XML: Available via API for enterprise integrations

## Data Included
- Projects: Name, description, status, dates, members, tags
- Tasks: Title, assignee, priority, due date, status, custom fields
- Comments: Author, content, timestamp, attachments
- Time entries: User, task, duration, date, billable status
- Files: Metadata only (files must be downloaded separately)

## Limits
- Maximum export size: 1 GB per request
- Rate limit: 1 export per hour
- Historical data: Available for the lifetime of the account
- Deleted items: Included for 30 days after deletion

## GDPR Data Export
For GDPR Subject Access Requests:
1. Go to Settings then Privacy then Data Export
2. Select user
3. Generate comprehensive export including all personal data
4. Download within 7 days (link expires)