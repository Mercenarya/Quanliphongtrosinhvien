# Testing and Quality Assurance Skill

This skill provides guidance for testing and maintaining quality in the Django-based room rental contract management system.

## When to Use This Skill
Use this skill when:
- Writing tests for new or existing functionality
- Setting up testing environments and configurations
- Implementing continuous integration practices
- Performing code reviews with quality focus
- Setting up monitoring and observability
- Improving overall application reliability and maintainability

## Skill Capabilities

### 1. Test Strategy and Planning
- Determine appropriate testing levels (unit, integration, end-to-end)
- Identify critical paths and high-risk areas for testing
- Plan test coverage based on business impact and complexity
- Establish testing routines and frequencies
- Balance automated vs manual testing efforts

### 2. Django Testing Framework
- Write and run unit tests using Django's TestCase
- Create test fixtures and factories for consistent test data
- Use Django's test client for view testing
- Test models, views, forms, and templates effectively
- Utilize Django's testing utilities and assertions

### 3. Test Automation
- Set up automated test execution
- Integrate tests with development workflows
- Configure test runners and discovery patterns
- Implement test reporting and metrics collection
- Handle test data isolation and cleanup

### 4. Code Quality and Standards
- Enforce coding standards and conventions
- Conduct effective code reviews
- Implement static analysis and linting
- Monitor technical debt and code smells
- Ensure documentation quality and completeness

### 5. Performance and Load Testing
- Establish performance baselines and benchmarks
- Identify and bottleneck areas
- Test application behavior under various loads
- Monitor resource usage and optimization opportunities
- Plan for scalability and performance improvements

### 6. Production Monitoring and Observability
- Implement logging strategies and levels
- Set up error tracking and alerting
- Monitor application metrics and health indicators
- Establish incident response procedures
- Plan for disaster recovery and backup strategies

## Django-Specific Testing Practices

### Model Testing
- Test model methods and properties
- Validate field constraints and validators
- Test model managers and custom querysets
- Verify relationships and cascading behaviors
- Test model string representations (__str__)

### View Testing
- Test both GET and POST request handling
- Validate URL routing and reverse lookups
- Test template rendering and context data
- Verify form handling and validation
- Test authentication and permission requirements
- Check for proper HTTP status codes and responses

### Form Testing
- Test field validation and cleaning
- Verify required fields and error messages
- Test widget rendering and attributes
- Validate form saving and instance creation
- Test custom form methods and properties

### Template Testing
- Test template rendering with various contexts
- Verify template tags and filters work correctly
- Test template inheritance and block overriding
- Check for proper escaping and security
- Validate template includes and extends

## Project-Specific Testing Approach

### Models Testing (Room and Contract)
```python
# Example test cases for Room model
def test_room_creation():
    room = Room.objects.create(
        id="P101",
        name="Phòng 101",
        area=20,
        price=3000000,
        status=Room.FREE
    )
    assert room.id == "P101"
    assert room.status == Room.FREE
    assert str(room) == "P101"

def test_room_status_transition():
    room = Room.objects.create(
        id="P102",
        name="Phòng 102",
        area=25,
        price=3500000,
        status=Room.FREE
    )
    # Test transition to rented
    room.status = Room.RENTED
    room.save()
    assert room.status == Room.RENTED
    
    # Test transition back to free
    room.status = Room.FREE
    room.save()
    assert room.status == Room.FREE
```

