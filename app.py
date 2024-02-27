from flask import Flask
from views import views
from socketio_instance import socketio

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'juan'  # Add this line
    app.register_blueprint(views, url_prefix='/views')
    socketio.init_app(app)
    return app

app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)