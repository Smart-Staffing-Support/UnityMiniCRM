UnityMiniCRM: Backend
=====================


Setup
-----

1. Create a virtual environment and activate it:

```sh
python venv .venv
. .venv/bin/activate
```

2. Install the package:

```sh
pip install -e .
```

3. Migrate the database:

```sh
./manage.py migrate
```

4. Create a demo user:

```sh
./manage.py createsuperuser
```

5. Run the development server:

```sh
./manage runserver
```


API Endpoints
-------------

### Authentication

- `POST /api/auth/login`
- `POST /api/auth/logout`

### Dashboard

- `GET /api/dashboard/stats` - Get dashboard statistics

### Companies

- `GET /api/companies` - List all companies
- `POST /api/companies` - Create a new company
- `GET /api/companies/:id` - Get company details
- `PUT /api/companies/:id` - Update a company
- `DELETE /api/companies/:id` - Delete a company

### Contacts

- `GET /api/contacts` - List all contacts
- `POST /api/contacts` - Create a new contact
- `GET /api/contacts/:id` - Get contact details
- `PUT /api/contacts/:id` - Update a contact
- `DELETE /api/contacts/:id` - Delete a contact

### Deals

- `GET /api/deals` - List all deals
- `POST /api/deals` - Create a new deal
- `GET /api/deals/:id` - Get deal details
- `PUT /api/deals/:id` - Update a deal
- `DELETE /api/deals/:id` - Delete a deal

### Tasks

- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/:id` - Get task details
- `PUT /api/tasks/:id` - Update a task
- `DELETE /api/tasks/:id` - Delete a task


Database Models
---------------

### Company

- `name`, `industry`, `website`, `phone`, `email`, `address`, `notes`
- `created_at`, `updated_at`
- `created_by` (FK: `User`)

### Contact

- `first_name`, `last_name`, `email`, `phone`, `position`, `notes`
- `company` (FK: `Company`)
- `created_at`, `updated_at`
- `created_by` (FK: `User`)

### Deal

- `title`, `amount`, `stage`, `probability`, `expected_close_date`, `notes`
- `company` (FK: `Company`)
- `created_at`, `updated_at`
- `created_by` (FK: `User`)

### Task

- `title`, `description`, `status`, `priority`, `due_date`
- `contact` (FK: `Contact`), `deal` (FK: `Deal`)
- `created_at`, `updated_at`
- `created_by` (FK: `User`)
