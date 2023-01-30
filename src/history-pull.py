import subprocess
from pathlib import Path
import platform
import os

def win_process_history():
    with open('history.txt', 'r') as history_file:
        lines = history_file.readlines()
        print(type(lines))

def linux_process_history(type_of_shell):
    with open(type_of_shell, 'r') as history_file:
        lines = history_file.readlines()
        print(lines)

def main():
    if platform.system() == 'Windows':
        print('Windows')
        out_file = open('history.txt', 'w')
        subprocess.call('powershell.exe cat (Get-PSReadlineOption).HistorySavePath', stdout=out_file)
        win_process_history()
    elif platform.system() == 'Linux':
        print('Linux')
        home = str(Path.home())
        if(os.path.exists('{}/.bash_history'.format(home))):
            linux_process_history('{}/.bash_history'.format(home))
        elif(os.path.exists('{}/.zsh_history'.format(home))):
            linux_process_history('{}/.zsh_history'.format(home))
        


if __name__ == '__main__':
    main()