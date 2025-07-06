import json
import logging
from datetime import datetime
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request

# Load .env variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Create Flask app
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

# Set up logging
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

# Register Auth0 with OAuth
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/login")
def login():
    app.logger.info(f"[LOGIN_ATTEMPT] Redirecting to Auth0 at {datetime.utcnow().isoformat()} from IP: {request.remote_addr}")
    return oauth.auth0.authorize_redirect(redirect_uri=url_for("callback", _external=True))


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token

    user_info = token.get("userinfo", {})
    user_id = user_info.get("sub")
    email = user_info.get("email")

    app.logger.info(f"[LOGIN_SUCCESS] user_id={user_id} email={email} timestamp={datetime.utcnow().isoformat()}")
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


@app.route("/")
def home():
    return render_template("home.html", session=session.get("user"), pretty=json.dumps(session.get("user"), indent=4))


@app.route("/protected")
def protected():
    if "user" not in session:
        app.logger.warning(f"[UNAUTHORIZED_ACCESS] Attempted access to /protected at {datetime.utcnow().isoformat()} from IP: {request.remote_addr}")
        return redirect("/login")

    user_info = session["user"].get("userinfo", {})
    user_id = user_info.get("sub")
    email = user_info.get("email")

    app.logger.info(f"[ACCESS_GRANTED] /protected accessed by user_id={user_id} email={email} timestamp={datetime.utcnow().isoformat()}")
    return render_template("protected.html", user=session["user"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(env.get("PORT", 3000)))
