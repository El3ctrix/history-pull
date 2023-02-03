def history(platform, rows, type_of_shell='None'):
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