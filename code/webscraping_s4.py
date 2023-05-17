# QUESTION_S4_1

import re

input_email = input()

string_p = re.compile('[a-zA-Z]+')
expression_p = re.compile("[a-zA-Z]+|\\w+[a-zA-Z]+|[a-zA-Z]+\\w+")
tailing = input_email.split('@')

while (input_email.find('@') == -1 or input_email.split('@')[1].find('.') == -1 or
       input_email.count("@") > 1 or (input_email.find('@') > input_email.rfind('.')) or
       expression_p.match(tailing[0]) is None or string_p.match(tailing[1].split('.')[0]) is None
       or string_p.match(tailing[1].split('.')[1]) is None):
    print('WRONG')
    exit()

print('OK')

""""""""""""

# QUESTION_S4_2

from bs4 import BeautifulSoup
import requests
import re

req = requests.get('https://divar.ir/s/mashhad/jobs')

soup = BeautifulSoup(req.text, 'html.parser')

div = soup.find_all('div', attrs={'class': 'kt-post-card__description'})

for item in div:
    if re.search("توافقی", item.text) is not None:
        parent_header = item.parent()[0]
        print(parent_header.text)

""""""""""""

# SESSION4_Project

import re

from bs4 import BeautifulSoup
import requests
import mysql.connector

cnx = mysql.connector.connect(user='', password='', host='localhost', database='')
cursor = cnx.cursor()
# query = "CREATE TABLE carsinfo (name VARCHAR(100), price INT, operation INT)"
# cursor.execute(query)
# cnx.commit()

brand, car_name = input().split(' ')
req = requests.get(f'https://www.truecar.com/used-cars-for-sale/listings/{brand}/{car_name}/')

soap = BeautifulSoup(req.text, 'html.parser')

cars_price = soap.find_all('div', attrs={'data-test': 'vehicleCardPricingBlockPrice'})
cars_operation = soap.find_all('div', attrs={'data-test': 'vehicleMileage'})

for i in range(0, 20):
    price = cars_price[i].text
    price = re.sub(r',', '', price)
    price = re.sub(r'\$', '', price)

    operation = cars_operation[i].text
    operation = re.sub(r',', '', operation)
    operation = re.sub(r' miles', '', operation)

    car_data = (f"{brand} {car_name}", int(price), int(operation))
    insert_cmd = "INSERT INTO carsinfo(name, price, operation) VALUES (%s, %s, %s)"
    cursor.execute(insert_cmd, car_data)
    # query = "SELECT * FROM carsinfo"
    # cursor.execute(query)
    # print(cursor.fetchall())
    cnx.commit()

cnx.close()
