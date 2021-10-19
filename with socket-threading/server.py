import socket 
import threading
import json 
import subprocess as sp  

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
  
def json_maker (result, expre):
    sending_message = {}
    sending_message["given_math_expression"]= expre
    sending_message["result"]= result 
    return json.dumps(sending_message)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            msg = json.loads(msg)

            if msg["command_type"] == 'computing':
                sending_message = {}
                sending_message["given_math_expression"]= msg["expression"]
                try:
                    result = eval( msg["expression"])
                    sending_message["result"]= result
                except: 
                    sending_message["result"]="The expression in not valid."
                
            elif msg["command_type"] == 'os':
                sending_message = {}
                given_command = msg["command_name"]
                for i in msg["parameters"]:
                    given_command += f'  {i}' 
                print(given_command)

                sending_message["given_os_command"]= given_command
                try:
                    result = sp.getoutput(given_command )
                    sending_message["result"]= result 
                except: 
                    sending_message["result"]="The expression in not valid."
                    
            sending_message= json.dumps(sending_message)
            conn.send(bytes(sending_message,encoding="utf-8"))
   

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()