
# Secure Poke API


Full launch :

```bash
poetry shell

python manage.py migrate
python manage.py createsuperuser
python manage.py create_users
```

```bash
black api
ruff check . --fix
bandit -r app/
```