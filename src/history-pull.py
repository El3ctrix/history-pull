from pathlib import Path
import subprocess
import sys
import platform
import os
import getopt

def process_history(platform, rows, type_of_shell='None'):
    history_file = None
    if(platform == 'Windows'):
        history_file = open('win_history.txt', 'r')
    elif(platform == 'Linux'):
        history_file = open(type_of_shell, 'r')
    lines = history_file.readlines()
    total_lines = len(lines)
    if(rows > total_lines):
        rows = total_lines
    for line in lines[-(rows+1):(total_lines-1)]:
        print(line, end='')
    history_file.close()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hr:", ["rows="])
    except getopt.GetoptError:
        print('python3 history-pull.py -r <number of rows>')
        sys.exit(2)
    rows = 5
    for opt, arg in opts:
        if(opt == '-h'):
            print('python3 history-pull.py -r <number of rows>')
            sys.exit()
        elif(opt in ('-r', '--rows')):
            if rows < 1:
                print('The total number of rows must be greater than 0')
                sys.exit(2)
            rows = int(arg)
    if platform.system() == 'Windows':
        print('Windows')
        out_file = open('win_history.txt', 'w')
        subprocess.call('powershell.exe cat (Get-PSReadlineOption).HistorySavePath', stdout=out_file)
        out_file.close()
        process_history('Windows', rows)
        os.remove('win_history.txt')
    elif platform.system() == 'Linux':
        print('Linux')
        home = str(Path.home())
        if(os.path.exists('{}/.bash_history'.format(home))):
            process_history('Linux', rows,'{}/.bash_history'.format(home))
        elif(os.path.exists('{}/.zsh_history'.format(home))):
            process_history('Linux', rows,'{}/.zsh_history'.format(home), rows)
        


if __name__ == '__main__':
    main(sys.argv[1:])