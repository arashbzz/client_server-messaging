from socket import socket
import zmq.green as zmq
import gevent
from gevent.subprocess import run
import json
import platform

FORMAT = 'utf-8'
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

"""response to the each client. """


def handle_client():
    connected = True
    while connected:

        msg = socket.recv(1024).decode(FORMAT)
        msg = json.loads(msg)
        sending_message = dict()
        if msg["command_type"] == 'disconnect':
            connected = False

        elif msg["command_type"] == 'computing':
            sending_message["given_math_expression"] = msg["expression"]
            try:
                result = eval(msg["expression"])
                sending_message["result"] = result
            except:
                sending_message["result"] = "The expression is not valid."

        elif msg["command_type"] == 'os':

            parameters = list()
            if platform.system() == 'Windows':  # if os is windows, run powershell for using variable commands from client
                parameters.append('powershell.exe')
            msg["parameters"].pop(-1)
            parameters.append(msg["command_name"])
            parameters.extend(msg["parameters"])
            given_command = msg["command_name"]
            for para in msg["parameters"]:
                given_command += f' {para}'
            sending_message["given_os_command"] = given_command
            try:
                result = run(parameters, capture_output=True, text=True)
                print(result.stderr)
                if result.stderr == '':
                    sending_message["result"] = result.stdout
                else:
                    sending_message["result"] = "The expression in not valid."
            except:
                sending_message["result"] = "The expression in not valid."

        sending_message = json.dumps(sending_message)
        socket.send(bytes(sending_message, encoding=FORMAT))


if __name__ == '__main__':
    print("[STARTING] server is starting...")
    greenlets = []
    while True:
        greenlets.append(gevent.spawn(handle_client))
        gevent.joinall(greenlets)
