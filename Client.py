import asyncio
import cv2  as cv
import numpy as np
from datetime import datetime


class Parrent_Client(object): 

  def __init__(self,client_conn, client_addr, Is_connected):
    """
    @ Child_Client : Child client onject which is defined by its type 
    @ client_type : Define the our client type 
    @ Is_Init : Flag for Client Init Section 
    """

    # Hand Made Define
    self.Child_Client = None
    self.Is_Init : bool = False
    self.Is_connected : bool = Is_connected

    # Server Based Variable
    self.client_conn = client_conn
    self.client_port = client_addr[0]
    self.client_IP = client_addr[1]
    self.msg_decode_format = "utf-8"


    print(f"CLIENT : One Client Created IP : {self.client_IP}")

  def Msg_Hand(self, client_msg : bytes, server_obj) -> None : 


    if self.Is_Init : 
      
      self.Child_Client.Child_Client_Msg_Hand(client_msg, server_obj)

      
    else :

      splited_msg: list = client_msg.decode(self.msg_decode_format).split("_")
      print(f"CLIENT : Init msg {splited_msg}")
      print(f"CLIENT : Init msg zero {splited_msg[0]}")

      self.Is_Init = True 

      if 'INIT' in splited_msg: 

        if splited_msg[1] == "CAM" :

          print(f"CLIENT : Cam Init Start ")

          self.Child_Client = Camera_Client( camera_ID = str( splited_msg[1] + "_" + splited_msg[2] ) )
          server_obj.Dict_Client[self.Child_Client.camera_ID] = self
          server_obj.System_Status[self.Child_Client.camera_ID] = False
          
          

        
        elif splited_msg[1] == "DRLOCK" :

          self.Child_Client = Door_Lock_Client()
          server_obj.Dict_Client["DRLOCK"] = self
          
        elif splited_msg[1] == "BUZZER" : 
          self.Child_Client = Buzzer_Client()
          server_obj.Dict_Client["BUZZER"] = self    

        elif splited_msg[1] == "GASS" :
          self.Child_Client = Gas_Leak_Client()
          server_obj.Dict_Client["GASS"] = self

        if len(server_obj.Dict_Client) >= 5 : 

          server_obj.Dict_Flag["CAM_01"] = True
          server_obj.Dict_Flag["CAM_02"] = True
          server_obj.System_Status["DRLOCK"] = True
          server_obj.System_Status["BUZZER"] = True
          server_obj.System_Status["GASS"] = True

          #server_obj.Dict_Flag["CAM_03"] = True


class Camera_Client(object) : 

  def __init__(self, camera_ID) -> None:
    
    self.camera_ID = camera_ID
    self.img_msg_byte = b''
    self.open_cv_img = None

    print(f"CHILD CLIENT : One Camera Client Init {self.camera_ID}")
 
  def Child_Client_Msg_Hand(self, client_msg : bytes, server_obj):
    """
    That is the function we handle the image msg and 
    Send into Img progress function .
    """
    # print(f"{self.camera_ID} : MSG Recived by ")

    self.img_msg_byte += client_msg

    if(b'\xFF\xD9' == client_msg[-2:]):
      

      img_array = np.frombuffer(self.img_msg_byte, dtype= np.uint8)
      self.open_cv_img = cv.imdecode(img_array, cv.IMREAD_COLOR)
      
      if self.camera_ID == "CAM_02" :
        self.open_cv_img = server_obj.Face_Rec_Func(self.camera_ID,self.open_cv_img)

      else :
        self.open_cv_img = server_obj.Object_Recognition(self.camera_ID,self.open_cv_img)

      self.img_show(self.open_cv_img, self.camera_ID)
      
      self.img_msg_byte = b''

  def img_show(self, img_frame, cam_id):

    cv.imshow(cam_id, img_frame )
    self.img_msg_byte = b''

    if cv.waitKey(3) & 0xFF == ord('q'):
      cv.destroyWindow(cam_id)


  
class Door_Lock_Client(object) :

  def __init__(self) -> None:
    
    self.door_lock_status = False
    self.door_lock_wait_time = 3 # In a second
  
  async def Lock_Wait_Set(self, server_obj) : 
    server_obj.System_Status["Is_Dr_Lock_on_Wait"] = True
    await asyncio.sleep(self.door_lock_wait_time)
    server_obj.System_Status["Is_Dr_Lock_on_Wait"] = False

class Buzzer_Client(object) :

  def __init__(self) -> None:
    self.buzzer_status = False
    self.buzzer_wait_time = 1

  async def Buzzer_Wait_Set(self, server_obj) : 
    server_obj.System_Status["Is_Buzzer_on_Wait"] = True
    await asyncio.sleep(self.buzzer_wait_time)
    print("WAT SHOULD BE END s")
    server_obj.System_Status["Is_Buzzer_on_Wait"] = False

class Gas_Leak_Client(object):

  def __init__(self) -> None:
    self.Is_leak = False

  def Child_Client_Msg_Hand(self, client_msg, server_obj):

    if client_msg == b'1' :
      self.Is_leak = True
      server_obj.Dict_Flag["Is_Buzzer_On"] = True

    else :
      self.Is_leak = False
      server_obj.Dict_Flag["Is_Buzzer_On"] = False

    




