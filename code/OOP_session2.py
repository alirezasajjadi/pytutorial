
# QUESTION_S2_1

class Sclass:
    def __init__(self, student_number: int, students_age: list, students_height: list, students_weight: list):
        self.student_number = student_number
        self.students_height = students_height
        self.students_weight = students_weight
        self.students_age = students_age

    def avg_height(self):
        sum_height = 0
        for height in self.students_height:
            sum_height += height
        return sum_height / self.student_number

    def avg_weight(self):
        sum_weight = 0
        for weight in self.students_weight:
            sum_weight += weight
        return sum_weight / self.student_number

    def avg_age(self):
        sum_age = 0
        for age in self.students_age:
            sum_age += age
        return sum_age / self.student_number


def create_class(stu_num):
    age = list(map(int, input().split()))
    hei = list(map(int, input().split()))
    wei = list(map(int, input().split()))

    return Sclass(stu_num, age, hei, wei)


stu_num_A = int(input())
classA = create_class(stu_num_A)
stu_num_B = int(input())
classB = create_class(stu_num_B)

print(classA.avg_age())
print(classA.avg_height())
print(classA.avg_weight())

print(classB.avg_age())
print(classB.avg_height())
print(classB.avg_weight())

if classA.avg_height() > classB.avg_height():
    print('A')
elif classA.avg_height() < classB.avg_height():
    print('B')
else:
    print('Same')


""""""""""""

# QUESTION_S2_1

import datetime as dt
import math

byear, bmonth, bday = map(int, input().split('/'))

try:
    my_date = dt.date(byear, bmonth, bday)
except ValueError:
    print('WRONG')
    exit()

today = dt.date.today()

delta_time = today - my_date
print(math.floor(delta_time.days / 365.25))


""""""""""""

# SESSION2_project
import random

class Human:
    def __init__(self):
        self.__name = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name


class Player(Human):
    def __init__(self):
        super().__init__()
        self.__team_name = None

    @property
    def team_name(self):
        return self.__team_name

    @team_name.setter
    def team_name(self, team):
        self.__team_name = team


player_list = []
for i in range(22):
    player_list.append(Player())

player_list[0].name = 'حسین'
player_list[1].name = 'مازیار'
player_list[2].name = 'اکبر'
player_list[3].name = 'نیما'
player_list[4].name = 'مهدی'
player_list[5].name = 'فرهاد'
player_list[6].name = 'محمد'
player_list[7].name = 'خشایار'
player_list[8].name = 'میلاد'
player_list[9].name = 'مصطفی'
player_list[10].name = 'امین'
player_list[11].name = 'سعید'
player_list[12].name = 'پویا'
player_list[13].name = 'پوریا'
player_list[14].name = 'رضا'
player_list[15].name = 'علی'
player_list[16].name = 'بهزاد'
player_list[17].name = 'سهیل'
player_list[18].name = 'بهروز'
player_list[19].name = 'شهروز'
player_list[20].name = 'سامان'
player_list[21].name = 'محسن'

team_A = random.sample(player_list, k=11)

for p in team_A:
    p.team_name = 'A'

team_b = []
for p in player_list:
    if p not in team_A:
        team_b.append(p)

for p in team_b:
    p.team_name = 'B'

for p in player_list:
    print(f"player name is {p.name} and played for team {p.team_name}")