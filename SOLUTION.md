# Solution: Interaction Log Feature

## Feature Choice & Rationale
I implemented an **Interaction Log** feature for the CRM. This feature allows users to record important customer touchpoints such as calls, emails, meetings, and notes.

This adds practical CRM value because relationship history is essential for sales and account management workflows. It helps teams track communication, maintain context, and manage follow-up actions more effectively.

## What I Built

### Backend
- Added a new `Interaction` model
- Linked interactions to existing CRM records:
  - `Contact` (required)
  - `Company` (optional)
  - `Deal` (optional)
- Implemented full CRUD API with Django REST Framework
- Added validation for:
  - required contact
  - follow-up date must not be earlier than interaction date
  - company/deal consistency with selected contact
- Extended dashboard stats with interaction metrics
- Extended contact serialization with:
  - `interactions_count`
  - `last_interaction_date`

### Frontend
- Added a dedicated **Interactions** page
- Implemented full CRUD UI using Vue 3 + Vuetify
- Added:
  - searchable interaction list
  - card/table toggle
  - create/edit dialog
  - delete action
  - loading states
  - validation and error messaging
- Integrated the feature into app routing and sidebar navigation

## Improvements Added

### 1. Interaction Filters
I added filtering support on the Interactions page for:
- interaction type
- contact
- company
- follow-up status

This makes the feature more practical when the dataset grows, allowing users to quickly find relevant communication history.

### 2. Overdue Follow-up Indicators
I added clearer overdue follow-up indicators in the interactions UI.

This improves usability by helping users identify missed follow-up actions immediately instead of only storing the interaction as passive historical data.

### 3. Contact Interaction Summary
I integrated the feature into the Contacts page by showing:
- interaction count
- last interaction date
- a no-activity state when applicable

This makes the feature feel connected to the existing CRM workflow and helps users quickly assess relationship activity at the contact level.

## Design Decisions
- A contact is required because every interaction in a CRM should be tied to a person
- Company and deal are optional to keep the feature flexible
- I used interaction types (`call`, `email`, `meeting`, `note`) to support common CRM workflows
- Interactions are ordered by most recent interaction date to prioritize recent activity
- Follow-up visibility was emphasized because CRM data is most valuable when it drives action

## Files Changed

### Backend
- `backend/tasks/models.py`
- `backend/tasks/serializers.py`
- `backend/tasks/views.py`
- `backend/tasks/urls.py`
- `backend/tasks/tests.py`
- migration file for `Interaction`

### Frontend
- `frontend/src/services/api.js`
- `frontend/src/views/InteractionsView.vue`
- `frontend/src/views/ContactsView.vue`
- `frontend/src/router/index.js`
- `frontend/src/App.vue`

## Testing
I added API tests covering:
- successful interaction creation
- validation failure when subject is missing
- validation failure when follow-up date is before interaction date
- listing interactions
- updating interactions
- deleting interactions
- validation failure when contact is missing

## Setup Instructions

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver