# AJAX/API Integration Skill

This skill provides guidance for working with the AJAX/API integration patterns used in the room rental contract management system.

## When to Use This Skill
Use this skill when:
- Modifying or extending API endpoints
- Working with frontend JavaScript that interacts with Django views
- Implementing new AJAX interactions
- Fixing issues in the client-server communication
- Improving performance or reliability of API interactions

## Skill Capabilities

### 1. Endpoint Development
- Create Django views that return JsonResponse
- Implement proper HTTP method handling (@require_http_methods)
- Handle CSRF protection correctly in AJAX requests
- Return appropriate HTTP status codes for different scenarios
- Structure JSON responses consistently with existing patterns
- Handle exceptions and return meaningful error messages

### 2. Frontend Integration
- Work with the existing JavaScript patterns in templates/
- Use the fetch API wrapper provided in the project
- Handle CSRF tokens in AJAX requests properly
- Update DOM elements based on API responses
- Implement proper loading states and user feedback
- Handle error cases gracefully in the UI

### 3. Data Serialization
- Format dates consistently (DD/MM/YYYY for display)
- Format currency values properly (VND with thousand separators)
- Structure nested data appropriately (room details in contract responses)
- Handle null/empty values gracefully
- Maintain consistency between different API endpoints

### 4. Security Considerations
- Implement proper CSRF protection for all state-changing endpoints
- Validate and sanitize all inputs before processing
- Use Django's built-in protections where applicable
- Implement proper authentication and authorization checks
- Protect against common web vulnerabilities (XSS, SQL injection, etc.)

## Project-Specific Patterns

### Backend API Patterns
All API views in this project follow these patterns:

1. **Method Restriction**: Use @require_http_methods(['GET', 'POST', etc.])
2. **Error Handling**: Try/catch blocks returning JsonResponse with error details
3. **Transaction Management**: Use @transaction.atomic for data modifications
4. **Response Format**: 
   - Success: JsonResponse({data}, status=200/201)
   - Error: JsonResponse({"error": "...", "details": "..."}, status=4xx/5xx)
5. **Database Access**: Use select_related() and select_for_update() appropriately
6. **CSRF Protection**: Expect X-CSRFToken header in POST requests

### Example Backend Pattern
```python
@require_http_methods(['POST'])
def my_endpoint(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            # Process data...
            
            with transaction.atomic():
                # Database operations...
                
            return JsonResponse({"message": "Success"}, status=200)
            
    except Exception as error:
        return JsonResponse(
            {
                "error":"Description of what went wrong",
                "details":f"{error}"
            },status=500
        )
```

### Frontend AJAX Patterns
The project uses a consistent pattern for AJAX requests:

1. **CSRF Handling**: Extract token from meta tag and send in headers
2. **Wrapper Function**: Uses `api()` function that handles fetch and error throwing
3. **POST Helper**: Uses `post()` function that sets proper headers and JSON body
4. **Error Handling**: Uses try/catch with user-friendly error display
5. **DOM Updates**: Updates specific elements based on response data

### Example Frontend Pattern
```javascript
// Generic API call wrapper
async function api(url, options = {}) {
  const res = await fetch(url, options);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || data.details || 'Có lỗi xảy ra.');
  return data;
}

// POST helper
const post = (url, body) => api(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
  body: JSON.stringify(body)
});

// Usage
try {
  await post('/endpoint/', {data: value});
  // Handle success
} catch (err) {
  // Handle error - display to user
}
```

### Response Handling Patterns
Frontend code handles responses in these ways:

1. **List Updates**: Replace table tbody.content with new data
2. **Modal Actions**: Hide modals after successful operations
3. **Form Handling**: Reset forms and clear validation states
4. **Error Display**: Show errors in designated alert elements
5. **Reload Patterns**: Use reloadAll() or specific load functions after mutations

## Common Integration Tasks

### Adding a New API Endpoint
1. **Design the endpoint**: Determine URL, HTTP method, and purpose
2. **Create the view**: Follow backend patterns in views.py
3. **Add URL pattern**: Register in urls.py with appropriate name
4. **Create frontend function**: Add appropriate API call function in JavaScript
5. **Update UI**: Modify event handlers to call the new function
6. **Handle response**: Update DOM based on API response data
7. **Test thoroughly**: Test success, error, and edge cases

### Modifying Existing Endpoint Behavior
1. **Understand current behavior**: Read existing view and frontend code
2. **Identify changes needed**: Determine what needs modification
3. **Update backend**: Modify view function following existing patterns
4. **Update frontend**: Adjust JavaScript calls and response handling
5. **Maintain compatibility**: Ensure existing functionality still works
6. **Test all scenarios**: Verify both old and new functionality work

### Creating Real-time Updates (Future Enhancement)
While current implementation uses manual reloads, consider:
- Implementing polling for periodic updates
- Using WebSocket connections for real-time updates
- Optimizing which data needs to be refreshed
- Managing connection lifecycle properly

## Security Best Practices

### CSRF Protection
- Always include X-CSRFToken header in POST/PUT/PDELETE requests
- Extract token from meta[name="csrf-token"] in templates
- Never disable CSRF protection without compelling reason and mitigation
- Use @csrf_exempt only when absolutely necessary and with alternative protections

### Input Validation
- Validate all inputs on both client and server sides
- Use Django's form validation where appropriate
- Implement proper type checking and range validation
- Sanitize outputs to prevent XSS (use escape functions in templates)
- Validate file uploads and inputs for security threats

### Error Handling
- Don't expose internal error details to users in production
- Log detailed errors server-side for debugging
- Return user-friendly error messages through API
- Handle network errors and timeouts gracefully
- Provide meaningful error messages for validation failures

### Data Protection
- Use HTTPS in production (not just development)
- Implement proper authentication for sensitive operations
- Consider rate limiting for public endpoints
- Protect sensitive data in API responses
- Follow principle of least privilege for data access

## Performance Considerations

### Efficient Queries
- Use select_related() for foreign key access to avoid N+1 problems
- Use only() or defer() to limit fields when not all data needed
- Consider pagination for large data sets
- Use database indexes appropriately for frequently queried fields

### Response Optimization
- Only return necessary data in API responses
- Consider compression for large responses
- Implement caching where appropriate and safe
- Use ETags or Last-Modified for conditional requests where beneficial

### Frontend Optimization
- Debounce rapid-fire user inputs
- Cache frequently accessed data when appropriate
- Minimize DOM manipulations
- Use requestAnimationFrame for animations
- Consider lazy loading for non-critical resources

## Testing API Interactions

### Backend Testing
1. **Unit Tests**: Test view functions with mock requests
2. **Integration Tests**: Test database interactions and transactions
3. **Edge Cases**: Test validation, error conditions, and boundary values
4. **Security Tests**: Test CSRF protection, input validation, authentication

### Frontend Testing
1. **Unit Tests**: Test JavaScript functions in isolation
2. **Integration Tests**: Test DOM updates and event handling
3. **User Simulation**: Test complete user workflows
4. **Error Scenario Tests**: Test network failures, invalid responses, etc.

### End-to-End Testing
1. **Happy Path**: Test complete successful workflows
2. **Error Paths**: Test how system handles various error conditions
3. **Concurrency**: Test simultaneous access scenarios
4. **Performance**: Test response times under various loads