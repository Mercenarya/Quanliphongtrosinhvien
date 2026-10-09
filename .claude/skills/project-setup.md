# Project Setup Skill

This skill provides guidance for setting up and configuring the Django-based room rental contract management system for development and deployment.

## When to Use This Skill
Use this skill when:
- Setting up the development environment for the first time
- Onboarding new developers to the project
- Configuring the project for different environments (dev, test, prod)
- Troubleshooting setup and configuration issues
- Setting up continuous integration and deployment pipelines
- Preparing the project for production deployment

## Skill Capabilities

### 1. Environment Setup
- Install and configure Python and Django dependencies
- Set up virtual environments properly
- Configure environment variables and settings
- Initialize the database and run migrations
- Set up static files and media handling

### 2. Configuration Management
- Understand and manage Django settings files
- Handle environment-specific configurations
- Manage secrets and sensitive configuration data
- Configure logging and debugging appropriately
- Set up allowed hosts and security settings

### 3. Database Management
- Initialize and migrate the database schema
- Handle database backups and restoration
- Manage data seeding and sample data
- Work with different database backends (SQLite for dev, PostgreSQL for prod)
- Handle database schema evolution and migrations

### 4. Development Workflow
- Set up development server with appropriate settings
- Configure auto-reload and debugging features
- Set up development tools and extensions
- Configure IDE and editor settings for the project
- Establish coding standards and pre-commit hooks

### 5. Deployment Preparation
- Prepare project for production deployment
- Configure production settings and optimizations
- Set up static file collection and serving
- Configure WSGI/ASGI servers appropriately
- Prepare environment-specific configuration files

## Project-Specific Setup Instructions

### Prerequisites
Before setting up this project, ensure you have:
- Python 3.8+ installed (Django 6.0.6 requires Python 3.8+)
- pip package manager available
- Git for version control (if using repository)
- Virtual environment tool (venv, virtualenv, or conda)
- Database system (SQLite3 included with Python, or PostgreSQL/MySQL for production)

### Step-by-Step Setup

#### 1. Clone or Obtain the Project
```bash
# If using git repository
git clone <repository-url>
cd <project-directory>

# If obtaining via other means, ensure you have the project files
```

#### 2. Create and Activate Virtual Environment
```bash
# Using venv (built-in)
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Unix/macOS:
source .venv/bin/activate

# Using virtualenv
virtualenv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix/macOS

# Using conda
conda create -n venv python=3.10
conda activate venv
```

#### 3. Install Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install Django and project dependencies
# If you have requirements.txt:
pip install -r requirements.txt

# If not, install Django explicitly (version from settings.py)
pip install "django==6.0.6"

# Note: This project appears to use minimal dependencies beyond Django
# Additional packages might be needed for production (psycopg2, gunicorn, etc.)
```

#### 4. Configure Environment Settings
The project uses a settings.local.jsone file for specific configurations. Review and adjust as needed:

```json
{
  "permissions": {
    "allow": [
      "PowerShell(python manage.py runserver --noreload --nothreading --timeout 1)",
      "PowerShell(python manage.py runserver --help)",
      "PowerShell(python manage.py runserver --noreload --nothreading)",
      "PowerShell($env:DJANGO_SETTINGS_MODULE = \"mysite.settings\"; python manage.py check)"
    ]
  }
}
```

#### 5. Set Environment Variables
```bash
# On Windows (PowerShell)
$env:DJANGO_SETTINGS_MODULE = "mysite.settings"

# On Unix/macOS (bash/zsh)
export DJANGO_SETTINGS_MODULE="mysite.settings"

# Optional: Set secret key for development (if not already in settings)
$env:DJANGO_SECRET_KEY = "your-development-secret-key-here"
export DJANGO_SECRET_KEY="your-development-secret-key-here"

# Optional: Enable debug mode for development
$env:DJANGO_DEBUG = "True"
export DJANGO_DEBUG="True"
```

#### 6. Initialize the Database
```bash
# Create database tables by running migrations
python manage.py migrate

# This will create the rental.db SQLite database file
# and tables for Room and Contract models
```

#### 7. Load Sample Data (Optional)
The project includes a seed_data() function in models.py. To load sample data:

```bash
# Option 1: Call the function directly in Django shell
python manage.py shell
>>> from services.models import seed_data
>>> seed_data()
>>> exit()

# Option 2: Create a custom management command or migration
# Option 3: Call it from your code during setup
```

#### 8. Collect Static Files (for Production)
```bash
# For production deployment, collect static files
python manage.py collectstatic
```

#### 9. Start Development Server
```bash
# Run the development server
python manage.py runserver

# Or with specific settings from the permissions file:
python manage.py runserver --noreload --nothreading

