import cv2  as cv
import numpy as np

class Parrent_Client(object): 

  def __init__(self,client_conn, client_addr, Is_connected):
    """
    @ Child_Client : Child client onject which is defined by its type 
    @ client_type : Define the our client type 
    @ Is_Init : Flag for Client Init Section 
    """

    # Hand Made Define
    self.client_type = None
    self.Child_Client = None
    self.Is_Init : bool = False
    self.Is_connected : bool = Is_connected

    # Server Based Variable
    self.client_conn = client_conn
    self.client_port = client_addr[0]
    self.client_IP = client_addr[1]
    self.msg_decode_format = "utf-8"

    print(f"CLIENT : One Client Created IP : {self.client_IP}")


  def Msg_Hand(self, client_msg : bytes, server_obj) -> dict : 

    if self.Is_Init : 
      
      self.Child_Client.Child_Client_Msg_Hand(client_msg, server_obj)

      
    else :

      splited_msg: list = client_msg.decode(self.msg_decode_format).split("_")
      print(f"CLIENT : Init msg {splited_msg}")
      print(f"CLIENT : Init msg zero {splited_msg[0]}")
      
      if 'INIT' in splited_msg: 

        if splited_msg[1] == "CAM" :

          print(f"CLIENT : Cam Init Start ")

          self.Child_Client = Camera_Client( camera_ID = str( splited_msg[1] + "_" + splited_msg[2] ) )
          server_obj.Dict_Client[self.Child_Client.camera_ID] = self
          
          self.Is_Init = True 

          if len(server_obj.Dict_Client) == 2 : 

            server_obj.Dict_Flag["Is_Cam_One_Started"] = True
            server_obj.Dict_Flag["Is_Cam_Two_Started"] = True




class Camera_Client(object) : 

  def __init__(self, camera_ID) -> None:
    
    self.camera_ID = camera_ID
    self.img_msg_byte = b''

    print(f"CHILD CLIENT : One Camera Client Init {self.camera_ID}")
 

  def Child_Client_Msg_Hand(self, client_msg : bytes, server_obj):
    """
    That is the function we handle the image msg and 
    Send into Img progress function .
    """
    self.img_msg_byte += client_msg

    if(b'\xFF\xD9' == client_msg[-2:]):

      """
      file = open(f"img_480p_{self.camera_ID}_{datetime.now()}.jpg", "wb")
      file.write(self.img_msg_byte)
      file.close()
      """
      img_array = np.frombuffer(self.img_msg_byte, dtype= np.uint8)
      cv_img = cv.imdecode(img_array, cv.IMREAD_COLOR)

      if self.camera_ID == "CAM_01" :
        server_obj.Face_Rec_Func(self.camera_ID,cv_img)

      else :
        server_obj.Object_Recognition(self.camera_ID,cv_img)

      print(f"{self.camera_ID} :  of total img in END {len(self.img_msg_byte)}")
      self.img_msg_byte = b''

      
class Door_Lock_Client(object) :

  def __init__(self) -> None:
    pass
    

class Buzzer_Client(object) :

  def __init__(self) -> None:
    pass


class Fire_Valve(object):

  def __init__(self) -> None:
    pass




