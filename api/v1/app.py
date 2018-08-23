#!/usr/bin/python3
'''
    This module contains our entry point of our flask application.
'''
from flask import Flask, jsonify
from models import storage
from flask_cors import CORS
from api.v1.views import app_views
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views, url_prefix="/api/v1")
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(err):
    '''
        This will call the close method.
    '''
    storage.close()


@app.errorhandler(404)
def page_not_found_404(e):
    '''
        This will return 404 not found error.
    '''
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST")
    if host is None:
        host = "0.0.0.0"
    port = os.getenv("HBNB_API_PORT")
    if port is None:
        port = 5000
    else:
        port = int(port)
    app.run(host=host, port=port, threaded=True)
