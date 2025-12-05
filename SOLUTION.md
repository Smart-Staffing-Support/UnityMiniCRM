# MiniCRM Take-Home Assessment

## Feature Choice & Product Rationale

When using the MiniCRM platform for the first time, I noticed a key usability gap: although the system tracks the number of companies, deals, and tasks created, it does not provide specific visibility into which company or deal was created, which contact is associated with a company, or which task was assigned to whom.

This lack of clarity can create uncertainty for new users(me). For example:

 - After creating a company, a user cannot immediately confirm that the company exists in the system.

 - When creating a deal, there is no instant feedback that it is linked correctly to a company or contact.

 - Task assignments are not clearly communicated, making it hard to track responsibilities.


 ---------


## Feature Choice

To address these issues, I implemented a **real-time notification and email system** that enhances user confidence, engagement, and transparency within MiniCRM.


## Product Rationale

This feature addresses key usability gaps:

 1. Users immediately know when a company, deal, or task has been successfully created.

 2. Users can view notifications without navigating away from the current page.

 3. Users can track activities in a chronological timeline, filtering by type and period for actionable insights.

 4. This improves CRM management by making actions visible and verifiable, fostering trust and reducing errors.


## Technical Overview

The solution includes:

 1. **Email Notifications:**

 - Sends emails to relevant parties when a *company or deal* is created, confirming that the action was successful.

 - Reinforces trust and communicates that agreements or partnerships are officially tracked in the system.

 2. **Frontend Notifications:**

 - Provides instant in-app feedback when a company, deal, or task is created.

 - Ensures users are aware of newly created records without needing to navigate away or manually check lists.

 3. **Activity Timeline with Filters:**

 - Captures all activities in a chronological timeline.

 - Allows users to *filter* events by type (company, deal, task) and period (daily, weekly, monthly) to get actionable insights and statistics.

 - Provides insights and statistics for tracking user activity and CRM engagement.



## Design Decisions

 - Used Django signals to trigger email notifications when backend objects are created.

 - Used Vue 3 reactive state for instant frontend notification updates.

 - Integrated a filterable timeline using computed properties and Vuetify components.

 - Ensured the notification bell updates dynamically with unread count.

 - Made UI responsive and accessible on desktop and tablet devices.

 - Prioritized minimal backend performance impact by sending emails asynchronously.



## Implementation Details

 1. **Backend:**

    - Added signal handlers for Company and Deal creation.

    - Email sending implemented via Django’s send_mail for asynchronous delivery.

    - Exposed API endpoints for activity timeline retrieval with filtering.

 2. **Frontend:**

    - Notification bell component shows unread count and dropdown with latest activities.

    - Badge notifications triggered immediately after creating companies, deals, or tasks.

    - Timeline component displays events, with chips for type filtering and a period dropdown.
    
 3. **Timeline Filtering:**

    - Computed property filters events by type and period.

    - Supports daily, weekly, and monthly views for analytics and monitoring.



## Challenges

 - Ensuring real-time updates without page reloads required careful use of reactive Vue state.

 - Handling email sending asynchronously to prevent blocking backend operations.

 - Maintaining consistent formatting and filtering in the timeline component.

 - Balancing frontend responsiveness with Vuetify styling constraints.

   **Current Bug / Limitation**

        - Notes are not separated per task: opening the notes dialog for any task sometimes shows notes from other tasks.

        - Editing or adding notes may not correctly trigger reactivity for that specific task.


## Time Breakdown

 | Task                                          | Approx. Time Spent |
| --------------------------------------------- | ------------------ |
| Backend: Django signals & email notifications | 6 hours            |
| Frontend: Notification bell & badge numbers   | 5 hours            |
| Frontend: Timeline component with filters     | 6 hours            |
| Testing (unit and integration)                | 4 hours            |
| Documentation & cleanup                       | 2 hours            |
| **Total**                                     | 23 hours           |



## Setup Instructions

1. **Clone the repository and checkout your feature branch:**
    - Follow the instructions in `SOLUTION.md` to set up both backend and frontend.

    ```git clone <your-fork-url>
        git checkout feature/real-time-notifications
    ```

2. **Install backend dependencies and run migrations:**
    ```pip install -r requirements.txt
        python manage.py migrate
    ```

3. **Start the backend server:**
    ```python manage.py runserver
    ```

4. **Install frontend dependencies:**
    ```cd frontend
        npm install
        npm run dev
    ```

## Testing Instructions

 1. Backend:
    - Run Django tests:

        ```
         python manage.py test tasks

        ```
    - **Backend tests include:**

    * Email sending on Company creation

    * Email sending on Deal creation

    * Timeline event creation for company/deal/task

    * Notification objects created and linked to timeline events

    * Unread notification default state


## Future Improvements

 - Add real-time push notifications via WebSockets for instant updates across multiple devices.

 - Allow users to customize notification preferences per event type.

 - Enable notifications for specific notes within a task, tracking conversations in each task until it is completed, helping to avoid overdue tasks.

 - Implement more advanced analytics in the timeline (charts, summaries, trends).

 - **Bug / To Fix:** Ensure notes are properly associated with each task so that adding or updating a note only affects the relevant task. 


## Trade-offs

 - Prioritized basic real-time notifications and timeline filtering over advanced analytics.

 - Email notifications are currently triggered synchronously in dev; in production, they should run via Celery or background tasks.

 - Timeline UI focuses on clarity and responsiveness over complex visualizations.


## Value Added:

- **Enhanced User Confidence:** Users immediately know their actions succeeded and can track specific entities.

- **Better Engagement:** Users receive confirmation of key CRM events, increasing trust and reducing errors.

- **Improved Tracking:** Users can visually see notifications and review the timeline, making CRM management more transparent and reliable.