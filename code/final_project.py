import time
from random import randint

import mysql.connector
from bs4 import BeautifulSoup
import requests
import re
import struct
from sklearn import tree
from sklearn.preprocessing import LabelEncoder

persian_to_english = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
zone_label_encoder = LabelEncoder()


# Generate different IP addresses to simulate different users
def random_ip_generator():
    return "{}.{}.{}.{}".format(randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255))


def find_href(item):
    pattern = r'href=\"/v/[\u0600-\u06FF-?_?\d?/\w+]+'
    href = re.findall(pattern, str(item))
    href = re.sub(r'href=\"', '', href[0])
    return href


def find_zone(cursor, id_attr, soap):
    zone_button = soap.find_all('button', attrs={'class': 'kt-chip kt-chip--has-action kt-wrapper-row__child'})
    print('zone button:', zone_button)
    if len(zone_button) > 1:
        zone = re.sub(r'.*\u062F\u0631', '', zone_button[1].text)
        print('z', zone)

        pattern = r"\((.*?)\)"
        match = re.search(pattern, zone)
        print('m', match)

        if match:
            match = re.sub(r'\(', '', match.group(1))
            match = re.sub(r'\)', '', match)
            print('m1', match)

            zone1 = match
            print('zone1', zone1)

            query = "INSERT INTO estate(id, zone) VALUES (%s, %s)"
            cursor.execute(query, (id_attr, zone1.strip()))
        else:
            query = "INSERT INTO estate(id, zone) VALUES (%s, %s)"
            cursor.execute(query, (id_attr, zone.strip()))


def find_meterage_year_rooms(cursor, id_attr, soap):
    row_values = soap.find_all('span', attrs={'class': 'kt-group-row-item__value'}, limit=3)
    for value in row_values:
        if re.match(r'^[\u06F0-\u06F9]{2,3}$', value.text) is not None:
            query = "UPDATE estate SET meterage = %s WHERE id = %s"
            meter = int(value.text.translate(persian_to_english))
            cursor.execute(query, (meter, id_attr))

        elif re.match(r'^[\u06F0-\u06F9]{4}$', value.text) is not None:
            query = "UPDATE estate SET year = %s WHERE id = %s"
            year = int(value.text.translate(persian_to_english))
            cursor.execute(query, (year, id_attr))

        elif re.match(r'^[\u06F0-\u06F9]$', value.text) is not None:
            query = "UPDATE estate SET number_room = %s WHERE id = %s"
            numer_room = int(value.text.translate(persian_to_english))
            cursor.execute(query, (numer_room, id_attr))


def find_prices(cursor, id_attr, soap):
    prices = soap.find_all('p', attrs={'class': 'kt-unexpandable-row__value'}, limit=2)

    for price in prices:
        price = re.sub(r'\u066C', '', price.text)
        price = re.sub(r'\u062A\u0648\u0645\u0627\u0646', '', price)
        price = price.strip()

        if re.match(r'^[\u06F0-\u06F9]{4,8}$', price) is not None:
            query = "UPDATE estate SET price_per_meter = %s WHERE id = %s"
            price_per_meter = int(price.translate(persian_to_english))
            cursor.execute(query, (price_per_meter, id_attr))
        elif re.match(r'^[\u06F0-\u06F9]{9,}$', price) is not None:
            query = "UPDATE estate SET total_price = %s WHERE id = %s"
            total_price = int(price.translate(persian_to_english))
            cursor.execute(query, (total_price, id_attr))


def find_elevator_park_warehouse(cursor, id_attr, soap):
    epw = soap.find_all('span', attrs={'class': 'kt-group-row-item__value kt-body kt-body--stable'}, limit=3)
    # epw[0]: elevator_status
    # epw[1]: parking slot status
    # epw[1]: ware house status
    print(epw)
    # pattern = ندارد
    pattern = r'\u0646\u062f\u0627\u0631\u062f'

    # has no elevator
    if re.search(pattern, epw[0].text):
        binary_value = struct.pack('b', 0)
        query = "UPDATE estate SET elevator = %s WHERE id = %s"
    # has elevator
    else:
        binary_value = struct.pack('b', 1)
        query = "UPDATE estate SET elevator = %s WHERE id = %s"
    cursor.execute(query, (binary_value, id_attr))

    # has no parking
    if re.search(pattern, epw[1].text):
        binary_value = struct.pack('b', 0)
        query = "UPDATE estate SET parking_space = %s WHERE id = %s"
    # has parking
    else:
        binary_value = struct.pack('b', 1)
        query = "UPDATE estate SET parking_space = %s WHERE id = %s"
    cursor.execute(query, (binary_value, id_attr))

    # has no warehouse
    if re.search(pattern, epw[2].text):
        binary_value = struct.pack('b', 0)
        query = "UPDATE estate SET warehouse = %s WHERE id = %s"
    # has warehouse
    else:
        binary_value = struct.pack('b', 1)
        query = "UPDATE estate SET warehouse = %s WHERE id = %s"
    cursor.execute(query, (binary_value, id_attr))


