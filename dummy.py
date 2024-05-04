
from PIL import Image
from io import BytesIO
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True



for val in range(1,11):

  file = open(str(1)+".txt", "rb")
  data = file.read()
  file.close()

  print(b'JFIF' in data)

  index_info = data.index(b'JFIF')

  data = data[index_info-6:]

  print(data[:100])
  #image = Image.open(BytesIO(data))

  #image.show()