### Views Testing (Contract Management)
```python
# Example test cases for contract views
from django.test import TestCase, Client
from django.urls import reverse
import json

class ContractViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test room
        self.room = Room.objects.create(
            id="P101",
            name="Phòng 101",
            area=20,
            price=3000000,
            status=Room.FREE
        )
    
    def test_contract_list_empty(self):
        response = self.client.get(reverse('contract-list'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['contracts']), 0)
    
    def test_contract_create_success(self):
        contract_data = {
            "contract_id": "HD-0001",
            "room_id": "P101",
            "tenant_name": "Nguyễn Văn An",
            "tenant_id_card": "012345678901",
            "duration_months": "6"
        }
        
        response = self.client.post(
            reverse('contract-add'),
            data=json.dumps(contract_data),
            content_type='application/json',
            HTTP_X_CSRFTOKEN='test-token'  # In real tests, handle CSRF properly
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['message'], "Thêm hợp đồng thành công.")
        self.assertEqual(data['contract']['id'], "HD-0001")
        
        # Verify room status updated
        self.room.refresh_from_db()
        self.assertEqual(self.room.status, Room.RENTED)
    
    def test_contract_create_duplicate_id(self):
        # Create first contract
        Contract.objects.create(
            id="HD-0001",
            room=self.room,
            tenant_name="Nguyễn Văn An",
            tenant_id_card="012345678901",
            contract_date=date.today(),
            duration_months=6
        )
        self.room.status = Room.RENTED
        self.room.save()
        
        # Try to create duplicate
        contract_data = {
            "contract_id": "HD-0001",  # Same ID
            "room_id": "P102",  # Different room
            "tenant_name": "Trần Thị Bình",
            "tenant_id_card": "098765432109",
            "duration_months": "12"
        }
        
        response = self.client.post(
            reverse('contract-add'),
            data=json.dumps(contract_data),
            content_type='application/json',
            HTTP_X_CSRFTOKEN='test-token'
        )
        
        self.assertEqual(response.status_code, 409)  # Conflict
        data = json.loads(response.content)
        self.assertIn("already exists", data['error'])
```

### JavaScript Testing Concepts
While the project uses vanilla JavaScript, consider:
- Testing DOM manipulation functions in isolation
- Testing form validation logic
- Testing AJAX request handling (with mocked fetch)
- Testing error handling and user feedback
- Testing edge cases in utility functions

## Quality Assurance Practices

### Code Review Checklist
When reviewing code for this project, check for:

1. **Functionality**
   - Does the code implement the intended feature correctly?
   - Are all edge cases handled?
   - Is the business logic correct and complete?

2. **Code Quality**
   - Does the code follow project conventions and patterns?
   - Is the code readable and well-structured?
   - Are variable and function names descriptive?
   - Is there appropriate commenting for complex logic?

3. **Security**
   - Is CSRF protection maintained for state-changing operations?
   - Are inputs properly validated and sanitized?
   - Are authentication and authorization checks in place?
   - Are there any potential vulnerabilities introduced?

4. **Performance**
   - Are database queries efficient (using select_related, etc.)?
   - Are there any N+1 query problems?
   - Is data fetched efficiently?
   - Are there any obvious performance bottlenecks?

5. **Testing**
   - Is the code covered by tests?
   - Are tests meaningful and not just for coverage?
   - Do tests test the right things (behavior, not implementation)?
   - Are tests maintainable and readable?

6. **Maintainability**
   - Is the code modular and loosely coupled?
   - Are dependencies clear and managed?
   - Is the code easy to modify and extend?
   - Are there any code smells or anti-patterns?

### Testing Pyramid for This Project
Apply the testing pyramid concept appropriately:

1. **Unit Tests (Foundation)**: 
   - Test individual functions, methods, and classes
   - Test model validation and business logic
   - Test utility functions and helpers
   - Aim for high coverage here (70-80% of tests)

2. **Integration Tests (Middle Layer)**:
   - Test view interactions with models
   - Test form processing and validation
   - Test template rendering with context data
   - Test API endpoint behavior
   - Moderate coverage (20-30% of tests)

3. **End-to-End Tests (Top)**:
   - Test complete user workflows
   - Test critical user journeys
   - Test cross-component interactions
   - Lower coverage but high value (5-10% of tests)
   - Consider using tools like Selenium Playwright for browser tests

### Continuous Integration Practices
For this project, consider setting up:

1. **Automated Testing on Push**:
   - Run tests on every push to repository
   - Fail builds on test failures
   - Provide fast feedback to developers

2. **Code Quality Checks**:
   - Run linters (flake8, pylint) on code changes
   - Check for security vulnerabilities (bandit, safety)
   - Enforce code formatting standards (black, isort)

3. **Dependency Management**:
   - Monitor for outdated packages
   - Check for known vulnerabilities in dependencies
   - Test upgrades in isolated environments

4. **Performance Monitoring**:
   - Track baseline performance metrics
   - Alert on significant performance degradations
   - Performance test in staging environments

### Specific Testing Tools for Django
Consider incorporating these tools:

1. **Testing Framework**:
   - Django's built-in TestCase (primary)
   - pytest-django for advanced features
   - Factory Boy for test fixtures
   - Faker for generating test data

