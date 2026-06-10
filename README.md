UnityMiniCRM
============

A full-stack CRM (Customer Relationship Management) application built with
Django REST framework with two different frontends: One using Vue and one using
React.


Tech Stack
----------

### Backend

- **Django 5.2** - Python web framework
- **Django REST Framework** - REST API toolkit on top of Django
- **SQLite** - Database

### Frontend (Vue)

- **Vue 3** - JavaScript web framework
- **Vuetify 3** - Material Design component library
- **Vue Router** - Client-side routing
- **Axios** - HTTP client
- **Vite** - Build tool and development server

### Frontend (React)

- **React** - JavaScript web framework
- **Tailwind** - CSS framework
- **Axios** - HTTP client
- **Vite** - Build tool and development server


Features
--------

- User authentication
- Dashboard with analytics and statistics
- Contact management (CRUD operations)
- Company management (CRUD operations)
- Deal tracking with pipeline stages
- Task management with priorities *(currently only in the Vue frontend)*


Development Notes
-----------------

- No TypeScript: Pure JavaScript codebases
- Token-based authentication with DRF's authtoken
- CORS headers configured for local development
- RESTful API architecture


Prerequisites
-------------

- Python 3.12+
- Node.js 18+ with *npm*


Setup
-----

To setup a specific backend/frontend, refer to its own `README.md`.


License
-------

This project is created for interview purposes.
