import os
import time
from flask import jsonify
import random
from app.ai_book_generation.content.ebook_content_generator import (
    EBookContentGenerator,
)
from app.ai_book_generation.store.shopify_generator import ShopifyGenerator
from app.ai_book_generation.content.ebook import Ebook
from app.ai_book_generation.store.product_data_generator import (
    ProductDataGenerator,
)
from app.ai_book_generation.util.thread import threaded
from app.ai_book_generation.aws.s3 import S3
from app.ai_book_generation.aws.ses import SES
from app.ai_book_generation.saas.email.email import EmailTemplate
import platform
from app.ai_book_generation.util.retry import retry



S3_BUCKET = "ai-ebook"
SENDER = "nulllabsllc@gmail.com"
REGION = "us-east-1"
EBOOK_READY_EMAIL_SUBJECT = "Your AI-generated ebook is ready!"

"""
Main class
"""

NUM_CHAPTERS = 6
NUM_SUBSECTIONS = 4


class Runner:
    @threaded
    def get_health(self):
        return jsonify({"message": "I am healthy!"})

    @retry(max_retries=3)
    @threaded
    def create_ebook(
        self,
        topic,
        target_audience,
        recipient_email,
        preview=False,
        sell=False,
        callback=None,
        id=None,
        add_to_shop=False,
        num_chapters=NUM_CHAPTERS,
        num_subsections=NUM_SUBSECTIONS,
    ):
        if id == None:
            id = str(random.getrandbits(32)) + str(time.time())

        if platform.system() == "Windows":
            print("Using a Windows machine!")
            import pythoncom

            pythoncom.CoInitialize()

        current_directory = os.getcwd()
        print("Current working directory:", current_directory)
        start_time = time.time()

        if preview:
            output_directory = f"app/ai_book_generation/preview/"
        else:
            output_directory = f"app/ai_book_generation/output/"

        eg = EBookContentGenerator(
            templates_file="app/ai_book_generation/templates/templates.json",
            output_directory=output_directory,
            id=id,
            topic=topic,
            target_audience=target_audience,
            recipient_email=recipient_email,
        )
        ebook = eg.generate_ebook(
            topic, target_audience, id, num_chapters, num_subsections, preview
        )

        if recipient_email:
            s3 = S3(S3_BUCKET, REGION)
            ses = SES(SENDER, REGION)

            # if permissions don't work, we want to fail early
            s3.try_permissions()
            ses.try_permissions()

            print("Uploading to S3...")
            file_url = s3.upload_file(ebook.pdf_file, f"{id}.pdf")

            docx_url = None
            if sell:
                print("Uploading docx to S3...")
                docx_url = s3.upload_file(ebook.docx_file, f"{id}.docx")

            print(
                f"Sending email to {recipient_email} with file url: {file_url}"
            )
            ses.send_email(
                "nulllabsllc@gmail.com",
                EmailTemplate.get_subject(ebook.title),
                EmailTemplate.get_body(
                    ebook.title,
                    topic,
                    target_audience,
                    file_url,
                    id,
                    recipient_email,
                    docx_url=docx_url,
                ),
            )
            ses.send_email(
                recipient_email,
                EmailTemplate.get_subject(ebook.title),
                EmailTemplate.get_body(
                    ebook.title,
                    topic,
                    target_audience,
                    file_url,
                    id,
                    recipient_email,
                    docx_url=docx_url,
                ),
            )

        if add_to_shop:
            sg = ShopifyGenerator(
                SHOPIFY_ACCESS_TOKEN=os.environ.get("SHOPIFY_ACCESS_TOKEN"),
                SENDOWL_API_KEY=os.environ.get("SENDOWL_API_KEY"),
                SENDOWL_API_SECRET=os.environ.get("SENDOWL_API_SECRET"),
                SHOP_NAME="fcfcec",
                PRODUCT_DATA_GENERATOR=ProductDataGenerator(
                    OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")
                ),
            )
            sg.create_ebook_product(ebook, "0")

        if callback:
            s3 = S3(S3_BUCKET, REGION)
            ses = SES(SENDER, REGION)

            # if permissions don't work, we want to fail early
            s3.try_permissions()
            ses.try_permissions()

            print("Uploading to S3...")
            file_url = s3.upload_file(ebook.pdf_file, f"{id}.pdf")

            callback(id, "completed", file_url)

        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_minutes, elapsed_seconds = divmod(elapsed_time, 60)
        print(
            f"Elapsed time: {int(elapsed_minutes)} minutes and"
            f" {elapsed_seconds:.2f} seconds"
        )

        return {
            "message": (
                "Successfully created ebook!"
                f"Elapsed time: {int(elapsed_minutes)} minutes and"
                f" {elapsed_seconds:.2f} seconds"
            )
        }


if __name__ == "__main__":
    runner = Runner()
    runner.create_ebook(
        "History of Maori Culture, and what happened to the Natives of New Zealand",
        "25, Maori Culture, New Zealand History",
        "tweti0504@gmail.com"
    )
