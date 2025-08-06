# Contact Management API - Bruno Test Suite

This test suite provides comprehensive testing for the Contact Management API endpoints.

## Test Files Overview

The tests are organized in a logical sequence to test all CRUD operations:

### 1. Health Check

- **01-health-check.bru** - Tests the root endpoint to ensure the API is running

### 2. Create Operations

- **02-create-contact.bru** - Creates a new contact (John Doe)
- **03-create-contact-duplicate.bru** - Tests duplicate phone number validation
- **10-create-second-contact.bru** - Creates another contact (Alice Johnson)
- **15-create-contact-invalid.bru** - Tests validation with empty fields

### 3. Read Operations

- **04-get-all-contacts.bru** - Retrieves all contacts
- **05-get-contacts-paginated.bru** - Tests pagination with skip/limit parameters
- **06-get-contact-by-id.bru** - Gets a specific contact by ID
- **07-get-contact-not-found.bru** - Tests 404 error for non-existent contact

### 4. Update Operations

- **08-update-contact.bru** - Updates an existing contact
- **09-update-contact-not-found.bru** - Tests update on non-existent contact
- **11-update-contact-duplicate.bru** - Tests duplicate phone validation on update

### 5. Delete Operations

- **12-delete-contact.bru** - Deletes a contact
- **13-delete-contact-not-found.bru** - Tests delete on non-existent contact
- **14-verify-contact-deleted.bru** - Verifies the contact was actually deleted

## Environment Variables

The tests use these variables (automatically set/used):

- `url` - Base API URL (set in dev.bru environment)
- `contactId` - ID of the first created contact (set by test 02)
- `secondContactId` - ID of the second created contact (set by test 10)

## Running the Tests

1. Start the backend services:

   ```bash
   docker-compose up -d
   ```

2. Open Bruno and import this collection

3. Set the environment to "dev" which uses `http://localhost:8000`

4. Run all tests in sequence - they are numbered to run in the correct order

## Test Scenarios Covered

- ✅ Basic CRUD operations (Create, Read, Update, Delete)
- ✅ Input validation (empty fields)
- ✅ Business logic validation (duplicate phone numbers)
- ✅ Error handling (404 for non-existent resources)
- ✅ Pagination functionality
- ✅ Data persistence verification
- ✅ API response structure validation

## Expected API Behavior

The API should:

- Return 200 for successful operations
- Return 400 for business logic violations (duplicate phone)
- Return 404 for non-existent resources
- Return 422 for validation errors
- Maintain data integrity across operations
- Support pagination for listing endpoints
