"""
routes.py specifies all the endpoints for the api
"""

from flask import Blueprint, request, jsonify
import os
from flask import Flask, jsonify, request
from flask import redirect
from app.health.health_service import Health
from app.ai_book_generation.runner import Runner
from app.ai_book_generation.saas.kafka.kafka_producer import KafkaProducer
from app.ai_book_generation.saas.stripe.stripe_handler import StripeHandler
from app.ai_book_generation.limiter.limiter import limiter
import uuid
from flask_cors import CORS, cross_origin
import time
import random


main = Blueprint("main", __name__, url_prefix="/api")
limiter.limit("10/second")(main)

stripe_handler = StripeHandler(
    os.environ.get("STRIPE_API_SECRET"),
    os.environ.get("STRIPE_ENDPOINT_SECRET"),
    os.environ.get("FRONTEND_URL"),
)

tasks = {}


def update_task_status(id, status, url=None):
    tasks[id] = {"status": status, "url": url}


@cross_origin
@main.route("/health", methods=["GET"])
def health():
    try:
        return Health().get_health(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    """
    Example request:
        curl -X 'GET' \
        'http://127.0.0.1:8000/health' \
        -H 'accept: application/json'
    """


@main.route("/runner_health", methods=["GET"])
def runner_health():
    try:
        return Runner().get_health(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    """
    Example request:
        curl -X 'GET' \
        'http://127.0.0.1:8000/runner_health' \
        -H 'accept: application/json'
    """


@main.route("/create_ebook", methods=["POST"])
def create_ebook():
    try:
        data = request.get_json()
        topic = data.get("topic")
        target_audience = data.get("target_audience")
        recipient_email = data.get("recipient_email")
        sell = data.get("sell")

        Runner().create_ebook(
            topic,
            target_audience,
            recipient_email,
            preview=False,
            sell=sell,
        )
        return (
            jsonify(),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@main.route("/create_ebook_preview", methods=["POST"])
def create_ebook_preview():
    try:
        data = request.get_json()
        topic = data.get("topic")
        target_audience = data.get("target_audience")

        id = str(random.getrandbits(32)) + str(time.time())
        tasks[id] = {"status": "processing", "url": None}
        Runner().create_ebook(
            topic,
            target_audience,
            recipient_email=None,
            preview=True,
            sell=False,
            callback=update_task_status,
            id=id,
        )

        return jsonify({"id": id})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


"""
curl -X POST -H "Content-Type: application/json" -d '{
    "topic": "Squirrels around the world",
    "target_audience": "mid-twenty year olds"
}' http://127.0.0.1:8000/create_ebook_preview
"""


@main.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        checkout_session = stripe_handler.create_checkout_session(request)
        return jsonify(redirect_url=checkout_session.url), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400


@main.route("/create-checkout-session-sell", methods=["POST"])
def create_checkout_session_sell():
    try:
        checkout_session = stripe_handler.create_checkout_session(
            request, sell=True
        )
        return jsonify(redirect_url=checkout_session.url), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400


@main.route("/session-status", methods=["GET"])
def session_status():
    try:
        checkout_session = stripe_handler.create_checkout_session()
        return jsonify(redirect_url=checkout_session.url), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@main.route("/stripe_webhooks", methods=["POST"])
def webhook():
    try:
        return stripe_handler.handle_webhook(request), 200
    except Exception as e:
        print("Error", str(e))
        return jsonify({"error": str(e)}), 400


@main.route("/check_status/<id>", methods=["GET"])
def check_status(id):
    task = tasks.get(id, None)
    if task:
        return jsonify({"status": task["status"]})
    else:
        return jsonify({"status": "not found"}), 404


"""
Example request:
curl -X 'GET' \
'http://127.0.0.1:8000/check_status/3713204e-e5d4-45b6-b7da-7eebbf47ba75' \
-H 'accept: application/json'
"""


@main.route("/get_pdf/<id>", methods=["GET"])
def get_pdf(id):
    task = tasks.get(id, None)
    if task and task["status"] == "completed":
        return jsonify({"file_url": task["url"]})
    return jsonify({"error": "PDF not ready"}), 400
