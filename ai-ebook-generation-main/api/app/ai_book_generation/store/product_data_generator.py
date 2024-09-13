import openai
import os


class ProductDataGenerator:
    def __init__(self, OPENAI_API_KEY) -> None:
        self.OPENAI_API_KEY = OPENAI_API_KEY
        openai.api_key = self.OPENAI_API_KEY
        self.SYSTEM = (
            "You are a marketing agent creating descriptions within a website"
            " for ebooks. Your goal is enable the most sales possible."
        )
        self.CHAT_GPT_MODEL = os.environ.get("GPT_VERSION")

        """ Helper function to generate the ebook product description """

    def generate_product_description(self, ebook):
        description_prompt = (
            "We are adding a new eBook to our store. The eBook is named"
            f' "{ebook.title}". Overall, it is about "{ebook.topic}". Our'
            f' target audience is "{ebook.target_audience}". The eBook has a'
            f" total of {ebook.page_count} pages. The ebook includes"
            " well-researched statistics and simple actionable steps the"
            " reader can follow. Write the product description for a new"
            " eBook. Write the description in a concise and convincing way."
            " You should exploit the problems and fears our target audience"
            " has, and describe how this ebook can solve these for our target"
            " audience. The description should begin with a hook that will"
            " grab reader's attention. Keep a professonal salesperson tone,"
            " and do not to mention the target audience explicitly. Limit the"
            " total word count to at most 150 words."
        )

        response = openai.ChatCompletion.create(
            model=self.CHAT_GPT_MODEL,  # The ChatGPT model
            messages=[
                {"role": "system", "content": self.SYSTEM},
                {"role": "user", "content": description_prompt},
            ],
        )
        description = response.choices[0].message.content.strip()
        return description

    def generate_product_tags(self, ebook):
        tags_prompt = (
            "We are adding a new eBook to our store. The eBook is named"
            f' "{ebook.title}". Overall, it is about "{ebook.topic}". Our'
            f' target audience is "{ebook.target_audience}". We need to add a'
            " list of tags to our product site for the ebook. Please list"
            " relevant tags, given the context in a comma separated list. For"
            ' example: "Tag 1, Tag 2, Tag 3]"'
        )

        response = openai.ChatCompletion.create(
            model=self.CHAT_GPT_MODEL,  # The ChatGPT model
            messages=[
                {"role": "system", "content": self.SYSTEM},
                {"role": "user", "content": tags_prompt},
            ],
        )
        tags = response.choices[0].message.content.strip()
        return tags
