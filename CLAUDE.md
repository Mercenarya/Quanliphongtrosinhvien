# Claude Code Configuration for Room Rental Contract Management System

This file provides project-specific guidance for using Claude Code with the Django-based room rental contract management system.

## Project Overview
This is a Django web application for managing room rentals and contracts. The system allows users to view and manage rooms, create/view/delete rental contracts, and track tenant information.

## Available Rules
Project-specific rules are located in `.claude/rules/`:

- `project-identity.md`: Defines the project's purpose, technical details, core models, key features, and development guidelines

## Available Skills
Project-specific skills are located in `.claude/skills/`:

- `django-contract-management.md`: Specialized guidance for Django development in this contract management system
- `rental-workflow.md`: Focuses on the specific business logic and workflows of room rental operations
- `ajax-api-integration.md`: Guidance for working with the AJAX/API integration patterns used in the system
- `testing-quality-assurance.md`: Testing and quality assurance practices for maintaining application reliability
- `project-setup.md`: Setup and configuration guidance for development and deployment

## How to Use These Resources

### When Starting Work
1. Review `project-identity.md` to understand the project context
2. Consult relevant skills based on your task:
   - For Django/model/view work: `django-contract-management.md`
   - For business logic/workflow changes: `rental-workflow.md`
   - For API/frontend integration: `ajax-api-integration.md`
   - For testing and quality work: `testing-quality-assurance.md`
   - For setup and configuration: `project-setup.md`

### Common Task Examples

#### Adding a New Feature
1. Review `project-identity.md` for overall guidelines
2. Consult `django-contract-management.md` for view/model patterns
3. Check `rental-workflow.md` if affecting rental business logic
4. Review `ajax-api-integration.md` if adding new API endpoints
5. Follow `testing-quality-assurance.md` for test coverage
6. Check `project-setup.md` if setup/configuration changes needed

#### Fixing a Bug
1. Identify affected areas (models, views, templates, etc.)
2. Consult relevant skills for best practices in those areas
3. Follow testing guidelines to create regression tests
4. Ensure changes align with project identity and conventions

#### Improving Performance
1. Review `ajax-api-integration.md` for optimization patterns
2. Check `django-contract-management.md` for efficient ORM usage
3. Consult `testing-quality-assurance.md` for performance testing approaches
4. Follow `project-setup.md` for deployment optimization

## Project-Specific Commands
The project has configured specific permissions in `.claude/settings.local.json`:
- PowerShell commands for running the Django development server
- PowerShell command for checking Django configuration
- PowerShell command for importing URLs to verify setup

## Development Workflow Recommendations
1. Always activate the virtual environment before working: `.venv\Scripts\activate`
2. Run `python manage.py check` periodically to catch configuration issues
3. Test changes thoroughly using the development server: `python manage.py runserver`
4. Keep the database backed up during development: `cp rental.db rental.db.backup`
5. Run migrations after model changes: `python manage.py makemigrations` and `python manage.py migrate`
6. Collect static files for production testing: `python manage.py collectstatic`

## Code Conventions to Follow
- Follow Django conventions and project-specific patterns
- Maintain CSRF protection for all state-changing operations
- Validate all inputs both client-side and server-side
- Use proper HTTP methods (GET for retrieval, POST for creates/deletes)
- Handle database transactions properly with `@transaction.atomic`
- Return consistent JSON responses from API endpoints
- Provide clear error messages to users
- Keep JavaScript modular and follow existing patterns
- Use Bootstrap classes consistently for styling
- Follow existing naming conventions for variables and functions