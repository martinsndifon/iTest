## A sample api implementation as part of a 3 part interview process.

### Required Dependencies

- python 3.9+
- postgresql 16+

### Local dev setup

Clone and navigate to the project directory

```bash
git clone git@github.com:martinsndifon/iTest.git && cd iTest
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

```bash
./venv/Scripts/activate
```

Install requirements

```bash
pip install -r requirements.txt
```

#### Copy and edit environment variables - _important_

Create the database on your local postgres DB using credentials you edited in the .env file

If you already have postgres installed and running, you would only have to create a new database
with same name as the DB_NAME in the .env file

```bash
cp .env.sample .env
```

Navigate to the working directory (app)

```bash
cd app
```

Test database availability

```bash
python manage.py wait_for_db
```

If the database exist and has the correct connection permissions, the Expected output is

```bash
Waiting for database...
Database available!
```

If you don't get the above output, then "Waiting for database..." will be outputed repeatedly
because it tries to connect to the database every 1 second

```bash
Waiting for database...
Waiting for database...
Waiting for database...
Waiting for database...
...
```

You can use `ctrl C` to end the process and view the error logs.

Apply database migrations

```bash
python manage.py migrate
```

Run Tests

```bash
python manage.py test
```

Start server

```bash
python manage.py runserver
```

visit the swagger documentation ui at http://127.0.0.1:8000/api/docs

Quickly reach out if any issue(s) is encountered, Thank you.

Call/whatsapp - 08164404546

email - martinsndifon@gmail.com
