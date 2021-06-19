import random
import re
from csv import reader
from pymongo import MongoClient


def get_database():
    '''Get MongoDB client.'''
    client = MongoClient('localhost', 27017)

    return client['yawoend-data']


def load_csv(fname='q1_catalog.csv'):
    '''Load data from CSV file.'''
    db_name = get_database()

    with open(fname, 'r') as read_obj:
        csv_reader = reader(read_obj)
        collection_company = db_name['companies']

        companies = []

        # Define the checker that returns 'None' if the zip code is not 6 digit
        # It was decided to use only numbers.
        match_zip = re.compile('^[0-9]{6}$').match

        for row in csv_reader:
            company_id = random.randint(0, 100)
            company_name = row[0].upper()
            zip_code = row[1]

            if not match_zip(zip_code):
                print(f"Error: the company {company_name} was not saved in the"
                       "data base because has an invalid zip code {zip_code}")
                continue

            dict_user = {'id': company_id,
                         'company_name': company_name,
                         'zip_code': zip_code}
            companies.append(dict_user)

        collection_company.insert_many(companies)
