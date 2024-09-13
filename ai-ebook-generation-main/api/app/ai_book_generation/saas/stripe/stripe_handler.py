from app.ai_book_generation.runner import Runner
import stripe
from flask import jsonify
import json


class StripeHandler:
    def __init__(
        self, STRIPE_API_SECRET, STRIPE_ENDPOINT_SECRET, FRONTEND_URL
    ):
        self.STRIPE_API_SECRET = STRIPE_API_SECRET
        self.STRIPE_ENDPOINT_SECRET = STRIPE_ENDPOINT_SECRET
        stripe.api_key = self.STRIPE_API_SECRET
        self.FRONTEND_URL = FRONTEND_URL

    def session_status(self, request):
        session = stripe.checkout.Session.retrieve(
            request.args.get("session_id")
        )
        return jsonify(
            status=session.status,
            customer_email=session.customer_details.email,
        )

    # https://stripe.com/docs/api/checkout/sessions/object
    def create_checkout_session(self, request, sell=False):
        try:
            data = request.get_json()
            topic = data.get("topic")
            target_audience = data.get("target_audience")
            product = stripe.Product.create(
                name=(
                    f"E-Book with topic: '{topic}' for target audience:"
                    f" '{target_audience}'"
                ),
            )
            print(product.id)
            unit_amount = 99
            if sell:
                unit_amount = 299
            price = stripe.Price.create(
                unit_amount=unit_amount,
                currency="usd",
                product=product.id,
                metadata={
                    "topic": topic,
                    "target_audience": target_audience,
                    "sell": sell,
                },
            )
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        "price": price.id,
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url=self.FRONTEND_URL + "/success",
                cancel_url=self.FRONTEND_URL + "?canceled",
            )
        except Exception as e:
            print(str(e))
            return str(e)

        return checkout_session

    # https://stripe.com/docs/payments/checkout/fulfill-orders
    def handle_webhook(self, request):
        print("Called Stripe Webhook")
        event = None
        payload = request.data
        sig_header = request.headers["STRIPE_SIGNATURE"]

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.STRIPE_ENDPOINT_SECRET
            )
        except ValueError as e:
            # Invalid payload
            raise e
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            raise e

        try:
            # Handle the checkout.session.completed event
            if event["type"] == "checkout.session.completed":
                payload_eval = json.loads(payload.decode("utf-8"))
                recipient_email = payload_eval["data"]["object"][
                    "customer_details"
                ]["email"]
                # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
                session = stripe.checkout.Session.retrieve(
                    event["data"]["object"]["id"],
                    expand=["line_items"],
                )
                line_items = session.line_items
                # There can only be one book per purchase currently, so right now
                # line items is just singular
                for line_item in line_items:
                    self.fulfill_order(line_item, recipient_email)
                return jsonify(
                    {"message": f"Successfully started fulfilling order(s)"}
                )
        except Exception as e:
            raise e

        return ""

    def fulfill_order(self, line_item, recipient_email):
        print("Fulfilling order:")
        print(line_item)
        topic = line_item["price"]["metadata"]["topic"]
        target_audience = line_item["price"]["metadata"]["target_audience"]
        sell = bool(line_item["price"]["metadata"]["sell"])
        runner = Runner()
        return runner.create_ebook(
            topic, target_audience, recipient_email, preview=False, sell=sell
        )
