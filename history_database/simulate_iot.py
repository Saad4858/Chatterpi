import csv
import time

def print_csv_data(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
            time.sleep(5)

def add_csv_data(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
            time.sleep(5)

print_csv_data('dummy_data/crop_recommendation.csv')