2. **Code Quality**:
   - flake8 for style checking
   - black for code formatting
   - isort for import sorting
   - mypy for type checking (if adding type hints)
   - bandit for security linting

3. **Coverage Testing**:
   - coverage.py for measuring test coverage
   - Coverage reports in CI/CD pipelines

4. **Performance Testing**:
   - Locust or JMeter for load testing
   - Django Debug Quarter for development insights
   - New Relic or similar for production monitoring

## Test Data Management

### Fixtures vs Factories
For this project, consider using factories over static fixtures:

```python
# Using factory_boy for test data
import factory
from factory import fuzzy
from .models import Room, Contract

class RoomFactory(factory.DjangoModelFactory):
    class Meta:
        model = Room
    
    id = factory.Sequence(lambda n: f"P{100 + n}")
    name = factory.Faker('catch_phrase')
    area = fuzzy.FuzzyInteger(15, 50)
    price = fuzzy.FuzzyInteger(2000000, 5000000)
    status = Room.FREE

class ContractFactory(factory.DjangoModelFactory):
    class Meta:
        model = Contract
    
    id = factory.Sequence(lambda n: f"HD-{1000 + n:04d}")
    room = factory.SubFactory(RoomFactory)
    tenant_name = factory.Faker('name')
    tenant_id_card = factory.regex('[0-9]{12}')
    contract_date = factory.Faker('date_this_year')
    duration_months = fuzzy.FuzzyChoice([3, 6, 12])
```

### Test Data Strategies
1. **Isolation**: Each test gets fresh data or cleans up after itself
2. **Realism**: Use realistic data that mirrors production
3. **Consistency**: Same tests produce same results given same environment
4. **Performance**: Tests run quickly without excessive data creation
5. **Maintainability**: Easy to update test data patterns when needed

## Monitoring and Observability

### Logging Strategy
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Log meaningful contextual information
- Avoid logging sensitive data (passwords, personal info)
- Structure logs for easy parsing and analysis
- Use Django's logging configuration effectively

### Error Tracking
- Implement exception monitoring (Sentry, Rollbar, etc.)
- Capture stack traces and contextual information
- Set up alerting for error rate spikes
- Track errors by type, frequency, and impact
- Establish error resolution processes

### Performance Monitoring
- Track key metrics: response times, throughput, error rates
- Monitor database query performance
- Track cache hit/miss ratios
- Monitor resource usage (CPU, memory, disk, network)
- Set up baseline comparisons and anomaly detection

### Health Checks
- Implement application health endpoints
- Monitor critical dependencies (database, cache, external services)
- Provide detailed status information for debugging
- Integrate with orchestration platforms (Kubernetes, etc.)

## Release Quality Gates

### Pre-Release Checklist
Before releasing changes to this project, verify:

1. **All Tests Pass**:
   - Unit tests: 100% pass rate
   - Integration tests: 100% pass rate
   - Critical path tests: 100% pass rate
   - Performance tests: Within acceptable thresholds

2. **Quality Standards Met**:
   - Code review completed and approved
   - Linting passes with no new violations
   - Security scans show no new critical issues
   - Documentation updated as needed

3. **Compatibility Verified**:
   - Backward compatibility maintained (where required)
   - Database migrations tested and working
   - No breaking changes to public APIs without notice
   - Mobile/responsive behavior verified

4. **Production Readiness**:
   - Rollback plan prepared and tested
   - Monitoring and alerting configured
   - Release notes completed
   - Team notified and prepared for deployment

### Post-Release Validation
After releasing, verify:

1. **Deployment Success**:
   - Application starts and serves requests
   - Database migrations applied successfully
   - All services dependencies connected

2. **Smoke Testing**:
   - Core functionality working (login, navigation, etc.)
   - Critical paths functional (contract creation, viewing, etc.)
   - Basic error handling working

3. **Monitoring Indicators**:
   - Error rates at baseline levels
   - Performance metrics within norms
   - Resource usage patterns normal
   - No alert storms or cascading failures

4. **User Feedback**:
   - No immediate user-reported issues
   - Support ticket volume at normal levels
   - Positive feedback on new features (if applicable)

## Conclusion
Testing and quality assurance are ongoing practices that should be integrated throughout the development lifecycle. By following the approaches outlined in this skill, you can help ensure that the room rental contract management system remains reliable, maintainable, and valuable to its users over time.