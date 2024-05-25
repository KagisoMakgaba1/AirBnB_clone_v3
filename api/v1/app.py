#!/usr/bin/python3
'''Contains a Flask web application API.
'''

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from werkzeug.exceptions import NotFound
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown."""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Handler for 404 errors."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
