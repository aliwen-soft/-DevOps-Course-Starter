from flask import Flask, render_template, redirect, request

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, get_item, save_item

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    return render_template("index.html", items=items)

@app.route('/add-todo', methods=['POST'])
def add_todo():
    add_item(request.form.get("title"))
    return redirect("/")


#I know this is the incorrect use of post but to use put ill need to use JQuery
@app.route('/mark-complete/<id>', methods=['POST'])
def mark_complete(id):
    item = get_item(id)
    item["status"] = "Completed"
    save_item(item)
    return redirect("/")