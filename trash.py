"""
class poo(object) :

  def __init__(self):
    self.coutner = 0 

  
  def counter_incrament(self, foo_obj):

    self.coutner += 1
    foo_obj.counter += 2
    foo_obj.dict_shit["anan"] = self 



class foo(object) :
  
  def __init__(self):
    self.counter = 0
    self.dict_shit = {}


  def deneme(self):
    poo_obj = poo()

    poo_obj.counter_incrament(self)

    print(poo_obj.coutner)
    print(self.counter)
    print(f"Big Shit {self.dict_shit["anan"].coutner}")



foo_obj = foo()

foo_obj.deneme()

"""

import numpy as np
import cv2

img_file = open("img_480p_CAM_01_2024-05-17 13:06:53.265861.jpg",'rb')
data = img_file.read()
img_file.close()

img_array = np.frombuffer(data, dtype= np.uint8)
print(type(data))
print(img_array.shape)

img_array = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
# Show the image
cv2.imshow('image',img_array)
cv2.waitKey(0)