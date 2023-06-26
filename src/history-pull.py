from pathlib import Path
import sys
import socket
import getopt
import json

def add_client(name, ip):
    json_file = open('clients.json', 'r+')
    json_data = json.load(json_file)
    new_item = {
        'Name': name.lower(),
        'IP': ip.lower()
    }
    exist = False
    for item in json_data:
        if name.lower() == item["Name"]:
            print("The name is already taken.")
            exist = True
            break
        elif ip.lower() == item["IP"]:
            print("This IP is already in another client.")
            exist = True
            break
    if not exist:
        json_data.append(new_item)    
        json_data = json.dumps(json_data, indent=4)
        json_file.seek(0)
        json_file.write(json_data)
        json_file.close()
    else:
        json_file.close()
        sys.exit(2)
    

def process_pull_petition(name, rows):
    #Formar peticion y pedir el historial
    json_file = open('clients.json', 'r')
    json_data = json.load(json_file)
    json_file.close()
    
    for client in json_data:
        if client['Name'] == name:
            print(client)
            pull_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            petition = {'Name': name, 'Rows': rows}
            pull_socket.connect((client['IP'], 42297))
            pull_socket.sendall(json.dumps(petition).encode('utf-8'))
            reply_json = json.loads(pull_socket.recv(1024).decode('utf-8'))
            print(reply_json)
            pull_socket.close()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "ha:r:i:n:", ["add=","rows=", "ip=", "name="])
    except getopt.GetoptError:
        # Necesito mejorar la explicacion de la explicacion
        print('python3 history-pull.py -r <number of rows>')
        sys.exit(2)
    rows = None
    name = None
    ip = None
    add_specified = (len([item for item in opts if item[0] == '-a' or item[0] == '--add']) > 0)
    ip_specified = (len([item for item in opts if item[0] == '-i' or item[0] == '--ip']) > 0)
    name_specified = (len([item for item in opts if item[0] == '-n' or item[0] == '--name']) > 0)
    for opt, arg in opts:
        if(opt in ('-h', '--help')):
            print('python3 history-pull.py -r <number of rows>')
            sys.exit()
        elif(opt in ('-r', '--rows')):
            if arg.isdigit():
                rows = int(arg)
            elif arg == 'all':
                rows = 'all'
            if rows != 'all' and rows < 1:
                print('The total number of rows must be greater than 0')
                sys.exit(2)
            if add_specified or ip_specified:
                print('There are invalid options.')
        elif(opt in ('-a', '--add')):
            if not ip_specified:
                print('ADD ERROR 1')
                sys.exit(2)
            elif rows != None:
                print('ADD ERROR 2')
                sys.exit(2)
            elif not arg:
                print('ADD ERROR 3')
                sys.exit(2)
            name = arg
            name_specified = True    
        elif(opt in ('-n', '--name')):
            if rows != None:
                print('NAME ERROR 1')
                sys.exit(2)
            name = arg
        elif(opt in ('-i', '--ip')):
            if not add_specified:
                print('IP ERROR 1')
                sys.exit(2)
            elif not name_specified:
                print('IP ERROR 2')
                sys.exit(2)     
            ip = arg  
    if not add_specified and not ip_specified:
        process_pull_petition(name, rows)
    if add_specified and name_specified and ip_specified:
        add_client(name, ip)


if __name__ == '__main__':
    main(sys.argv[1:])