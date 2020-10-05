
Project
==========

> [admin page](https://one-acre.herokuapp.com/admin/)


## Running the application locally

clone the rep
```
$ git clone <repo-url>
```

create a virtual environment

```
$ python -m venv venv
```

activate the virtual environment

linux: `$source venv/bin/activate`

windows: `$venv/Scripts/activate `

run the application

`$ flask run`

setup environment variables. Add the following to your `.env` file.
You can omit `DATABASE_URL` if you opt to use the minimalistic `sqlite3` database
that comes with Python.

`DATABASE_URL=<DB_URL>`
`SECRET_KEY=<SECRET_KEY>`
`SENDGRID_API_KEY=<SENDGRID_API_KEY>`
