
## Пример работы с классами

class multifilter:

    def judge_half(pos, neg):
        return pos >= neg
    # допускает элемент, если его допускает хотя бы половина фукнций (pos >= neg)

    def judge_any(pos, neg):
        return pos >= 1
        # допускает элемент, если его допускает хотя бы одна функция (pos >= 1)

    def judge_all(pos, neg):
        return neg == 0
        # допускает элемент, если его допускают все функции (neg == 0)

    def __init__(self, iterable, *funcs, judge=judge_any):
        self.iterable = iterable
        self.funcs = funcs
        self.judge = judge
        self.i = 0

    def __next__(self):
        while self.i < len(self.iterable):
            pos = neg = 0
            for f in self.funcs:
                if f(self.iterable[self.i]):
                    pos += 1
                else:
                    neg += 1
            self.i += 1
            if self.judge(pos, neg):
                return self.iterable[self.i - 1]
        raise StopIteration

    def __iter__(self):
        return self
        # возвращает итератор по результирующей последовательности


def mul2(x):
    return x % 2 == 0


def mul3(x):
    return x % 3 == 0


def mul5(x):
    return x % 5 == 0


a = [i for i in range(31)]
print(list(multifilter(a, mul2, mul3, mul5)))
print(list(multifilter(a, mul2, mul3, mul5, judge=multifilter.judge_half)))
print(list(multifilter(a, mul2, mul3, mul5, judge=multifilter.judge_all)))

## Пример работы со сторонними API

import requests
api_url = 'http://api.openweathermap.org/data/2.5/weather'
city = input('City?')

params = {'q': city,
          'appid': '7f86edf458f8a778a6abeef6812253e4',
          'units': 'metric',
          'lang': 'ru'
          }
res = requests.get(api_url, params=params)
data = res.json()
tempr = 'Current tempreture in {} is {}'
print(tempr.format(city, data['main']['temp']))

## Пример работы с JSON

import requests
import json

client_id = 'e2a8b2ec6005995cd30e'
client_secret = 'fe8528346a870195d68c4e1f16173d49'
r = requests.post('https://api.artsy.net/api/tokens/xapp_token',
                  data={
                      'client_id': client_id,
                      'client_secret': client_secret
                  })

j = json.loads(r.text)
token = j['token']
headers = {'X-Xapp-Token' : token}
with open("dataset_24476_4.txt", 'r') as inp, open("artists.txt", 'w') as wrt:
    for key in inp:
        r = requests.get('https://api.artsy.net/api/artists/{}'.format(key), headers=headers)
        j = json.loads(r.text)
        print(j['sortable_name'])
        wrt.write(j['sortable_name'], '\n')


## И пример реализации игры Быки и коровы

from my_study_programs.Game.mastermind_engine import number, output_num, check_num
number()
n = 0
while True:
    inp_num = str(input('Введите 4 значное число '))
    if len(inp_num) == 4:
        results = check_num(input_number=inp_num)
        n += 1
        if results['bulls'] == 4:
            print('Вы выйграли! ', end='')
            print('Количество ходов:', n)
            print('Ещё партейку?')
            break
    else:
        print('Вы ввели число меньшей или большей длинны, введите число из 4 знаков.')

## файл mastermind_engine из которого беру "движок" игры

output_number = []


def number():
    global output_number
    output_number = [random.randint(1, 9)]
    while len(output_number) < 4:
        output_number.append(random.randint(0, 9))
        output_number_1 = set(output_number)
        output_number = list(output_number_1)
        if output_number[0] == 0:
            output_number[0] = random.randint(1, 9)
            output_number_1 = set(output_number)
            output_number = list(output_number_1)
    return output_number


def output_num():
    print(''.join(map(str, output_number)))


def check_num(input_number):
    results = {'bulls': 0, 'cows': 0}
    string_of_numbers = ''.join(map(str, output_number))
    for i in range(0, len(input_number)):
        position = string_of_numbers.find(input_number[i])
        if position == -1:
            continue
        if position == i:
            results['bulls'] += 1
        if position != i and position != -1:
            results['cows'] += 1
    print('> быки - ', results['bulls'], '> коровы - ', results['cows'])
    return results
