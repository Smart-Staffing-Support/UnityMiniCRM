UnityMiniCRM: Backend
=====================


Setup
-----

1. Create a virtual environment and activate it.

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
