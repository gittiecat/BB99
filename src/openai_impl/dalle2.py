from enum import Enum
import os
import openai

class Size(Enum):
    SMALL="256x256"
    MEDIUM="512x512"
    LARGE="1024x1024"

class GenDallE2():
    def __init__(self):
        self.key = os.getenv("OPEN_AI_API_KEY")
    
    def generate(self, input, res=Size.MEDIUM.value):
        openai.api_key = self.key
        return openai.Image.create(
            prompt=input,
            n=1,
            size=res
        )