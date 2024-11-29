from flask import Flask

app = Flask(__name__)
def create_app():
    from .home import home
    from .timer import timer
    from .group import group
    from .todo import todo
    from .invite import invite
    app.register_blueprint(home)
    app.register_blueprint(timer)
    app.register_blueprint(group)
    app.register_blueprint(todo)
    app.register_blueprint(invite)
    return app