from flask import Flask, render_template, redirect, request
from todo_app.flask_config import Config
from todo_app.data.db_items import get_items, change_item_status, add_item, remove_item
from todo_app.data.todo_item import TODO_STATUS, DONE_STATUS, DOING_STATUS
from todo_app.view_model import ViewModel
from todo_app.user.user import User, requireWriter, isWriter
from flask_login import LoginManager, login_required, login_user, current_user
import requests
from loggly.handlers import HTTPSHandler
from logging import Formatter

def set_up_logging(app):
    app.logger.setLevel(app.config['LOG_LEVEL'])
    
    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler( f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')

        handler.setFormatter(Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))

        app.logger.addHandler(handler)


def create_app():

    app = Flask(__name__)
    config = Config()
    app.config.from_object(config)

    login_manager = LoginManager()

    set_up_logging(app)
 
    @login_manager.unauthorized_handler
    def unauthenticated():
        app.logger.info("redirecting to github login")
        github_login = "https://github.com/login/oauth/authorize?client_id=" + config.CLIENT_ID
        return redirect(github_login)

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)

    @app.route('/')
    @login_required
    def index():
        items = get_items(config)
        items = sorted(items, key=lambda item: item.get_ordering_index())
        item_view_model = ViewModel(items)
        return render_template("index.html", item_view_model=item_view_model, isWriter=isWriter())

    @app.route('/login/callback')
    def user_log_in():
        code = request.args.get("code")

        data = {
            "client_id": config.CLIENT_ID,
            "client_secret": config.CLIENT_SECRET,
            "code": code
        }

        access_token_response = requests.post(
            "https://github.com/login/oauth/access_token", params=data, headers={"Accept": "application/json"})

        access_token_response = access_token_response.json()
        access_token = access_token_response['access_token']

        user_info_response = requests.get("https://api.github.com/user",
                                          headers={"Accept": "application/json", "Authorization": "Bearer {}".format(access_token)})

        user_info = user_info_response.json()

        app.logger.info("logging in as: %s", user_info["id"])

        user = User(user_info["id"])

        login_user(user)

        return redirect("/")

    @ app.route('/add-todo', methods=['POST'])
    @ login_required
    @ requireWriter
    def add_todo():
        app.logger.info("Adding Item %s ", request.form.get("title"))
        add_item(config, request.form.get("title"))
        return redirect("/")

    @ app.route('/remove-todo/<id>', methods=['POST'])
    @ login_required
    @ requireWriter
    def remove_todo(id):
        app.logger.info("Removing item with id %s", id)
        remove_item(config, id)
        return redirect("/")

    @ app.route('/mark-complete/<id>', methods=['POST'])
    @ login_required
    @ requireWriter
    def mark_complete(id):
        change_item_status(config, id, DONE_STATUS)
        return redirect("/")

    @ app.route('/mark-doing/<id>', methods=['POST'])
    @ login_required
    @ requireWriter
    def mark_doing(id):
        change_item_status(config, id, DOING_STATUS)
        return redirect("/")

    @ app.route('/mark-todo/<id>', methods=['POST'])
    @ login_required
    @ requireWriter
    def mark_todo(id):
        change_item_status(config, id, TODO_STATUS)
        return redirect("/")

    return app
