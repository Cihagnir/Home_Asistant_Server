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
IPV4 = "192.168.223.42"
addr = (IPV4,port)
Server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Server.bind(addr)


counter = 0



def door_lock_message_sender(msg, conn, last_state):

  if door_lock == 0 :
    door_lock = 1
  elif door_lock == 1 :
    door_lock = 0

  print("--------- MSG SENDER---------")
  print(msg)
  encoded_msg = msg.encode("utf8")
  msg_lenght = len(encoded_msg)
  send_lenght = str(msg_lenght).encode()
  send_lenght += b" " * (header - len(send_lenght))
  conn.send(encoded_msg)
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

def img_msg_handler(): 
  pass


def handle_client(conn, addr):

  print("-------------------- HAND LOOP --------------------")
  print(f"[NEW CONNECTION] {addr} connected")
  
  connected = True

  raw_msg = conn.recv(header)
  print(f"Raw msg {raw_msg}")

  temp = raw_msg.decode("utf-8") 
  print(f"Decoded Raw Msg {temp}")

  
  msg = b'1'
  print(f"sended msg {msg}")
  print(f"sended msg {msg[0]}")
  conn.send(msg)



  img_bytes = b''
  door_lock = 0
  

  while connected :


    raw_msg = conn.recv(header)
    print(f"Lenght of the photo is {raw_msg}")
    temp = int.from_bytes(raw_msg,"big")
    print(f"Lenght of the photo is {temp}")

    """
    img_bytes += raw_msg

    if(b'\xFF\xD9' == raw_msg[-2:]):
      

      file = open(f"img_480p_{datetime.now()}.jpg", "wb")
      file.write(img_bytes)
      file.close()

      print(f"LEN of total img in END {len(img_bytes)}")
      img_bytes = b''

    elif raw_msg == b'DISCONNECT':

        print("lol there")
        connected = False
        conn.close()
    """
def start():
  Server.listen()
  while True:
    print("-------------------- MAIN LOOP --------------------")
    conn, addr = Server.accept()
    thread = threading.Thread(target=handle_client,args=(conn, addr))
    thread.start()



print("[STARTING] server is starting ... ")
start()