# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

### Adding Trello API variables

To interact with the Trello API after cloning the .env file you need to change the following variables:

TRELLO_API_KEY: [Your API key](https://trello.com/app-key) in order to access the api 

TRELLO_API_TOKEN: [Your Api Token](https://trello.com/app-key) this autherises your login to access your boards

TRELLO_BOARD_ID : the ID of the board you are using. You can use the following API call to find the IDs of your boards


`Get https://api.trello.com/1/members/me/boards?fields=name,url&key={Your-Api-Key}&token={Your-Access-token}`

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the Tests

This project uses pytest to run the tests run:

```bash
$ poetry run pytest
```

this should discover and run all tests in the project. when adding a test please add the file to the tests folder with a _test suffix

## Running the App via Ansible on the VM

On the control node run

```
 ansible-playbook playbook.yml -i inventory --vault-id tbs@prompt
```

You will be prompted for the vault password

## Running the App using Docker

To run on the dev environment use:

```
docker-compose up
```

To run on the prod environment use:
```
docker build --target production --tag todo-app:prod .
docker run -p 3000:3000 --env-file .env todo-app:prod
```
