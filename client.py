import socket

header = 2048
port = 120
format = "charmap"
server_ip = "192.168.1.114"
addr = (server_ip,port)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(addr)



def message_sender(msg):
    encoded_msg = msg.encode(format)
    msg_lenght = len(encoded_msg)
    send_lenght = str(msg_lenght).encode()
    send_lenght += b" " * (header - len(send_lenght))
    client.send(encoded_msg)

message_sender(str(243))

islisten = True
while islisten :
    msg = client.recv(header).decode(format)
    if len(msg) > 0 :        
        print(msg)
        islisten = False

message_sender("!DISCONNECT")

