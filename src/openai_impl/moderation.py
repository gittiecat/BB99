import json
import os
import openai

class ModerationClass():
    def __init__(self):
        self.key = os.getenv("OPEN_AI_API_KEY")

    def moderate_message(self, message):
        openai.api_key = self.key

        try:
            response = openai.Moderation.create(
                input=message
            )
            return response["results"][0]
        except openai.error.InvalidRequestError as err:
            return str(err)

    def get_types(self, results):
        categories = results["categories"]
        json_obj = json.loads(str(categories))
        return [item for item in json_obj if json_obj[item] == True]