# The server will be available at http://127.0.0.1:8000/
```

### Environment-Specific Configurations

#### Development Environment
- DEBUG = True
- Detailed error pages enabled
- Console email backend
- Verbose logging
- Allow localhost and 127.0.0.1 in ALLOWED_HOSTS
- Development-specific secrets and API keys

#### Testing Environment
- DEBUG = False (usually)
- Test database configuration
- Disabled caching (or test cache configurations)
- Test-specific credentials and services
- Coverage collection enabled

#### Production Environment
- DEBUG = False
- Proper ALLOWED_HOSTS configuration
- Secure SECRET_KEY (strong, unique, kept secret)
- Proper database configuration (PostgreSQL/MySQL recommended)
- Email backend configured for real email sending
- Static files served properly (via CDN or web server)
- Security headers and protections enabled
- Logging configured for production (file-based, appropriate levels)
- Caching configured and optimized
- File permissions set appropriately

### Database Configuration Examples

#### SQLite (Development - Default)
```python
# Already configured in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'rental.db',
    }
}
```

#### PostgreSQL (Production Recommended)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rental_db',
        'USER': 'rental_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### MySQL Alternative
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rental_db',
        'USER': 'rental_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Settings Management Approaches

#### Method 1: Environment Variables (Recommended)
Use python-decouple or similar to manage settings via environment variables:
```python
# In settings.py
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

# Database example
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

#### Method 2: Settings Files Hierarchy
```
mysite/
    settings/
        __init__.py
        base.py          # Common settings
        development.py   # Dev-specific settings
        production.py    # Prod-specific settings
        testing.py       # Test-specific settings
```

#### Method 3: settings.local.json Pattern (Current Approach)
The project already uses a settings.local.json approach for Claude Code permissions.
This can be extended for other environment-specific configurations.

### Development Tools and Extensions

#### Recommended Packages for Development
```bash
# Install development dependencies
pip install \
    ipython \
    django-extensions \
    debug-toolbar \
    factory-boy \
    Faker \
    pytest \
    pytest-django \
    coverage
```

#### Useful Django Extensions Commands
```bash
# Shell enhancements
python manage.py shell_plus

# Model visualization (requires graphviz)
python manage.py graph_models

# Route listing
python manage.py show_urls

# Reset migrations (use with caution!)
python manage.py reset_app

# Generate sample data
python manage.py generate_fixture_data
```

#### Debug Toolbar Configuration
```python
# In settings.py (when DEBUG=True)
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
    INTERNAL_IPS = ['127.0.0.1', 'localhost']
```

### IDE and Editor Configuration

#### VS Code Settings
Create `.vscode/settings.json`:
```json
{
    "python.pythonPath": "./.venv/bin/python",
    "django.enableLanguageServers": true,
    "editor.formatOnSave": true,
    "editor.tabSize": 4,
    "files.insertFinalNewline": true,
    "files.trimTrailingWhitespace": true,
    "[python]": {
        "editor.defaultFormatter": "ms-python.python"
    }
}
```

#### PyCharm Configuration
- Set project interpreter to .venv/bin/python
- Enable Django support in project settings
- Configure code style to match project conventions
- Set up inspections and code quality tools

### Pre-Commit Hooks (Optional but Recommended)
Install and configure pre-commit for automatic code quality checks:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
        additional_args: [--max-line-length=88]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.910
    hooks:
      - id: mypy
        additional_args: [--ignore-missing-imports]
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.0.1
    hooks:
      - id: trailing-whitespace
      - id: ending-newline
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
EOF

# Install hooks
pre-commit install

# Run manually on all files (optional)
pre-commit run --all-files
```

### Testing the Setup
After setup, verify the installation works:

```bash
# Check Django version
python -c "import django; print(django.get_version())"

# Check project can be imported
python -c "import mysite; print('Project imported successfully')"

# Run basic checks
python manage.py check

# Create superuser (for admin access)
python manage.py createsuperuser

# Test database connection
python manage.py dbshell  # Should open SQLite shell

# Run development server and verify it works
python manage.py runserver
# Visit http://127.0.0.1:8000/ in browser
```

### Common Setup Issues and Solutions

#### Issue: ModuleNotFoundError for Django
**Solution**: Ensure Django is installed in the active virtual environment
```bash
# Check active environment
which python  # or where python on Windows
# Should point to .venv/bin/python or similar
pip list | grep Django
# Install if missing
pip install django==6.0.6
```

#### Issue: Permission Denied on Database File
**Solution**: Check file permissions and ensure the process can write to the directory
```bash
# On Unix/Linux/macOS
ls -la rental.db
chmod 664 rental.db  # if needed
# Ensure directory is writable
ls -la .
chmod 775 .  # if needed (be careful with permissions)
```

#### Issue: Address Already in Use When Running Server
**Solution**: Stop existing processes or use different port
```bash
# Find and kill existing processes
lsof -i :8000  # Unix/Linux/macOS
netstat -ano | findstr :8000  # Windows
# Kill the process using PID from above
# Or use different port
python manage.py runserver 8001
```

#### Issue: Migration Errors Due to Existing Database
**Solution**: Handle existing data carefully
```bash
# Backup existing database if needed
cp rental.db rental.db.backup

