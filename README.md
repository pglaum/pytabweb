# PyRSS

## Setup

Before you start the program, you need to create the first user account.
Use the following command:

```shell
./cli.py --create-admin
```

Also, the database uri must be set.
For this you have to set the environment variables `SECRET_KEY` and
`DATABASE_URL`.

```
# Example flask env

FLASK_APP=app.py
FLASK_DEBUG=1
FLASK_ENV=development
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=1234

DATABASE_URL=sqlite:////home/user/pyrss/app.db
SECRET_KEY=a_secret_key
```

You can also set a postgres db or any other database that is supported by
SQLAlchemy.

A secret key can be generated with the following python snippet:

```python3
import secrets
print(secrets.token_hex(16))
```
