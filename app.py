from flask import Flask, render_template
from config import Config
from extensions import db, bcrypt, jwt
from auth import auth
from tasks import task

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(task, url_prefix="/")

with app.app_context():
    db.create_all()
