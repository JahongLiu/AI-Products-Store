from flask import jsonify


class Health:
    def get_health(self):
        response = jsonify({"message": "I am healthy!"})
        return response
