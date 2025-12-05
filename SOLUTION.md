# MiniCRM Take-Home Assessment

## Feature Selection Background & Motivation

When I first interacted with the MiniCRM platform, I noticed several usability gaps that made the system feel less transparent and harder to navigate, especially for someone using it for the first time. Although the dashboard displays counts of companies, deals, and tasks, it does not provide deeper visibility into what was created or how items are connected.

The most noticeable gaps were:

1. **Lack of immediate confirmation:**
After creating a company, there was no direct indication that it had been successfully added.

2. **Unclear associations:**
When creating a deal, I could not instantly verify whether it was correctly linked to the intended company or contact.

3. **Task responsibility not clearly surfaced:**
Task assignments were not shown in a way that made it easy to understand who was responsible for what.

Together, these issues created friction and uncertainty — reducing confidence that actions were actually being processed or recorded correctly. For a CRM, where clarity and traceability are essential, this made the system feel less responsive than expected.

In addition to these visibility issues, I also noticed challenges in the overall user experience:

4. **No loading indicators:**
When submitting a company, deal, or task, the interface sometimes appeared completely unresponsive. This led me to click multiple times without realizing the request was still processing.

5. **Lack of error feedback:**
If something went wrong, there were no error alerts. Actions failed silently, leaving no clear explanation of what happened or what the user should do next.

For a new user, especially someone unfamiliar with backend response times, this uncertainty can quickly become confusing. Navigation became unpredictable, and it was hard to know whether actions were successful or if errors occurred.

These combined issues highlighted an important principle: a system is only as good as its simplest, core interactions. If the basic functionality — confirmation of actions, visible feedback, and clear associations, does not work reliably, it hinders solving larger, more complex problems.

This motivated me to implement a feature that reinforces user confidence, system feedback, and visibility of actions inside the CRM.


-----------


## Feature Choice

To address these issues, I implemented a **real-time notification and email system** that enhances user confidence, engagement, and transparency within MiniCRM.


## Product Rationale

This feature addresses key usability gaps:

 1. Users immediately know when a company and deal has been successfully created.

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

| Task                                                           | Approx. Time Spent |
| -------------------------------------------------------------- | ------------------ |
| Backend: Django signals & email notifications                  | 6 hours            |
| Frontend: Notification bell & badge numbers                    | 5 hours            |
| Frontend: Timeline component with filters                      | 6 hours            |
| Attempted task-specific note-taking feature (unsubmitted)*     | 4 hours            |
| Testing (unit and integration)                                 | 6 hours            |
| Documentation & cleanup                                        | 2 hours            |
| **Total**                                                      | 29 hours           |

\*I also spent time implementing a task-specific note-taking feature intended to help users track the progress of each task.  
   The idea was to maintain a conversation thread per task so issues could be flagged early, discussed, and resolved **before the task became overdue**.  
   This would help avoid delays and allow timely support or follow-up.  
   However, I encountered a bug where task-specific notes could not be isolated (all notes were returned regardless of task).  
   Due to time constraints and the feature not reaching a stable state, I did not include this part in the final submission.


## Setup Instructions

1. **Clone the repository and checkout your feature branch:**
    - Follow the instructions in `SOLUTION.md` to set up both backend and frontend.

    ```
        git clone https://github.com/mairura/UnityMiniCRM.git
        git checkout -b feature/email-notification-timeline

    ```

2. **Install backend dependencies and run migrations:**
    ```
        pip install -r requirements.txt
        python manage.py migrate

    ```

3. **Start the backend server:**
    ```
        python manage.py runserver

    ```

4. **Install frontend dependencies:**
    ```
        cd frontend
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

- **Better UX:** Loading states and error alerts prevent confusion and improve navigation for new users.