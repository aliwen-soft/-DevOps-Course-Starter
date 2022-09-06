FROM python:3.9-buster as base

RUN pip install "poetry==1.2.0"

WORKDIR /app

COPY poetry.lock pyproject.toml pytest.ini ./
RUN poetry config virtualenvs.create false --local && poetry install

COPY todo_app todo_app/

From base as production
EXPOSE $PORT
CMD poetry run gunicorn "todo_app.app:create_app()" -- bind 0.0.0.0:$PORT

From base as development
EXPOSE 5000
CMD ["poetry", "run", "flask", "run","--host", "0.0.0.0"] 

FROM base as test

CMD ["poetry", "run", "pytest"]