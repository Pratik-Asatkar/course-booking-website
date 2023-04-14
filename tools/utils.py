import csv
from time import time
from datetime import datetime

def current_epoch():
    return int(time())


def current_time():
    return datetime.now().strftime("%d-%m-%Y %H:%M")


def save_response(data):
    filename = "response.csv"

    data_list = [data['name'], data['email'],data['dob'], data['address'], data['gender'], data['course1'], data['course2'], data['course3']]

    with open(filename, 'a', newline='\n') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(data_list)

