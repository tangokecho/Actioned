# Security Hardening Configuration for ActionEDx
# Production security best practices

# ==================== API SECURITY ====================

# Rate Limiting Configuration
class SecurityConfig:
    # Rate limits by tier
    RATE_LIMITS = {
        "free": {
            "requests_per_minute": 10,
            "requests_per_hour": 100,
            "requests_per_day": 500
        },
        "basic": {
            "requests_per_minute": 30,
            "requests_per_hour": 500,
            "requests_per_day": 5000
        },
        "pro": {
            "requests_per_minute": 100,
            "requests_per_hour": 2000,
            "requests_per_day": 20000
        },
        "enterprise": {
            "requests_per_minute": 1000,
            "requests_per_hour": 10000,
            "requests_per_day": 100000
        }
    }
    
    # CORS Configuration
    CORS_ORIGINS = [
        "https://actionedx.com",
        "https://www.actionedx.com",
        "https://app.actionedx.com"
    ]
    
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS = ["*"]
    
    # JWT Configuration
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 24
    JWT_REFRESH_EXPIRATION_DAYS = 30
    
    # API Key Validation
    API_KEY_HEADER = "X-API-Key"
    API_KEY_MIN_LENGTH = 32
    
    # Request Size Limits
    MAX_REQUEST_SIZE_MB = 10
    MAX_UPLOAD_SIZE_MB = 50
    
    # IP Blocking
    IP_BLACKLIST_ENABLED = True
    MAX_FAILED_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 15
    
    # Content Security
    ALLOWED_FILE_EXTENSIONS = [".pdf", ".docx", ".txt", ".jpg", ".png"]
    SANITIZE_HTML = True
    
    # Headers Security
    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'"
    }

# ==================== SECRETS MANAGEMENT ====================

class SecretsConfig:
    # Never commit these to git
    # Use environment variables or secret managers
    
    # Required secrets
    REQUIRED_SECRETS = [
        "MONGO_URL",
        "EMERGENT_LLM_KEY",
        "JWT_SECRET",
        "REDIS_URL"
    ]
    
    # Secret rotation schedule
    SECRET_ROTATION_DAYS = 90
    
    # AWS Secrets Manager (optional)
    USE_AWS_SECRETS_MANAGER = False
    AWS_SECRET_NAME = "actionedx/production"
    
    # HashiCorp Vault (optional)
    USE_VAULT = False
    VAULT_URL = "https://vault.example.com"

# ==================== DATABASE SECURITY ====================

class DatabaseSecurity:
    # MongoDB security
    USE_TLS = True
    TLS_CA_FILE = "/path/to/ca-certificate.crt"
    
    # Authentication
    AUTH_SOURCE = "admin"
    
    # Connection security
    MIN_POOL_SIZE = 10
    MAX_POOL_SIZE = 50
    CONNECT_TIMEOUT_MS = 5000
    SOCKET_TIMEOUT_MS = 30000
    
    # Query limits
    MAX_QUERY_RESULTS = 1000
    MAX_QUERY_TIME_MS = 10000
    
    # Encryption at rest
    ENCRYPTION_ENABLED = True

# ==================== LOGGING & AUDIT ====================

class AuditConfig:
    # What to log
    LOG_AUTHENTICATION = True
    LOG_API_CALLS = True
    LOG_DATA_ACCESS = True
    LOG_ADMIN_ACTIONS = True
    LOG_ERRORS = True
    
    # Log retention
    LOG_RETENTION_DAYS = 90
    
    # PII handling
    MASK_SENSITIVE_DATA = True
    SENSITIVE_FIELDS = ["password", "api_key", "ssn", "credit_card"]
    
    # Log destinations
    LOG_TO_FILE = True
    LOG_TO_CLOUDWATCH = False
    LOG_TO_DATADOG = False

# ==================== COMPLIANCE ====================

class ComplianceConfig:
    # GDPR
    GDPR_ENABLED = True
    DATA_RETENTION_DAYS = 365
    RIGHT_TO_DELETE = True
    DATA_EXPORT_ENABLED = True
    
    # SOC 2
    SOC2_CONTROLS_ENABLED = False
    
    # HIPAA (if handling health data)
    HIPAA_COMPLIANT = False
