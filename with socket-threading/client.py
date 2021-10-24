import socket
import json
import sys

"""defining port and server IP."""
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())  # for using the current ip
ADDRESS = (SERVER, PORT)

"""defining socket and connect to the socket"""
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

""" making a json file and send it to the server"""


def send_json(json_file):
    client.send(bytes(json_file, encoding=FORMAT))
    print(f'[from server]: {client.recv(2048).decode(FORMAT)}')
    inputting_data()

def disconnet_connection():
    request_message = dict()
    request_message["command_type"] = "disconnect"
    json_file = json.dumps(request_message)
    client.send(bytes(json_file, encoding=FORMAT))
    sys.exit()

"""for inputting data by client in dictionary format. """


def inputting_data():
    request_message = dict()
    command_type = input('Input the type of command: 1.compute 2.OS 3.exit (1 , 2 or 3): ')
    if command_type == str(1):
        expression = input('Input expression: ')
        request_message["command_type"] = "computing"
        request_message["expression"] = expression

    elif command_type == str(2):
        command_name = input('Input command name: ')
        adding_parameter = True
        parameters = list()
        while adding_parameter:
            para = input('Input command parameters, or press enter to end.: ')
            if para == '':
                adding_parameter = False
            parameters.append(para)
        request_message["command_type"] = "os"
        request_message["command_name"] = command_name
        request_message["parameters"] = parameters
    elif command_type == str(3):
        disconnet_connection()
    else:
        print('please select only between 1, 2 and 3.')
        inputting_data()

    json_file = json.dumps(request_message)
    send_json(json_file)


if __name__ == '__main__':
    inputting_data()
