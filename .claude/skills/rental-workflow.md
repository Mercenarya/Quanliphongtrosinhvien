# Rental Workflow Skill

This skill focuses on the specific business logic and workflows of the room rental contract management system.

## When to Use This Skill
Use this skill when:
- Implementing or modifying rental business logic
- Working with contract lifecycle management
- Handling room availability and allocation
- Implementing business rules specific to rental operations
- Validating rental domain constraints

## Skill Capabilities

### 1. Room Lifecycle Management
- Understand room status transitions (FREE ↔ RENTED)
- Implement proper room allocation logic
- Handle room maintenance and availability tracking
- Prevent double-booking through proper validation

### 2. Contract Lifecycle Management
- Manage contract creation, validation, and termination
- Handle contract durations and renewal logic
- Work with tenant information and identification
- Manage contract dates and terms

### 3. Business Rule Implementation
- Enforce rental policies and constraints
- Validate contract terms against business requirements
- Implement pricing calculations and total cost computations
- Handle late fees, deposits, and other financial aspects (if applicable)

### 4. Data Integrity and Consistency
- Maintain referential integrity between rooms and contracts
- Ensure proper cascading of status changes
- Prevent orphaned records and data inconsistencies
- Handle concurrent access scenarios properly

## Key Business Logic Patterns

### Room Allocation Workflow
1. **Check Availability**: Verify room status is FREE before contract creation
2. **Lock Resource**: Use database locking (select_for_update) to prevent race conditions
3. **Create Contract**: Create contract record with tenant information
4. **Update Status**: Change room status from FREE to RENTED
5. **Commit Transaction**: Ensure all operations succeed or fail together

### Contract Termination Workflow
1. **Load Contract**: Retrieve contract with related room information
2. **Validate Existence**: Ensure contract exists before deletion
3. **Delete Contract**: Remove contract record from database
4. **Update Status**: Change room status from RENTED to FREE
5. **Commit Transaction**: Ensure data consistency

### Contract Validation Rules
1. **Format Validation**: Contract ID must match HD-XXXX pattern
2. **Uniqueness**: Contract ID must be unique in the system
3. **Room Availability**: Target room must be in FREE status
4. **Tenant Information**: Name and ID card must be provided and valid
5. **Duration**: Must be one of allowed values (3, 6, or 12 months)
6. **Dates**: Contract date should be valid (typically current date)

## Domain-Specific Considerations

### Tenant Management
- ID card validation (9 or 12 digits for Vietnamese CMND/CCCD)
- Name formatting and validation
- Contact information handling (if extended in future)

### Contract Terms
- Fixed duration options: 3, 6, or 12 months
- Start date typically set to current date
- End date calculated from start date + duration
- Pricing: Monthly room price × duration (no discounts/taxes in current implementation)

### Room Attributes
- Area measurement in square meters
- Monthly pricing in Vietnamese Đồng (VND)
- Status tracking for availability management
- Room identification for tenant communication

## Implementation Guidelines

### When Modifying Workflow Logic
1. **Identify Trigger**: Determine what initiates the workflow (user action, system event)
2. **Map Steps**: break down the workflow into atomic operations
3. **Identify Dependencies**: Determine what resources or data are needed
4. **Consider Concurrency**: Plan for simultaneous access scenarios
5. **Define Rollback**: Establish what happens if part of the workflow fails
6. **Validate Inputs**: Check all preconditions before proceeding
7. **Ensure Consistency**: Verify postconditions after workflow completion

### Error Handling in Workflows
1. **Validation Errors**: Return clear, actionable feedback to users
2. **System Errors**: Log details for debugging while showing user-friendly messages
3. **Partial Failures**: Implement rollback mechanisms when possible
4. **Race Conditions**: Use database locking and retry logic where appropriate
5. **Edge Cases**: Handle boundary conditions and unusual scenarios

## Testing Considerations
1. **Positive Paths**: Test normal workflow execution
2. **Negative Paths**: Test validation failures and error conditions
3. **Edge Cases**: Test boundary values and unusual scenarios
4. **Concurrency**: Test simultaneous access scenarios
5. **Data Integrity**: Verify that related data remains consistent
6. **Performance**: Ensure workflows complete in reasonable time

## Project-Specific Validation Examples

### Contract Creation Validation
```python
# Check room exists and is available
room = Room.objects.select_for_update().filter(pk=room_id).first()
if room is None:
    return error("Room not found")
if room.status != Room.FREE:
    return error("Room already rented")

# Check for duplicate contract ID
if Contract.objects.filter(id=contract_id).exists():
    return error("Contract ID already exists")
```

### Contract Deletion Validation
```python
# Load contract with related data
contract = Contract.objects.select_related("room").select_for_update().filter(pk=contract_id).first()
if contract is None:
    return error("Contract not found")

# Perform deletion and status update in transaction
contract.delete()
contract.room.status = Room.FREE
contract.room.save()
```

## Integration Points

### With Frontend
- Form validation mirrors backend validation
- Error messages are consistent between client and server
- Loading states and user feedback are handled appropriately
- Success transitions update both contract and room views

### With Database
- All modifications occur within transactions
- Proper indexing for query performance
- Referential integrity maintained through foreign key constraints
- Efficient querying using select_related where appropriate

### With External Systems
- Current system is standalone but designed for extensibility
- Clear separation between business logic and presentation
- API endpoints follow consistent patterns for potential integration