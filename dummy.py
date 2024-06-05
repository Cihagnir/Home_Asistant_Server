import time
import socket
import threading
import cv2  as cv
import numpy as np 
import PIL.Image as Image
from datetime import datetime

from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

header = 4096
port = 120
IPV4 = "192.168.1.148"
addr = (IPV4,port)
Server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Server.bind(addr)

door_lock = 0

counter = b'0'



def door_lock_message_sender(conn,ligt_status):

  print("--------- MSG SENDER---------")
  print(f"LIGTH STATUS ON FUNC {ligt_status}")

  conn.send(ligt_status)
  print("--------- MSG SENDED ---------")

  return door_lock

def raw_msg_handler(raw_list) : 
  print("-------------------- MSG HAND --------------------")
  image_array = [] 
  for val in raw_list :

    temp_var = [ int( val[:2], 16 ), int( val[2:4], 16 ) , int( val[4:], 16 )]
    image_array.append(temp_var)


  image_array = np.array(image_array)
  image_array = image_array.reshape((16,16,3))

  return image_array


def handle_client(conn, addr):

  print("-------------------- HAND LOOP --------------------")
  print(f"[NEW CONNECTION] {addr} connected")
  
  connected = True
  light_on = True

  while connected :
    
    if(light_on) :
      print(f"Ligth Sitt {light_on}")
      door_lock_message_sender(conn, b'10')
      light_on = not light_on
      print(f"Ligth Sitt {light_on}")


    else : 
      print(f"Ligth Sitt {light_on}")
      door_lock_message_sender(conn, b'01')
      light_on = not light_on
      print(f"Ligth Sitt {light_on}")



    time.sleep(3)



def start():
  Server.listen()
  while True:
    print("-------------------- MAIN LOOP --------------------")
    conn, addr = Server.accept()
    thread = threading.Thread(target=handle_client,args=(conn, addr))
    thread.start()



print("[STARTING] server is starting ... ")
start()