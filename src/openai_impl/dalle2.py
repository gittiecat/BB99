from enum import Enum
import os
import openai

class Size(Enum):
    SMALL="256x256"
    MEDIUM="512x512"
    LARGE="1024x1024"

class GenDallE2Class():
    def __init__(self):
        self.key = os.getenv("OPEN_AI_API_KEY")
    
    def generate(self, input, res, num):
        openai.api_key = self.key
    
        try:
            return openai.Image.create(
                prompt=input,
                n=int(num),
                size=self.get_size(res),
                response_format="b64_json"
            )
        except openai.error.InvalidRequestError as err:
            return str(err)

    def get_size(self, r):
        if (r == "small"):
            return Size.SMALL.value
        elif (r == "medium"):
            return Size.MEDIUM.value
        elif (r == "large"):
            return Size.LARGE.value
        else:
            return Size.MEDIUM.value
    
    