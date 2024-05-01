import PIL.Image as Image
import io
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

file = open("image copy.txt", "rb")

data = file.read()

file.close()

data = bytearray(data)


img = Image.open(io.BytesIO(data))

img.show()


