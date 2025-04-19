# Welcome to Cloud Functions for Firebase for Python!
# Deploy with `firebase deploy`

from firebase_functions import https_fn #version 0.1.2
from flask import Flask #version 3.1.0

app = Flask(__name__)

@app.route('/')
def hello_dw():
    return "Hello, Digital Wisdom!"

@https_fn.on_request(
    memory=512,
    timeout_sec=60,
    max_instances=1
)
def simple_function(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()
