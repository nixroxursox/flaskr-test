import os
from flask import Flask
from db import close_db, init_db_command
from auth import bp
import blog

test_config = None


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
    )


if test_config is None:
    app.config.from_pyfile("config.py", silent=True)
else:
    app.config.from_mapping(test_config)
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.register_blueprint(bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

    # a simple page that says hello


@app.route("/hello")
def hello():
    return "Hello, World!"


create_app().run(debug=True, host="0.0.0.0")
