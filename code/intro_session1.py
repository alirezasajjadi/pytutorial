
# QUESTION_S1_1

def num_prime_counter(x):
    p = 2
    counter = []
    while x > 1:
        if x % p == 0:
            counter.append(p)
            x /= p
            # print('x= %d , p = %d' % (x, p))
        else:
            p += 1
            # print('p=',p)
    new_counter = []
    [new_counter.append(item) for item in counter if item not in new_counter]

    return len(new_counter)


li = []
for i in range(10):
    x = int(input())
    y = num_prime_counter(x)
    li.append((x, y))
max_fac = 0
num = []
for i in li:
    if i[1] >= max_fac:
        max_fac = i[1]
for i in li:
    if i[1] == max_fac:
        num.append(i[0])
print(max(num), max_fac)


""""""""""""

# QUESTION_S1_2


dic = {'Iran': {'wins': 0,
                'loses': 0,
                'draws': 0,
                'goal difference': 0,
                'points': 0
                },
       'Morocco': {'wins': 0,
                   'loses': 0,
                   'draws': 0,
                   'goal difference': 0,
                   'points': 0
                   },
       'Portugal': {'wins': 0,
                    'loses': 0,
                    'draws': 0,
                    'goal difference': 0,
                    'points': 0
                    },
       'Spain': {'wins': 0,
                 'loses': 0,
                 'draws': 0,
                 'goal difference': 0,
                 'points': 0
                 }
       }

for i in range(6):
    x, y = '', ''
    if i == 0:
        x = "Iran"
        y = "Spain"
    elif i == 1:
        x = "Iran"
        y = "Portugal"
    elif i == 2:
        x = "Iran"
        y = "Morocco"
    elif i == 3:
        x = "Spain"
        y = "Portugal"
    elif i == 4:
        x = "Spain"
        y = "Morocco"
    elif i == 5:
        x = "Portugal"
        y = "Morocco"

    result = str.split(input(), '-')
    if result[0] > result[1]:
        dic[x]['wins'] += 1
        dic[x]['goal difference'] += (int(result[0]) - int(result[1]))
        dic[x]['points'] += 3

        dic[y]['loses'] += 1
        dic[y]['goal difference'] += (int(result[1]) - int(result[0]))

    elif result[0] < result[1]:
        dic[y]['wins'] += 1
        dic[y]['goal difference'] += (int(result[1]) - int(result[0]))
        dic[y]['points'] += 3

        dic[x]['loses'] += 1
        dic[x]['goal difference'] += (int(result[0]) - int(result[1]))
    else:
        dic[x]['draws'] += 1
        dic[x]['goal difference'] += (int(result[0]) - int(result[1]))
        dic[x]['points'] += 1

        dic[y]['draws'] += 1
        dic[y]['goal difference'] += (int(result[1]) - int(result[0]))
        dic[y]['points'] += 1
dicti = dict(sorted(dic.items(), key=lambda item: (item[1]['points'], item[1]['wins']), reverse=True))

for item in dicti.keys():
    print(item + '  ', end='')
    j = 0
    for i in dicti.get(item).items():
        j += 1
        print(str(i[0]) + ':' + str(i[1]), end='')

        if j != 5:
            print(' , ', end='')
    print()


""""""""""""

# QUESTION_S1_3


number = int(input())
dic = {'Horror': 0,
       'Romance': 0,
       'Comedy': 0,
       'History': 0,
       'Adventure': 0,
       'Action': 0
       }
for i in range(number):
    input_args = str.split(input(), ' ')

    for ganr in input_args[1:]:
        dic[ganr] += 1
dic_sorted_keys = sorted(dic, key=lambda x: (-dic[x], x))
for key in dic_sorted_keys:
    print(f"{key} : {dic[key]}")


""""""""""""

# QUESTION_S1_5


import re

inp_str = str.split(input(), ' ')
found = False
for i in range(1, len(inp_str)):

    if bool(re.search('.\\.$', inp_str[i])) and i != len(inp_str) - 1:
        inp_str[i + 1] = re.sub('.', ' ', inp_str[i + 1])

    if bool(re.match('[A-Z]', inp_str[i][0])):
        found = True
        if bool(re.search('.\\.$|.,$', inp_str[i])):
            inp_str[i] = re.sub('\\.$|,$', '', inp_str[i])
        print(f"{i + 1}:{inp_str[i]}")

if not found:
    print('None')


""""""""""""

# QUESTION_S1_6


num = int(input())
dic = {}
for i in range(num):
    inp = str.split(input(), ' ')
    dic[inp[0]] = (inp[1], inp[2], inp[3])

inp_str = str.split(input(), ' ')
target = ''
for word in inp_str:
    key = [k for k, v in dic.items() if word in v]
    if len(key) != 0:
        target += "%s " % key[0]

    else:
        target += "%s " % word

print(target.strip())


""""""""""""

# QUESTION_S1_4

number = int(input())
arr = {'f': [], 'm': []}
for i in range(number):
    input_args = str.split(input(), '.')
    # if input_args[0] not in dic.keys():
    # arr.append((input_args[0], input_args[1], input_args[2]))
    arr[input_args[0]].append((input_args[1].lower().capitalize(), input_args[2]))

for k, v in arr.items():
    arr[k] = sorted(v, key=lambda x: x[0])

for k, v in arr.items():
    for i in range(len(v)):
        if k == 'f':
            print(f"f {v[i][0]} {v[i][1]}")
        elif k == 'm':
            print(f"m {v[i][0]} {v[i][1]}")

