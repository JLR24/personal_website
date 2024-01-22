from flask import Flask, flash, render_template, redirect, url_for, request
from flask_mail import Mail, Message
from os import getenv

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = getenv("SECRET_KEY")

# Setup mailing
app.config.update(dict(
    DEBUG = False,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = getenv("EMAIL"),
    MAIL_PASSWORD = getenv("APP_PASSWORD"),
))
mail = Mail(app)


@app.route("/")
@app.route("/home")
def home():
    '''Displays the home page, which contains announcements.'''
    return render_template("home.html")


@app.route("/projects")
def projects():
    '''Displays a list of personal projects.'''
    return render_template("projects.html")


@app.route("/about")
def about():
    '''Provides some basic information as well as a contact form (handled by 'handle_contact').'''
    return render_template("about.html")


@app.route("/handle_contact", methods=["POST"])
def handle_contact():
    '''Handles the form submission when the user submits a query from the /about page.'''
    send_query(request.form.get("name"), request.form.get("email"), request.form.get("query"))
    return redirect(url_for("about"))


def send_query(name, email, query):
    '''This function sends the user's query as an email to my email address.'''
    try:
        # Define email details
        msg = Message(
            "Query from Personal Website",
            sender = ("Personal Website", getenv("EMAIL")),
            recipients = ["jack@ricketts.co.uk"]
        )
        # Only uses the body if the HTML file is unavailable
        msg.body = f"{name} ({email}): {query} [Error loading HTML file]"
        msg.html = render_template("send_query.html", name=name, email=email, query=query)
        mail.send(msg)
        flash("Your query has been received.")
    except:
        # If the process fails (most likely an account login failure)...
        flash("Unfortunately, we were unable to send your message at the minute. Please try again later.")


@app.errorhandler(404)
def page_not_found(error):
    flash("That page does not seem to exist! Redirecting to the home page...")
    return redirect(url_for("home"))

@app.errorhandler(Exception)
def handle_error(error):
    flash(f"Encountered an unknown error: {error}. Redirecting to the home page...")
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True) 