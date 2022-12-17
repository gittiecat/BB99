import base64
import io
from PIL import Image

class ImageProcessor():

    def create_image(data):
        path = "resources/tmp/image.jpg"
        decoded_data = base64.b64decode(data)
        binary_stream = io.BytesIO(decoded_data)

        image = Image.open(binary_stream)
        image.save(path)
        return path

