
import socket
import threading

import Client as Client_Lib


class Server(object) : 

  def __init__(self):
    
    # Server Proporties Define
    self.header = 4096
    self.port = 120
    self.IPV4 = "192.168.124.42"
    self.server_addr = (self.IPV4, self.port)


    # Sub-System Status Flag
    self.Dict_Flag = {
      "Is_Buzzer_On" : False,
      "Is_Door_Locked" : True,
      "Is_Fire_Spring_On" : False,
    }

    self.Dict_Client = {}

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
      
      self.Dict_Flag = client_obj.Msg_Hand(recv_msg, self)

      print(f"SERVER : Server Clients {self.Dict_Client}")


Server_Obj = Server()













