
from PIL import Image
from io import BytesIO
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True



file = open("img_parital.txt", "rb")
img_one = file.read()
file.close()

file = open("PIC_100.jpg", "rb")
img_two = file.read()
file.close()


"""
for index in range(len(img_one)) : 
  
  if img_one[index] != img_two[index] : 
    print(f"Line diff start {index}")
    print(img_one[index])
    print("===================")
    print(img_two[index])
    print("=================")
    print(len(img_one[index]))
    print(len(img_two[index]))

    break

"""


file = open("dif_file3.txt", "wb")

for index in range(len(img_one)):

  if img_one[index] != img_two[index] : 
    print(f"Unmatch byte at {index} => img_one {img_one[index]} ||| img_two {img_two[index]} \n")
    break



print(len(img_one))
print(len(img_two))




