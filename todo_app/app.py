import imp
from flask import Flask, render_template, redirect, request
from todo_app.flask_config import Config
from todo_app.data.db_items import get_items, change_item_status, add_item, remove_item
from todo_app.data.todo_item import TODO_STATUS, DONE_STATUS, DOING_STATUS
from todo_app.view_model import ViewModel
from flask_login import LoginManager, login_required
import requests


def create_app():

    app = Flask(__name__)
    config = Config()
    app.config.from_object(config)

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        github_login = "https://github.com/login/oauth/authorize?client_id=" + config.CLIENT_ID
        return redirect(github_login)

    @login_manager.user_loader
    def load_user(user_id):
        pass  # We will return to this later

    login_manager.init_app(app)

    @app.route('/')
    @login_required
    def index():
        items = get_items(config)
        items = sorted(items, key=lambda item: item.get_ordering_index())
        item_view_model = ViewModel(items)
        return render_template("index.html", item_view_model=item_view_model)

    @app.route('/login/callback')
    def user_log_in():
        code = request.args.get("code")

        data = {
            "client_id": config.CLIENT_ID
        }

        access_token_response = x = requests.post(
            "https://github.com/login/oauth/access_token")

        print(code)

        return redirect("/ah")

    @app.route('/add-todo', methods=['POST'])
    @login_required
    def add_todo():
        add_item(config, request.form.get("title"))
        return redirect("/")

    @app.route('/remove-todo/<id>', methods=['POST'])
    @login_required
    def remove_todo(id):
        remove_item(config, id)
        return redirect("/")

    @app.route('/mark-complete/<id>', methods=['POST'])
    @login_required
    def mark_complete(id):
        change_item_status(config, id, DONE_STATUS)
        return redirect("/")

    @app.route('/mark-doing/<id>', methods=['POST'])
    @login_required
    def mark_doing(id):
        change_item_status(config, id, DOING_STATUS)
        return redirect("/")

    @app.route('/mark-todo/<id>', methods=['POST'])
    @login_required
    def mark_todo(id):
        change_item_status(config, id, TODO_STATUS)
        return redirect("/")

    return app
