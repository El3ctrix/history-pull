from pathlib import Path
import subprocess
import sys
import platform
import os
import getopt
import json

def add_client(name, ip):
    print('Add client')
    json_file = open('../clients.json', 'r+')
    json_data = json.load(json_file)
    item = {
        'Name': name,
        'IP': ip
    }
    if item not in json_data:
        json_data.append(item)    
        json_data = json.dumps(json_data, indent=4)
        json_file.seek(0)
        json_file.write(json_data)
    else:
        print('Client already exists')
    json_file.close()
    

def retrieve_history(platform, rows, type_of_shell='None'):
    #Falta agregar el nombre y direccion para poder obtener el historial
    pass

def process_history(rows):
    if platform.system() == 'Windows':
        out_file = open('win_history.txt', 'w')
        subprocess.call('powershell.exe cat (Get-PSReadlineOption).HistorySavePath', stdout=out_file)
        out_file.close()
        retrieve_history('Windows', rows)
        os.remove('win_history.txt')
    elif platform.system() == 'Linux':
        home = str(Path.home())
        if(os.path.exists('{}/.bash_history'.format(home))):
            retrieve_history('Linux', rows,'{}/.bash_history'.format(home))
        elif(os.path.exists('{}/.zsh_history'.format(home))):
            retrieve_history('Linux', rows,'{}/.zsh_history'.format(home), rows)

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hr:a:c:n:", ["rows=", "add=", "client=", "name="])
    except getopt.GetoptError:
        print('python3 history-pull.py -r <number of rows>')
        sys.exit(2)
    rows = None
    name = None
    ip = None
    add_specified = (len([item for item in opts if item[0] == '-a' or item[0] == '--add']) > 0)
    client_specified = (len([item for item in opts if item[0] == '-c' or item[0] == '--client']) > 0)
    name_specified = (len([item for item in opts if item[0] == '-n' or item[0] == '--name']) > 0)
    for opt, arg in opts:
        if(opt == '-h'):
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
            elif add_specified:
                print('The client option cannot be used with the rows option')
                sys.exit(2)
            elif name_specified:
                print('The name option cannot be used with the rows option')
                sys.exit(2)
        elif(opt in ('-a', '--add')):
            if client_specified:
                print('The client option cannot be used with the client option')
                sys.exit(2)
            elif rows != None:
                print('The client option cannot be used with the rows option')
                sys.exit(2)
            elif not name_specified:
                print('The name option cannot be used with the rows option')
                sys.exit(2)    
            ip = arg
        elif(opt in ('-n', '--name')):
            if not add_specified:
                print('The name option can only be used with the add option')
                sys.exit(2)
            elif rows != None:
                print('The name option can only be used with the add option')
                sys.exit(2)
            name = arg
        elif(opt in ('-c', '--client')):
            if add_specified:
                print('The client option cannot be used with the add option')
                sys.exit(2)
            elif name_specified:
                print('The name option cannot be used with the rows option')
                sys.exit(2)       
    if not add_specified and not name_specified:
        process_history(rows)
    if add_specified and name_specified:
        add_client(name, ip)


if __name__ == '__main__':
    main(sys.argv[1:])