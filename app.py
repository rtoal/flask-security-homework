from flask import (
    Flask, request, make_response, redirect, render_template, g, abort)
from user_service import get_user_with_credentials, logged_in
from account_service import get_balance, do_transfer
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)

# This is the secret key used by Flask to encrypt session cookies. It should
# not be in the code like this. Homework: get this from an environment
# variable.
app.config["SECRET_KEY"] = "yoursupersecrettokenhere"

# Without this line we would be vulnerable to CSRF attacks. In class we saw
# how to exploit this vulnerability to transfer money from one account to
# another without the user's consent. This line prevents that attack.
csrf = CSRFProtect(app)


@app.route("/", methods=["GET"])
def home():
    if not logged_in():
        return render_template("login.html")
    return redirect("/dashboard")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = get_user_with_credentials(email, password)
    if not user:
        return render_template("login.html", error="Invalid credentials")
    response = make_response(redirect("/dashboard"))
    response.set_cookie("auth_token", user["token"])
    return response, 303


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if not logged_in():
        return render_template("login.html")
    return render_template("dashboard.html", email=g.user)


@app.route("/details", methods=["GET"])
def details():
    if not logged_in():
        return render_template("login.html")
    account_number = request.args["account"]
    #
    # Homework: Validate that the account number is well-formed
    # (not too long, not too short, regex)
    #
    return render_template(
        "details.html",
        user=g.user,
        account_number=account_number,
        balance=get_balance(account_number, g.user))


@app.route("/transfer", methods=["GET"])
def transfer():
    if not logged_in():
        return render_template("login.html")
    return render_template("transfer.html")


@app.route("/transfer", methods=["POST"])
def make_transfer():
    if not logged_in():
        return render_template("login.html")
    source = request.form.get("from")
    target = request.form.get("to")
    #
    # Homework: Validate that the account numbers are well-formed
    #
    amount = int(request.form.get("amount"))
    #
    # Homework: Validate that the amount is well-formed and if not,
    # abort with a 400 error.
    #

    if amount < 0:
        abort(400, "NO STEALING")
    if amount > 1000:
        # Homework: You can be more creative than this.
        abort(400, "WOAH THERE TAKE IT EASY")

    available_balance = get_balance(source, g.user)
    if available_balance is None:
        abort(404, "Account not found")
    if amount > available_balance:
        abort(400, "You don't have that much")

    if do_transfer(source, target, amount):
        # Homework give feedback to the user that the transfer was successful.
        # You can do this by adding a message to the template and passing it
        # as a parameter. You may wish to mask certain values for privacy and
        # security.
        pass
    else:
        abort(400, "Something bad happened")

    response = make_response(redirect("/dashboard"))
    return response, 303


@app.route("/logout", methods=["GET"])
def logout():
    response = make_response(redirect("/dashboard"))
    response.delete_cookie("auth_token")
    return response, 303
