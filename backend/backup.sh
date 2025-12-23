#!/bin/bash
# Backup Script for ActionEDx Production Database
# Schedule with cron: 0 2 * * * /path/to/backup.sh

BACKUP_DIR="${BACKUP_DIR:-/var/backups/actionedx}"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="actionedx_backup_$DATE"
LOG_FILE="$BACKUP_DIR/backup.log"

# Create backup directory
mkdir -p "$BACKUP_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🗄️  Starting backup: $BACKUP_NAME"

# ==================== MONGODB BACKUP ====================

if [ -n "$MONGO_URL" ]; then
    log "Backing up MongoDB..."
    
    mongodump --uri="$MONGO_URL" \
        --out="$BACKUP_DIR/$BACKUP_NAME/mongodb" \
        --gzip \
        2>&1 | tee -a "$LOG_FILE"
    
    if [ $? -eq 0 ]; then
        log "✅ MongoDB backup completed"
    else
        log "❌ MongoDB backup failed"
        exit 1
    fi
else
    log "⚠️  MONGO_URL not set, skipping MongoDB backup"
fi

# ==================== REDIS BACKUP ====================

if [ -n "$REDIS_URL" ]; then
    log "Backing up Redis..."
    
    # Save Redis snapshot
    redis-cli -u "$REDIS_URL" BGSAVE
    sleep 5
    
    # Copy RDB file
    redis-cli -u "$REDIS_URL" --rdb "$BACKUP_DIR/$BACKUP_NAME/redis_dump.rdb" 2>&1 | tee -a "$LOG_FILE"
    
    if [ $? -eq 0 ]; then
        log "✅ Redis backup completed"
    else
        log "⚠️  Redis backup failed (non-critical)"
    fi
else
    log "⚠️  REDIS_URL not set, skipping Redis backup"
fi

# ==================== APPLICATION FILES ====================

log "Backing up application files..."

# Backup environment files
cp /app/backend/.env "$BACKUP_DIR/$BACKUP_NAME/backend.env" 2>/dev/null
cp /app/frontend/.env "$BACKUP_DIR/$BACKUP_NAME/frontend.env" 2>/dev/null

# Backup upload directory (if exists)
if [ -d "/app/uploads" ]; then
    cp -r /app/uploads "$BACKUP_DIR/$BACKUP_NAME/uploads"
fi

log "✅ Application files backed up"

# ==================== COMPRESS BACKUP ====================

log "Compressing backup..."

cd "$BACKUP_DIR"
tar -czf "${BACKUP_NAME}.tar.gz" "$BACKUP_NAME" 2>&1 | tee -a "$LOG_FILE"

if [ $? -eq 0 ]; then
    log "✅ Backup compressed: ${BACKUP_NAME}.tar.gz"
    
    # Remove uncompressed directory
    rm -rf "$BACKUP_NAME"
    
    # Get backup size
    BACKUP_SIZE=$(du -h "${BACKUP_NAME}.tar.gz" | cut -f1)
    log "📦 Backup size: $BACKUP_SIZE"
else
    log "❌ Backup compression failed"
    exit 1
fi

# ==================== UPLOAD TO S3 (Optional) ====================

if [ -n "$AWS_S3_BACKUP_BUCKET" ]; then
    log "Uploading to S3..."
    
    aws s3 cp "${BACKUP_NAME}.tar.gz" "s3://$AWS_S3_BACKUP_BUCKET/backups/" 2>&1 | tee -a "$LOG_FILE"
    
    if [ $? -eq 0 ]; then
        log "✅ Backup uploaded to S3"
    else
        log "⚠️  S3 upload failed (backup retained locally)"
    fi
fi

# ==================== CLEANUP OLD BACKUPS ====================

log "Cleaning up old backups (retention: $RETENTION_DAYS days)..."

find "$BACKUP_DIR" -name "actionedx_backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete 2>&1 | tee -a "$LOG_FILE"

log "✅ Backup completed successfully: ${BACKUP_NAME}.tar.gz"

exit 0
