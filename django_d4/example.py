"""
Тестирование кода Flake8 и PyLint
Установка
pip install flake8
pip install pylint
Запуск
flake8 <filename>	pylint <filename>
В данном случае тестировали файл example.py
flake8 example.py	pylint example.py
--------------------------------
Этот файл в проекте не участвует
"""
import string;

shift = 3
choice = input("would you like to encode or decode?")
word = input("Please enter text")
letters = string.ascii_letters + string.punctuation + string.digits
encoded = ''
if choice == "encode":
    for letter in word:
        if letter == ' ':
            encoded = encoded + ' '
        else:
            x = letters.index(letter) + shift
            encoded = encoded + letters[x]
if choice == "decode":
    for letter in word:
        if letter == ' ':
            encoded = encoded + '  '
        else:
            x = letters.index(letter) - shift
            encoded = encoded + letters[x]
print(encoded)
