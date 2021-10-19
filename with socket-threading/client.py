import socket
import json

''' defining port and server IP'''
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)

''' definng socket and connect to the socket'''
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def send_json(json_file):
    client.send(bytes(json_file, encoding="utf-8"))
    print(f'[from server]: {client.recv(2048).decode(FORMAT)}')
    data_inputting()


def data_inputting():
    request_message = dict()
    command_type = input('Input the type of command: 1.compute 2.OS (1 or 2): ')
    if command_type == str(1):
        expression = input('Input expression: ')
        request_message["command_type"] = "computing"
        request_message["expression"] = expression

    elif command_type == str(2):
        command_name = input('Input command name: ')
        adding_parameter = True
        parameters = list()
        while adding_parameter:
            para = input('Input parameters of command: ')
            if para == '':
                adding_parameter = False
            parameters.append(para)
        request_message["command_type"] = "os"
        request_message["command_name"] = command_name
        request_message["parameters"] = parameters

    json_file = json.dumps(request_message)
    send_json(json_file)


if __name__ == '__main__':
    data_inputting()