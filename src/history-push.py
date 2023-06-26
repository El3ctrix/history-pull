from pathlib import Path
import platform
import subprocess
import socket
import json
import os

def get_history(rows):
    shell_type = None
    if platform.system() == 'Windows':
        shell_type = "Powershell"
        out_file = open('win_history.txt', 'w')
        subprocess.call('powershell.exe cat (Get-PSReadlineOption).HistorySavePath', stdout=out_file)
        out_file.close()
        #os.remove('win_history.txt')
    elif platform.system() == 'Linux':
        if(os.path.exists('{}/.bash_history'.format(str(Path.home())))):
            print('Bash')
            shell_type = "bash"
        elif(os.path.exists('{}/.zsh_history'.format(str(Path.home())))):
            print('Zsh')
            shell_type = "zsh"
    history_file = None
    if(shell_type == "Powershell"):
        history_file = open('win_history.txt', 'r')
    elif(shell_type == "bash"):
        history_file = open('{}/.{}_history'.format(str(Path.home()),'bash'), 'r')
    elif(shell_type == "zsh"):
        history_file = open('{}/.{}_history'.format(str(Path.home()),'zsh'), 'r')
    lines = history_file.readlines()
    total_lines = len(lines)
    if(rows > total_lines):
        rows = total_lines
    for line in lines[-(rows+1):(total_lines-1)]:
        print(line, end='')
    history_file.close()

def main():
    puller_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    puller_socket.bind(("localhost", 42297))
    puller_socket.listen(2)
    while True:
        puller, puller_address = puller_socket.accept()
        data = json.loads(puller.recv(1024).decode('utf-8'))
        if not data:
            break
        get_history(data['Rows'])

if __name__ == '__main__':
    main()
 