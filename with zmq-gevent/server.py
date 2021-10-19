
from socket import socket
import zmq.green as zmq
import gevent 
import json
import subprocess as sp 

FORMAT = 'utf-8'
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
def handle_client ():
    
    while True:

        msg = socket.recv(1024).decode(FORMAT)
            # if msg == DISCONNECT_MESSAGE:
            #     connected = False
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
        socket.send(bytes(sending_message,encoding="utf-8"))

def start():
    greenlets =[]
    print (len(greenlets))
    greenlets.append(gevent.spawn(handle_client))
    gevent.joinall(greenlets)


print("[STARTING] server is starting...")
start()