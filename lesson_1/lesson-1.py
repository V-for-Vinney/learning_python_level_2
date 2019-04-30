print('Задание 1:')
words_1 = ['разработка', 'сокет', 'декоратор']
print('типы:', ', '.join([str({w: type(w)}) for w in words_1]))
unicode_words_1 = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
                   '\u0441\u043e\u043a\u0435\u0442',
                   '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']
print('типы:', ', '.join([str({w: type(w)}) for w in unicode_words_1]))


print('\nЗадание 2:')
words_2 = [b'class', b'function', b'method']
print('длины:', ', '.join([str({w: len(w)}) for w in words_2]))


print('\nЗадание 3:')
words_3 = ['attribute', 'класс', 'функция', 'type']
for w in words_3:
    try:
        w.encode('ascii')
        print(w, "- можно конвертировать в байты.")
    except UnicodeEncodeError:
        print(w, "- НЕЛЬЗЯ конвертировать в байты.")


print('\nЗадание 4:')
words_4 = ['разработка', 'администрирование', 'protocol', 'standard']
tmp_bytes = []
tmp_strs = []

for w in words_4:
    tmp_bytes.append(w.encode())
print(', '.join([str({w: type(w)}) for w in tmp_bytes]))

for b in tmp_bytes:
    tmp_strs.append(b.decode())
print(', '.join([str({w: type(w)}) for w in tmp_strs]))


print('\nЗадание 5:')
import subprocess
import platform
windows = True if 'windows' in platform.platform().lower() else False
resources = ['yandex.ru', 'youtube.com']
for res in resources:
    subproc_ping = subprocess.Popen(['ping', res], stdout=subprocess.PIPE)
    for line in subproc_ping.stdout:
        if windows:
            print(line.decode('cp866'))
        else:
            print(line.decode('utf-8'))


print('\nЗадание 6:')
import sys
file = './lesson_1/test_file.txt'

try:
    import chardet
    with open(file, 'rb') as f:
        print(chardet.detect(f.read()))
except ImportError:
    print('Модуль charset не установлен!')

with open(file, 'r', encoding='utf-8') as f:
    print(f.read())
