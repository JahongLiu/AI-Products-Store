import uuid
import openai
import os
import requests


class GptWrapper:
    def __init__(self):
        self.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        openai.OPENAI_API_KEY = self.OPENAI_API_KEY
        self.CHAT_GPT_MODELS = [
            "gpt-3.5-turbo-1106",
            "gpt-3.5-turbo",
        ]
        self.GPT_MODEL_INDEX = 0
        self.CHAT_GPT_MODEL = self.CHAT_GPT_MODELS[self.GPT_MODEL_INDEX]
        self.convos = dict()

    def retry(func):
        def wrapper(self, *args, **kwargs):
            while self.GPT_MODEL_INDEX < len(self.CHAT_GPT_MODELS) - 1:
                try:
                    result = func(self, *args, **kwargs)
                    return result
                except Exception as e:
                    # We should make this specific to the model error code
                    print(f"An exception occurred: {e}")
                    print(
                        f"Switching to the next model in self.CHAT_GPT_MODELS"
                    )
                    self.GPT_MODEL_INDEX += 1
                    self.CHAT_GPT_MODEL = self.CHAT_GPT_MODELS[
                        self.GPT_MODEL_INDEX
                    ]
            else:
                raise Exception(
                    f"All models in self.CHAT_GPT_MODELS have been tried and"
                    f" exceeded"
                )

        return wrapper

    @retry
    def start_convo(self, system):
        convo_id = str(uuid.uuid4())
        self.convos[convo_id] = [
            {"role": "system", "content": system},
        ]
        return convo_id

    @retry
    def msg_in_convo(self, convo_id, prompt):
        self.convos[convo_id].append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model=self.CHAT_GPT_MODEL,
            messages=self.convos[convo_id],
        )
        text = response.choices[0].message.content.strip()
        self.convos[convo_id].append({"role": "assistant", "content": text})
        return text

    @retry
    def msg_in_convo_given_history(self, convo_id, messages):
        self.convos[convo_id] = messages
        response = openai.ChatCompletion.create(
            model=self.CHAT_GPT_MODEL,
            messages=messages,
        )
        text = response.choices[0].message.content.strip()
        self.convos[convo_id].append({"role": "assistant", "content": text})
        return text

    @retry
    def ask_question_in_convo(self, convo_id, question):
        question += "Answer with only a single word: 'True' or 'False'"
        self.convos[convo_id].append({"role": "user", "content": question})
        response = openai.ChatCompletion.create(
            model=self.CHAT_GPT_MODEL,
            messages=self.convos[convo_id],
        )
        text = response.choices[0].message.content.strip()
        response = True
        if text.lower() == "true":
            response = True
        elif text.lower() == "false":
            response = False
        else:
            raise Exception("Response is not a bool")
        self.convos[convo_id].append({"role": "assistant", "content": text})
        return response

    @retry
    def generate_photo(self, photo_prompt):
        improved_gpt_prompt = (
            f"A positive image of: {photo_prompt}, rendered artistically in a"
            " chic, cartooney, minimalistic style."
        )
        response = openai.Image.create(
            model="dall-e-3",
            prompt=improved_gpt_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        img_data = requests.get(image_url).content
        return img_data
