from flask import Flask, render_template, redirect, request

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, get_item, save_item, remove_item

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    items = sorted(items, key = lambda item: 1 if item["status"] == "Completed" else 0 )
    return render_template("index.html", items=items)

@app.route('/add-todo', methods=['POST'])
def add_todo():
    add_item(request.form.get("title"))
    return redirect("/")

@app.route('/remove-todo/<id>', methods=['POST'])
def remove_todo(id):
    remove_item(id)
    return redirect("/")

#I know this is the incorrect use of post but to use put I need to use JQuery for the form submission
@app.route('/mark-complete/<id>', methods=['POST'])
def mark_complete(id):
    item = get_item(id)
    item["status"] = "Completed"
    save_item(item)
    return redirect("/")