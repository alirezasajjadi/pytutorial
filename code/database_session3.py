# QUESTION_S3_1

import mysql.connector

cnx = mysql.connector.connect(user='', password='', host='localhost', database='')
cursor = cnx.cursor()
# table_dsc = "CREATE TABLE test (Name varchar(15), Weight int, Height int)"
# table_dsc = "INSERT INTO test VALUES (\'Ahmad\', 60, 175)"
query = 'SELECT * FROM test ORDER BY height DESC, weight'
cursor.execute(query)

for (name, weight, height) in cursor:
    print(name, height, weight)
# query = "SELECT Name, Weight, Height FROM "

cnx.close()

""""""""""""

# QUESTION_S3_2

import mysql.connector
import re

cnx = mysql.connector.connect(user='', password='', host='localhost', database='')
cursor = cnx.cursor()

# table_dsc = "CREATE TABLE test2 (username VARCHAR(255), password VARCHAR(255))"

username = input('please enter your username: ')

string_p = re.compile('[a-zA-Z]+')
expression_p = re.compile("[a-zA-Z]+|\\w+[a-zA-Z]+|[a-zA-Z]+\\w+")
tailing = username.split('@')

while (username.find('@') == -1 or username.split('@')[1].find('.') == -1 or
       username.count("@") > 1 or (username.find('@') > username.rfind('.')) or
       expression_p.match(tailing[0]) is None or string_p.match(tailing[1].split('.')[0]) is None
       or string_p.match(tailing[1].split('.')[1]) is None):
    print("Email format should be like this: expression@string.string")
    username = input('please enter your username: ')
    tailing = username.split('@')


password = input('please enter your password: ')

p = re.compile('\\d+[a-zA-Z]+\\d*[a-zA-Z]*|\\d*[a-zA-Z]*\\d+[a-zA-Z]+')

while p.match(password) is None:
    print('week password. Your password should contain at least one number and string.')
    password = input('please enter your password: ')

email_data = (username, password)

table_insertion = "INSERT INTO test2 VALUES (%s, %s)"
cursor.execute(table_insertion, email_data)
cnx.commit()

cursor.close()
cnx.close()
