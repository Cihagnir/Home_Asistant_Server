import os
import socket
import cv2 as cv
import threading
import numpy as np
import face_recognition
from ultralytics import YOLO
from datetime import datetime

import Client as Client_Lib


class Server(object) : 

  def __init__(self):
    
    # Server Proporties Define
    self.header = 4096
    self.port = 120
    self.IPV4 = "192.168.223.42"
    self.server_addr = (self.IPV4, self.port)


    # Sub-System Status Flag
    self.Dict_Flag = {
      "Is_Buzzer_On" : False,
      "Is_Door_Locked" : True,
      "Is_Fire_Spring_On" : False,
      "Is_Cam_One_Started" : False,
      "Is_Cam_Two_Started" : False
    }

    # Face Recognition Defines 
    self.known_face_ID = []
    self.known_face_encoding = []
    self.face_confidence_threshold = 0.95
    self.known_face_dir = 'known_faces'

    # Object Detection 
    self.model = YOLO("yolo-Weights/yolov8n.pt")
    self.class_names = ["person", "dog", "cat"]
    self.object_confidence_threshold = 0.75

    self.Dict_Client = {}

    self.Known_Faces_Init()

    self.Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.Server.bind(self.server_addr)

    self.Server.listen()

    print("-------- SERVER START LISTENING -------- ")
    print(f"Server Addrs : {self.server_addr}")
    while True:

      client_conn, client_addr = self.Server.accept()

      client_thread = threading.Thread( target= self.Client_Handler, args=(client_conn, client_addr, True))

      client_thread.start()


  def Client_Handler(self, client_conn, client_addr, is_connected):

    client_obj = Client_Lib.Parrent_Client(client_conn, client_addr, is_connected)

    print(f"Connectoin Catch {client_obj.client_IP, client_obj.client_port}")    

    while( client_obj.Is_connected ) :
      
      recv_msg = client_obj.client_conn.recv(self.header)
      
      client_obj.Msg_Hand(recv_msg, self)

      self.Flag_Check_Function()



  def Face_Rec_Func(self, cam_ID, img_frame):

    face_locations = face_recognition.face_locations(img_frame)
    face_encodings = face_recognition.face_encodings(img_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

      matches = face_recognition.compare_faces(self.known_face_encoding, face_encoding)
      name = "Unknown"
      confidence = 0.0

      if True in matches:
        first_match_index = matches.index(np.max(matches))
        name = self.known_face_ID[first_match_index]
        confidence = np.max(matches)

      if confidence >= self.face_confidence_threshold:
        cv.rectangle(img_frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv.rectangle(img_frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv.FILLED)
        font = cv.FONT_HERSHEY_DUPLEX
        
        cv.putText(img_frame, f"{name} ({confidence:.2f})", (left + 6, bottom - 10), font, 1.0, (255, 255, 255), 1)
        
        self.Dict_Flag["Is_Door_Locked"] = False
      
      else:
        cv.rectangle(img_frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv.rectangle(img_frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv.FILLED)
        font = cv.FONT_HERSHEY_DUPLEX

        cv.putText(img_frame, "Unknown", (left + 6, bottom - 10), font, 1.0, (255, 255, 255), 1)
        
        self.Dict_Flag["Is_Door_Locked"] = False

      cv.imwrite(f"img_480p_{cam_ID}_{datetime.now()}.jpg",img_frame)

  def Object_Recognition(self, cam_ID, img_frame) : 

    results = self.model(img_frame, stream=True)

    for r in results:
        boxes = r.boxes
        classes = r.names

        for box in boxes:
            
            if box.conf[0] > self.object_confidence_threshold :
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                class_id = int(box.cls[0])
                class_name = classes[class_id]

                if class_name in self.class_names:
                    cv.rectangle(img_frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

                    org = (x1, y1 - 10)
                    font = cv.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 2

                    cv.putText(img_frame, f"{class_name} detected!", org, font, fontScale, color, thickness)

    cv.imwrite(f"img_480p_{cam_ID}_{datetime.now()}.jpg",img_frame)  



  def Flag_Check_Function(self):

    if self.Dict_Flag["Is_Cam_One_Started"] : 

      self.Dict_Client["CAM_01"].client_conn.send(b'1')
    
    if self.Dict_Flag["Is_Cam_Two_Started"] : 

      self.Dict_Client["CAM_02"].client_conn.send(b'1')

  def Known_Faces_Init(self):

    for file_name in os.listdir(self.known_face_dir): 
      file_path = os.path.join(self.known_face_dir,file_name)

      if os.path.isfile(file_path) : 

        image = face_recognition.load_image_file(file_path)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        face_loc = face_recognition.face_locations(image)

        if len(face_loc) > 0 : 

          face_encoding = face_recognition.face_encodings(image)[0]
          self.known_face_encoding.append(face_encoding)

          face_ID = os.path.splitext(file_name)[0]
          self.known_face_ID.append(face_ID)


Server_Obj = Server()













