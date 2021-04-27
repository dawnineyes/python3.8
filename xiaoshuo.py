with open('a.txt', mode="r", encoding='utf-8') as f, open('b.txt', mode='w', encoding='utf-8') as result:  # 设置文件对象
    for line in f:
        if line.startswith('    '):
            line = line.lstrip(' ')
            line = line.rstrip('\n')
            result.write('    ' + line[::-1]+'\n')
        else:
            result.write(line)
