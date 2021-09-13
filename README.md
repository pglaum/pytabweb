# pytabweb

Guitar Pro tab viewer on the web.

## Installation

- download the repository
- download [fontawesome](https://fontawesome.com/) and put it into
  `web/static/fonts/fa`
- install sqlite3
- create a virtual env (`python3 -m venv venv`)
- create the .flaskenv file (see below)
- install python dependencies in the venv (`pip install -r requirements.txt`)

### .flaskenv

The flask env file can look like this

```shell
FLASK_APP=app.py
FLASK_DEBUG=0
FLASK_ENV=production
FLASK_RUN_HOST=127.0.0.1
FLASK_RUN_PORT=1234

DATABASE_URL=sqlite:////path/to/sqlite3.db
SECRET_KEY=some-secret-key

DATA_DIR=/path/to/where/you/want/to/store/the/tabs/
```