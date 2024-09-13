import boto3

""" Class for SES operations """


class SES:
    def __init__(self, sender, region):
        self.ses = boto3.client("ses", region_name=region)
        self.sender = sender

    def try_permissions(self):
        # Attempt to get the SES identity verification attributes
        # This operation doesn't change any settings, but will fail if credentials are not available
        self.ses.get_identity_verification_attributes(
            Identities=[
                self.sender,
            ]
        )

    def send_email(self, recipient, subject, body):
        email = {
            "Source": self.sender,
            "Destination": {
                "ToAddresses": [
                    recipient,
                ],
            },
            "Message": {
                "Subject": {
                    "Data": subject,
                },
                "Body": {
                    "Text": {
                        "Data": body,
                    }
                },
            },
        }

        self.ses.send_email(**email)
