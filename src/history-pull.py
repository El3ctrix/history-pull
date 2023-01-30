import subprocess
import platform
import os

def process_history():
    with open('history.txt', 'r') as history_file:
        lines = history_file.readlines()
        print(type(lines))

def main():
    if platform.system() == 'Windows':
        print('Windows')
        out_file = open('history.txt', 'w')
        subprocess.call('powershell.exe cat (Get-PSReadlineOption).HistorySavePath', stdout=out_file)
        process_history()
    elif platform.system() == 'Linux':
        print('Linux')
        if(os.path.exists('~/.bash_history')):
            subprocess.call('cat ~/.bash_history')
        elif(os.path.exists('~/.zsh_history')):
            subprocess.call('cat ~/.zsh_history')


if __name__ == '__main__':
    main()