# Options for resolving migration conflicts:
# 1. Start fresh (delete db and rerun migrations)
rm rental.db
python manage.py migrate

# 2. Fake initial migration if tables exist
python manage.py migrate --fake-initial

# 3. Reset migrations (advanced - use with caution)
# Only if you control the database completely
```

#### Issue: Static Files Not Loading in Development
**Solution**: Check DEBUG mode and static files configuration
```bash
# Ensure DEBUG=True in settings
# Check that you're running runserver (not just running the server directly)
# Verify STATIC_URL and STATICFILES_DIRS settings
# Try accessing static file directly: http://127.0.0.1:8000/static/<path>
```

### Production Deployment Considerations

#### Web Server Choices
For production, consider these options:

1. **Gunicorn + Nginx** (most common)
   ```bash
   # Install
   pip install gunicorn
   
   # Run
   gunicorn mysite.wsgi:application --bind 0.0.0.0:8000
   
   # Or via systemd service
   ```

2. **uWSGI + Nginx**
3. **mod_wsgi + Apache**
4. **Daphne + Nginx** (for ASGI/WebSocket support)
5. **Hypercorn + Nginx** (ASGI alternative)

#### Key Production Settings
In production settings.py:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = '# generate a strong secret key #'
# Use environment variable in production: os.environ.get('SECRET_KEY')

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_HOST = None
SECURE_SSL_REDIRECT = True  # if using SSL/TLS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# Database - use PostgreSQL or MySQL
# Configure properly for production load

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
# Ensure collectstatic has been run

# Media files (if applicable)
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Configure SMTP settings appropriately

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'error.log',
        },
    },
    'root': {
        'handlers': ['file'],
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
```

#### Deployment Process
1. **Code Preparation**
   - Ensure all changes are committed and tested
   - Run linters and code quality checks
   - Update dependencies as needed
   - Prepare release notes

2. **Environment Preparation**
   - Provision servers or containers
   - Install required system dependencies
   - Configure networking and firewalls
   - Set up SSL/TLS certificates
   - Prepare database and backup systems

3. **Deployment Execution**
   - Pull latest code
   - Create/activate virtual environment
   - Install dependencies
   - Run database migrations
   - Load any required seed data
   - Collect static files
   - Configure web server
   - Start application services
   - Run health checks

4. **Post-Deployment Verification**
   - Verify application responds correctly
   - Check key functionality works
   - Monitor error logs
   - Check performance metrics
   - Confirm security configurations
   - Validate backup and recovery processes

5. **Monitoring and Maintenance**
   - Set up ongoing monitoring
   - Configure log rotation
   - Schedule regular backups
   - Plan for security updates
   - Establish incident response procedures

### Troubleshooting Common Issues

#### Database Connection Issues
- Verify database service is running
- Check connection parameters (host, port, name, user, password)
- Ensure network connectivity between app and DB
- Verify user has sufficient permissions
- Check for connection limits or exhaustion

#### Performance Problems
- Identify slow queries using Django Debug Toolbar or db logging
- Check for missing database indexes
- Look for N+1 query problems
- Verify caching is working effectively
- Check resource utilization (CPU, memory, disk I/O)
- Consider horizontal scaling or load balancing

#### Security Concerns
- Regularly update dependencies
- Conduct periodic security audits
- Monitor for suspicious activity in logs
- Keep SSL/TLS certificates current
- Review and update security settings periodically
- Conduct penetration testing periodically

#### Deployment Failures
- Check deployment logs for error messages
- Verify environment variables are set correctly
- Check file permissions and ownership
- Validate configuration file syntax
- Ensure sufficient disk space and memory
- Check service dependencies are available

#### User-Reported Issues
- Reproduce the issue in a controlled environment
- Check logs for relevant error messages
- Verify recent changes didn't introduce regressions
- Test with user-specific data and scenarios
- Consider A/B testing or feature flags for risky changes

## Conclusion
Proper setup and configuration are crucial for the success of any Django project. By following the guidelines in this skill, you can ensure that the room rental contract management system is set up correctly, maintains consistency across environments, and is ready for both development and production use. Remember that setup is not a one-time task but an ongoing process that requires attention as the project evolves and scales.