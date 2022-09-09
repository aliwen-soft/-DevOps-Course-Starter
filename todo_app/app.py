from flask import Flask, render_template, redirect, request
from todo_app.flask_config import Config
from todo_app.data.db_items import get_items, change_item_status, add_item, remove_item
from todo_app.data.todo_item import TODO_STATUS, DONE_STATUS, DOING_STATUS
from todo_app.view_model import ViewModel


def create_app():

    app = Flask(__name__)
    config = Config()
    app.config.from_object(config)

    @app.route('/')
    def index():
        items = get_items(config)
        items = sorted(items, key=lambda item: item.get_ordering_index())
        item_view_model = ViewModel(items)
        return render_template("index.html", item_view_model=item_view_model)

    @app.route('/add-todo', methods=['POST'])
    def add_todo():
        add_item(config, request.form.get("title"))
        return redirect("/")

    @app.route('/remove-todo/<id>', methods=['POST'])
    def remove_todo(id):
        remove_item(config, id)
        return redirect("/")

    @app.route('/mark-complete/<id>', methods=['POST'])
    def mark_complete(id):
        change_item_status(config, id, DONE_STATUS)
        return redirect("/")

    @app.route('/mark-doing/<id>', methods=['POST'])
    def mark_doing(id):
        change_item_status(config, id, DOING_STATUS)
        return redirect("/")

    @app.route('/mark-todo/<id>', methods=['POST'])
    def mark_todo(id):
        change_item_status(config, id, TODO_STATUS)
        return redirect("/")

    return app
