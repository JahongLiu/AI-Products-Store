"""
app.py is the main runner of the api
"""

from flask_cors import CORS, cross_origin
import logging

from app import create_app
from flask import Flask

app = create_app()
CORS(
    app,
    resources={
        r"/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}
    },
)
app.config["CORS_HEADERS"] = "Content-Type"
app.logger.setLevel(logging.ERROR)
app.run(host="0.0.0.0", port=8000, debug=True)
