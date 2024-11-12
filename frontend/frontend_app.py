"""
Flask application for the frontend of the Masterblog.

This module initializes a Flask web application and defines a single route to serve
the home page of the Masterblog frontend. The application renders the `index.html` template
when the user visits the root URL (`/`).

The application is configured to run on host `0.0.0.0` and port `5001`, with debugging enabled.
"""

from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """
    Render the home page of the Masterblog.

    This route serves the `index.html` page, which is the landing page for the Masterblog frontend.

    Returns:
        str: The rendered HTML content of the `index.html` template.
    """
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
