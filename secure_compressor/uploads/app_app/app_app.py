from flask import Flask, redirect, request, jsonify, render_template, url_for
import os
import logging
from config import Config
from auth.google_auth import google_bp 
from controller.chatgpt_controller import chatgpt_bp
from extensions import db, migrate
from flask_session import Session

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object(Config)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:.rlXI0}1mq}gf+(Gp$DGA7<%#-.7@172.18.0.2/studybeam"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = os.getenv("SECRET_KEY", "your-secure-key")
# Configure session to use the filesystem (or other backends)
app.config["SESSION_TYPE"] = "filesystem"  # Other options: 'redis', 'sqlalchemy'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_FILE_DIR"] = "./flask_session"  # Path to store session files (if using filesystem)

Session(app)

# Initialize the database and migrations
db.init_app(app)
migrate.init_app(app, db)

# Register blueprints
app.register_blueprint(google_bp, url_prefix="/google")
app.register_blueprint(chatgpt_bp, url_prefix="/chatgpt")

# Set up logging
logging.basicConfig(
    filename="application.log",  # Log file name
    level=logging.DEBUG,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
)

# Add a logger for Flask errors
logger = logging.getLogger("flask.app")
logger.setLevel(logging.DEBUG)

# Routes
@app.route("/")
@app.route("/login")
def index():
    app.logger.debug("Rendering login page.")
    return render_template("login.html")

@app.route("/callback")
def callback():
    app.logger.debug("Processing callback.")
    try:
        params = request.args.to_dict()
        redirect_uri = url_for("google_bp.auth_callback", _external=True, **params)
        app.logger.info(f"Redirecting to: {redirect_uri}")
        return redirect(redirect_uri)
    except Exception as e:
        app.logger.error(f"Error in callback: {str(e)}", exc_info=True)
        return jsonify({"error": "Callback processing failed", "details": str(e)}), 500

if __name__ == "__main__":
    with app.app_context():
        app.logger.info("Creating database tables if not already created.")
        db.create_all()
    app.logger.info("Starting Flask application.")
    app.run(debug=True)
