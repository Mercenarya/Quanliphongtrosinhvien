# Django Contract Management Skill

This skill provides specialized guidance for working with the Django-based room rental contract management system.

## When to Use This Skill
Use this skill when:
- Adding new features to the contract management system
- Modifying existing models, views, or templates
- Fixing bugs in the Django application
- Improving performance or security
- Adding new API endpoints or modifying existing ones

## Skill Capabilities

### 1. Model Management
- Understand Room and Contract model relationships
- Add new fields to models with proper migrations
- Implement model validation and constraints
- Work with foreign key relationships (Contract -> Room)

### 2. View Development
- Create function-based views following project patterns
- Implement proper HTTP method handling (GET, POST)
- Use @require_http_methods decorator appropriately
- Handle database transactions with @transaction.atomic
- Return proper JsonResponse objects with correct status codes
- Implement proper error handling and validation

### 3. Template & Frontend Work
- Modify Bootstrap-based templates in /templates/
- Work with vanilla JavaScript in /templates/static/
- Implement form validation client-side and server-side
- Work with CSRF tokens in AJAX requests
- Update modal forms and table rendering logic

### 4. URL Configuration
- Add new paths to urls.py following existing patterns
- Use proper path parameters and converters
- Name URLs consistently for reverse lookups

### 5. Database Operations
- Use select_related() and select_for_update() appropriately
- Implement proper locking for concurrent access
- Use get_or_create() for idempotent operations
- Handle migrations properly when modifying models

### 6. Security Considerations
- Always maintain CSRF protection
- Validate and sanitize all user inputs
- Use proper HTTP status codes for different scenarios
- Implement proper permission checks where needed
- Secure direct object references (use get_object_or_404)

## Common Task Patterns

### Adding a New Feature
1. Update models.py if needed (add fields, new models)
2. Create and run migrations
3. Update views.py to handle new functionality
4. Add URL patterns in urls.py
5. Modify templates/frontend as needed
6. Add form validation and error handling
7. Test thoroughly

### Modifying Existing Functionality
1. Identify affected files (models, views, urls, templates)
2. Make minimal, focused changes
3. Preserve existing patterns and conventions
4. Update related tests if any exist
5. Verify backward compatibility

## Best Practices for This Project
1. Follow existing code style and patterns
2. Keep views focused and single-responsibility
3. Use Django's ORM efficiently (select_related, prefetch_related)
4. Handle edge cases (empty states, error conditions)
5. Provide clear user feedback through JSON responses
6. Maintain separation of concerns (logic in views, presentation in templates)
7. Keep JavaScript modular and reusable
8. Use Django's built-in features where possible (forms, validation)
9. Test both success and error paths
10. Document complex logic with comments

## Project-Specific Conventions
- Contract IDs follow format: HD-XXXX (where X is digit)
- Room IDs follow format: PXXX (where X is digit)
- Status values: Room.FREE = "Chưa được thuê", Room.RENTED = "Đã được thuê"
- Date format: DD/MM/YYYY for display
- Money format: Vietnamese đ currency with thousand separators
- Use transaction.atomic for database modifications
- Always check room status before creating contracts
- Update room status when contracts are created/deleted