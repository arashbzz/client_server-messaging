import zmq
import json

context = zmq.Context()


socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
FORMAT = 'utf-8'

def send_json (json_file):
    
    socket.send(bytes(json_file,encoding="utf-8"))
    print(f'[from server]: {socket.recv(2048).decode(FORMAT)}')
    inputing_data()


def inputing_data ():
    commnad_type = input ('Input the type of command: 1.compute 2.OS (1 or 2): ')
    if commnad_type ==  str(1) :
        expression = input ('Input experession: ')
        request_message = {}
        request_message["command_type"] = "computing"
        request_message["expression"] = expression
        
    elif commnad_type == str(2):
        command_name = input ('Input command name: ')
        
        adding_parameter = True
        parameters=[]
        while adding_parameter :
            para = input ('Input parameters of command: ')
            if para == '':
                adding_parameter= False
            parameters.append(para)
           
        request_message = {}
        request_message["command_type"] = "os"
        request_message["command_name"] = command_name
        request_message["parameters"] = parameters
    json_file = json.dumps(request_message)
    send_json(json_file)

inputing_data()