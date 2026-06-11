# UnityMiniCRM Live Coding Exercise

## Overview

UnityMiniCRM is a simple CRM application with the following entities:

* Company
* Contact
* Deal
* Task

The project scaffolding has already been provided.

> Check out the `README.md` to familiarize yourself with the project structure and existing functionality.

For this task, you may choose either the **Vue** or **React** frontend implementation.

---

## Objective

Currently, creating a deal requires a user to:

1. Create a Company
2. Create a Contact
3. Create a Deal

You are required to replace this workflow with a single multi-step form wizard that allows users to create a Company, Contact, and Deal in one flow.

You will also create a Django REST Framework endpoint that accepts the combined payload and creates all related resources in the backend.

---

# Part 1: Frontend (Vue or React)

## Requirement

Create a multi-step form (wizard) for Deal Creation.

### Step 1: Company Information

Capture company details.

### Step 2: Contact Information

Capture contact details and associate them with the company being created.

### Step 3: Deal Information

Capture deal details and associate them with the company and contact.

> Check the available backend resources for expected fields, payload structure, and validation rules.

---

## UX Requirements

* Previous / Next navigation
* Validation on required fields
* Review all entered data before submission
* Disable submission while request is in progress
* Display success and error messages
* Prevent submission of invalid data

---

## Submission Payload

When the user submits the final step, send a single request to the backend containing all collected information.

The payload structure should be based on the backend models and validation requirements.

---

# Part 2: Backend (Django + DRF)

## Requirement

Create a Django REST Framework endpoint that accepts the combined payload and creates:

1. Company
2. Contact
3. Deal

in a single request.

---

## Business Rules

### Company

* Create the Company record.

### Contact

* Create the Contact record.
* Associate the Contact with the newly created Company.

### Deal

* Create the Deal record.
* Associate the Deal with:

  * the Company
  * the Contact

### Response

Return the created resources in the API response.

---

## Technical Expectations

### Frontend

* Component-based implementation
* Proper state management
* Clean form validation
* Reasonable UX decisions
* API integration
* Maintainable and readable code

### Backend

* DRF Serializer(s)
* View, ViewSet, or APIView
* Transaction handling (`transaction.atomic`)
* Validation of nested payloads
* Clean error responses
* Maintainable and readable code

---

# Bonus (Optional)

If time permits:
## Bonus 1

Persist each step of the wizard so that users can resume where they left off after a browser refresh, closure, or crash without losing previously entered data.

## Bonus 2

Allow searching for and selecting an existing Company instead of creating a new one.

## Bonus 3

Support both create and update operations using the same endpoint.

## Bonus 4

Add optimistic UI feedback and loading indicators.

## Bonus 5

Write at least one backend test covering the endpoint.

---

# Evaluation Criteria

We will evaluate:

* Code organization
* Django REST Framework knowledge
* Frontend architecture
* API design
* Validation strategy
* Error handling
* User experience considerations
* Communication and reasoning during implementation

---

## Notes

* Focus on delivering a working solution with clean, maintainable code.
* It is not necessary to implement every possible feature.
* If you make assumptions, document them clearly.
* Feel free to discuss trade-offs and design decisions during the session.
