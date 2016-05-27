"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
from flask import render_template

app = Flask(__name__, static_url_path="", static_folder="static")
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
#app.static_url_path('public')

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
#    return 'Hello World!'
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