def delete_null_records(cursor):
    query = "DELETE FROM estate " \
            "WHERE zone IS NULL OR meterage IS NULL OR year IS NULL OR number_room IS NULL OR " \
            "total_price IS NULL OR price_per_meter IS NULL OR elevator IS NULL OR parking_space IS NULL OR " \
            "warehouse IS NULL"
    cursor.execute(query)


def create_table(cnx, cursor):
    query = "CREATE TABLE estate (id INT, zone VARCHAR(100), meterage INT, year INT, " \
            "number_room INT, total_price BIGINT, price_per_meter INT," \
            "elevator BIT(1), parking_space BIT(1), warehouse BIT(1))"
    query = "ALTER TABLE estate ADD PRIMARY KEY (id)"
    cursor.execute(query)
    cnx.commit()


def scrapping_and_push_database(cnx, cursor):
    id_attr = 1

    for page_number in range(1, 84):
        ip = random_ip_generator()
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/113.0.0.0 Safari/537.36',
                  'X-Forwarded-For': ip
                  }
        url = f"https://divar.ir/s/mashhad/buy-apartment?page={page_number}"
        request = requests.get(url, headers=header)
        soap = BeautifulSoup(request.text, 'html.parser')

        # find all residential item in one page <div></div>
        items_div = soap.find_all('div', attrs={'class': 'post-card-item-af972 kt-col-6-bee95 kt-col-xxl-4-e9d46'})

        # in this list of items, find href of each item. and send get request to that link
        for item in items_div:
            href = find_href(item)

            # send get request to that href link
            time.sleep(0.2)

            ip = random_ip_generator()
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/113.0.0.0 Safari/537.36',
                      'X-Forwarded-For': ip
                      }
            url_1 = f"https://divar.ir{href}"
            request_residential = requests.get(url_1, headers=header)
            soap_inner = BeautifulSoup(request_residential.text, 'html.parser')

            print("url = ", url_1)

            try:
                # FIND ZONE
                find_zone(cursor, id_attr, soap_inner)
                cnx.commit()

                # FIND METERAGE
                find_meterage_year_rooms(cursor, id_attr, soap_inner)
                cnx.commit()

                # FIND PRICE
                find_prices(cursor, id_attr, soap_inner)
                cnx.commit()

                # FIND ELEVATOR PARKING WARE_HOUSE
                find_elevator_park_warehouse(cursor, id_attr, soap_inner)
                cnx.commit()
                id_attr += 1
            except Exception:
                pass

    # delete records which has null column
    delete_null_records(cursor)
    cnx.commit()


def main_function():
    cnx = mysql.connector.connect(user='', password='', host='localhost', database='')
    cursor = cnx.cursor()

    # create_table(cnx,cursor)
    # scrapping_and_push_database(cnx, cursor)

    query = "SELECT zone, meterage, year, number_room, elevator, parking_space, " \
            "warehouse, total_price FROM estate"
    cursor.execute(query)
    records = cursor.fetchall()

    x = []
    y = []

    zone_label_encoder.fit([record[0] for record in records])  # Fit the LabelEncoder with the 'zone' values

    for record in records:
        # row = [float(val) if isinstance(val, str) and val.replace('.', '').isdigit() else val for val in record[1:7]]
        row = [val for val in record[1:7]]
        encoded_zone = zone_label_encoder.transform([record[0]])[0]
        row.insert(0, encoded_zone)

        x.append(row)
        y.append(record[7])

    cnx.close()

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x, y)

    new_data = [['بلوار سجاد', '90', '1400', '2', '1', '1', '1']]
    encoded_zone = zone_label_encoder.transform([new_data[0][0]])[0]
    new_data[0][0] = encoded_zone
    print(new_data)

    answer = clf.predict(new_data)

    print(answer)


if __name__ == '__main__':
    main_function()
