import json
import requests
import os
import base64
from pdf2image import convert_from_path
import shutil
import datetime
from app.ai_book_generation.content.ebook import Ebook
from app.ai_book_generation.store.product_data_generator import (
    ProductDataGenerator,
)


class ShopifyGenerator:
    def __init__(
        self,
        SHOPIFY_ACCESS_TOKEN,
        SENDOWL_API_KEY,
        SENDOWL_API_SECRET,
        SHOP_NAME,
        PRODUCT_DATA_GENERATOR,
    ) -> None:
        self.SHOPIFY_ACCESS_TOKEN = SHOPIFY_ACCESS_TOKEN
        self.SENDOWL_API_KEY = SENDOWL_API_KEY
        self.SENDOWL_API_SECRET = SENDOWL_API_SECRET
        self.SHOP_NAME = SHOP_NAME
        self.PRODUCT_DATA_GENERATOR = PRODUCT_DATA_GENERATOR

    """ Main function for ShopifyGenerator. Adds an ebook as a product to Shopify store, with AI-generated fields (i.e. descriptions)"""

    def create_ebook_product(self, ebook, price):
        ebook.price = price
        product_data = self.generate_shopify_product_data(ebook)
        self.add_product_to_shopify(ebook, product_data)
        self.add_images_to_product(ebook)
        self.create_sendowl_product(ebook)

    def create_sendowl_product(self, ebook):
        files = {
            "product[name]": (None, ebook.title),
            "product[product_type]": (None, "digital"),
            "product[attachment]": open(ebook.pdf_file, "rb"),
            "product[shopify_variant_id]": (None, ebook.shopify_variant_id),
        }

        response = requests.post(
            "https://www.sendowl.com/api/v1/products.xml",
            files=files,
            auth=(self.SENDOWL_API_KEY, self.SENDOWL_API_SECRET),
        )
        if response.status_code == 200 or response.status_code == 201:
            print(response.text)
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
        return response

    """ Function to generated well-formed product data to be uploaded to Shopify """

    def generate_shopify_product_data(self, ebook):
        ebook.description = (
            self.PRODUCT_DATA_GENERATOR.generate_product_description(ebook)
        )
        ebook.tags = self.PRODUCT_DATA_GENERATOR.generate_product_tags(ebook)
        product_data = {
            "product": {
                "title": f"{ebook.title} (E-Book)",
                "body_html": ebook.description,
                "vendor": "N&J Publishing Co.",
                "product_type": "e-book",
                "published_scope": "global",
                "tags": ebook.tags,
                "status": "active",
                "variants": [
                    {
                        "title": "PDF",
                        "option1": "PDF",
                        "price": f"{ebook.price}",
                        "requires_shipping": "false",
                    },
                ],
                "options": [
                    {
                        "name": "Download Format",
                        "values": [
                            "PDF",
                        ],
                    },
                ],
            },
        }
        print(product_data)
        return product_data

    """ Function to make HTTP request to add product to Shopify """

    # https://shopify.dev/docs/api/admin-rest/2023-04/resources/product#post-products
    def add_product_to_shopify(self, ebook, product_data):
        headers = {
            "X-Shopify-Access-Token": self.SHOPIFY_ACCESS_TOKEN,
            "Content-Type": "application/json",
        }

        response = requests.post(
            f"https://{self.SHOP_NAME}.myshopify.com/admin/api/2023-04/products.json",
            headers=headers,
            json=product_data,
        )

        # Check if the request was successful
        if response.status_code == 201:
            print("Product added successfully!")
            print(json.dumps(response.json(), indent=4))
            create_response = response.json()
            # Update ebook data
            ebook.shopify_product_id = create_response["product"]["id"]
            ebook.shopify_variant_id = create_response["product"]["variants"][
                0
            ]["id"]
            return create_response

        else:
            print(
                f"Failed to add product. Status code: {response.status_code}"
            )
        return None

    def add_images_to_product(self, ebook):
        product_id = ebook.shopify_product_id
        current_time = datetime.datetime.now()
        time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        ebook.preview_dir = f"folder_{time_str}"
        try:
            os.mkdir(ebook.preview_dir)
        except:
            pass

        preview_count = 8
        self.create_preview_imgs(ebook, preview_count)

        headers = {
            "X-Shopify-Access-Token": self.SHOPIFY_ACCESS_TOKEN,
            "Content-Type": "application/json",
        }

        files = os.listdir(ebook.preview_dir)

        def numerical_part(filename):
            return int(filename.split(".")[0].lstrip("page"))

        sorted_files = sorted(files, key=numerical_part)

        for i, file_name in enumerate(sorted_files):
            img_file = os.path.join(ebook.preview_dir, file_name)
            if (
                img_file.endswith(".png")
                or img_file.endswith(".jpg")
                or img_file.endswith(".jpeg")
            ):
                print(img_file)
                with open(img_file, "rb") as image_file:
                    img_base64 = base64.b64encode(image_file.read())
                    json_data = {
                        "image": {
                            "position": i + 1,
                            "attachment": img_base64,
                            "filename": img_file,
                        },
                    }
                    response = requests.post(
                        f"https://{self.SHOP_NAME}.myshopify.com/admin/api/2023-07/products/{product_id}/images.json",
                        headers=headers,
                        json=json_data,
                    )
                    print(response.text)

        # Cleanup
        try:
            shutil.rmtree(ebook.preview_dir)
            print(
                f"Directory '{ebook.preview_dir}' and its contents have been"
                " removed successfully."
            )
        except FileNotFoundError:
            print(f"Directory '{ebook.preview_dir}' not found.")
        except Exception as e:
            print(
                f"An error occurred while trying to remove the directory: {e}"
            )

    """ Function to create preview images. Currently requires poppler """

    def create_preview_imgs(self, ebook, preview_count):
        pages = convert_from_path(ebook.pdf_file, 200)
        for i, page in enumerate(pages):
            if i <= preview_count:
                page.save(f"{ebook.preview_dir}/page{i}.jpg", "JPEG")


if __name__ == "__main__":
    sg = ShopifyGenerator(
        SHOPIFY_ACCESS_TOKEN=os.environ.get("SHOPIFY_ACCESS_TOKEN"),
        SENDOWL_API_KEY=os.environ.get("SENDOWL_API_KEY"),
        SENDOWL_API_SECRET=os.environ.get("SENDOWL_API_SECRET"),
        SHOP_NAME="fcfcec",
        PRODUCT_DATA_GENERATOR=ProductDataGenerator(
            OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")
        ),
    )
    # TODO: Automate 3d Mockups with python. Currently it is the cover of the book which seems okay
    ebook = Ebook(
        title=(
            "Retirement in Cupertino: The Ultimate Guide to Securing Your"
            " Dream"
        ),
        topic="planning retirement in Cupertino, California",
        target_audience="middle-aged men",
        pdf_file="mvp/cupertino_retirement_ebook.pdf",
        cover_img="mvp/cupertino_cover.png",
        assets=None,
        page_count=30,
    )
    sg.create_ebook_product(ebook, "0")
