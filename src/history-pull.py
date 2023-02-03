from pathlib import Path
import subprocess
import sys
import platform
import os
import getopt


def retrieve_history(platform, rows, type_of_shell='None'):
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
        opts, args = getopt.getopt(argv, "hr:c:", ["rows=", "client="])
    except getopt.GetoptError:
        print('python3 history-pull.py -r <number of rows>')
        sys.exit(2)
    rows = 5
    client_specified = (len([item for item in opts if item[0] == '-c' or item[0] == '--client']) > 0)
    for opt, arg in opts:
        if(opt == '-h'):
            print('python3 history-pull.py -r <number of rows>')
            sys.exit()
        elif(opt in ('-r', '--rows')):
            if rows < 1:
                print('The total number of rows must be greater than 0')
                sys.exit(2)
            elif client_specified:
                print('The client option cannot be used with the rows option')
                sys.exit(2)
            rows = int(arg)
        elif(opt in ('-c', '--client')):
            pass
    if not client_specified:
        process_history(rows)
        


if __name__ == '__main__':
    main(sys.argv[1:])