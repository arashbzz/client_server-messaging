import socket
import threading
import json
import subprocess as sp
import platform

"""defining port and server IP."""

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

"""defining socket and connect to the socket"""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def json_maker(result, expre):
    sending_message = {}
    sending_message["given_math_expression"] = expre
    sending_message["result"] = result
    return json.dumps(sending_message)


"""response to the each client. """


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = conn.recv(1024).decode(FORMAT)
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
            if platform.system() == 'Windows':      # if os is windows, run powershell for using variable commands from client
                parameters.append('powershell.exe')
            parameters.append(msg["command_name"])
            parameters.extend(msg["parameters"])
            sending_message["given_os_command"] = parameters
            try:
                result = sp.run(parameters, capture_output=True, text=True)
                print(result.stderr)
                if result.stderr == '':
                    sending_message["result"] = result.stdout
                else:
                    sending_message["result"] = "The expression in not valid."
            except:
                sending_message["result"] = "The expression in not valid."

        sending_message = json.dumps(sending_message)
        conn.send(bytes(sending_message, encoding="utf-8"))
    print(f"[DISCONNECTION] {addr} disconnected.")
    conn.close()


"""  allocating a thread for each client. """


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        threads_number = threading.activeCount()
        print(f"[ACTIVE CONNECTIONS] {threads_number}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == '__main__':
    print("[STARTING] server is starting...")
    start()
