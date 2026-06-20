# Backup and Disaster Recovery

## Automatic Backups
- Frequency: Every 6 hours
- Retention: 30 days of rolling backups
- Storage: Geographically distributed (minimum 3 regions)
- Encryption: AES-256 with customer-managed keys (Enterprise)

## What Is Backed Up
- All project and task data
- User accounts and permissions
- Custom fields and configurations
- File attachments (up to plan storage limits)
- Workflow automations
- API keys and integrations (encrypted)

## Point-in-Time Recovery (Enterprise)
Restore your workspace to any point within the last 30 days:
1. Go to Settings then Data Management then Backup and Recovery
2. Select date and time
3. Preview data snapshot
4. Confirm restoration
5. Recovery completes within 1-4 hours depending on data size

## Manual Backup
Create an on-demand backup:
1. Go to Settings then Data Management then Export
2. Select "Full Backup" option
3. Choose format (recommended: JSON for restoration)
4. Download when ready

## Disaster Recovery
- RTO (Recovery Time Objective): 4 hours
- RPO (Recovery Point Objective): 6 hours
- Failover: Automatic to secondary region
- Data replication: Synchronous within region, cross-region async

## Disaster Recovery Plan
1. Incident detected and classified
2. Failover initiated (automatic for critical)
3. DNS update (if needed)
4. Services restored from latest backup
5. Customer communication via status page
6. Post-incident review and report

## Data Integrity
- Checksums verified on every backup
- Monthly backup restoration testing
- Annual disaster recovery drill
- Third-party audit of backup procedures