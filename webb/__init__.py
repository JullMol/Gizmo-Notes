from flask import Flask

def create_app():
    app = Flask(__name__)
    from .home import home
    from .timer import timer
    from .group import group
    from .todo import todo
    app.register_blueprint(home)
    app.register_blueprint(timer)
    app.register_blueprint(group)
    app.register_blueprint(todo)
    return app