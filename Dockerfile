FROM python:3.9-buster as base

RUN pip install "poetry==1.1.4"
COPY poetry.lock pyproject.toml .
RUN poetry install

COPY ./todo_app /todo_app/

From base as production
EXPOSE 3000
CMD ["poetry","run","gunicorn","-w","4","-b","0.0.0.0:3000","todo_app.wsgi:app"]

From base as development
EXPOSE 5000
CMD ["poetry", "run", "flask", "run","--host", "0.0.0.0"] 
