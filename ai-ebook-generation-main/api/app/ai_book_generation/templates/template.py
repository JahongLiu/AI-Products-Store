import json
import openai
import os
from app.ai_book_generation.util.retry import retry


class Template:
    def __init__(self, templates_file):
        self.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        self.templates = self.load_templates(templates_file)

    def load_templates(self, templates_file):
        try:
            with open(templates_file, "r") as file:
                templates_data = json.load(file)
            return templates_data
        except FileNotFoundError:
            print(f"Error: Config file '{templates_file}' not found.")
            return None
        except json.JSONDecodeError as e:
            print(
                "Error: Unable to parse JSON in config file"
                f" '{templates_file}': {e}"
            )
            return None

    @retry(max_retries=3)
    def choose_template(self, title, topic, target_audience):
        self.SYSTEM = (
            "You are an AI helping me create an ebook. Your goal is to provide"
            " be as helpful as possible in making decisions. Your responses"
            " will be used in a program script, so respond with no filler,"
            " just what it is asked."
        )
        self.CHAT_GPT_MODEL = os.environ.get("GPT_VERSION")

        template_prompt = (
            f'We are choosing a cover  an eBook. The ebook is titled "{title}"'
            f' Overall, it is about "{topic}". Our target audience is'
            f' "{target_audience}" \nWe have a few options for a cover'
            " template to use, each has tags associated with it. Given the"
            " following template name and tags, return the name of the most"
            " suitable cover template for our ebook as strictly the name. \n"
        )
        for name, vals in self.templates.items():
            tags = str(vals["tags"])
            template_prompt += f"Name: {name}, Tags: {tags}\n"

        print(template_prompt)
        response = openai.ChatCompletion.create(
            model=self.CHAT_GPT_MODEL,  # The ChatGPT model
            messages=[
                {"role": "system", "content": self.SYSTEM},
                {"role": "user", "content": template_prompt},
            ],
        )
        template_name = response.choices[0].message.content.strip()
        print(f"Chosen template name: {template_name}")
        return self.templates[template_name]
