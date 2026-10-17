import random

letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers='0123456789'
symbols='!@#$%^&*'

password=''

for i in range(3):
    password+=random.choice(letters)
for i in range(3):
    password+=random.choice(numbers)
for i in range(2):
    password+=random.choice(symbols)

random.shuffle(list(password))
password=''.join(password)

print(f'Ваш пароль:{password}')
