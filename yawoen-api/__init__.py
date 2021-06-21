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
        collection = db_name['companies']

        companies = []

        # Define the checker that returns 'None' if the zip code is not 6 digit
        # It was decided to use only numbers.
        match_zip = re.compile('^[0-9]{6}$').match

        for row in csv_reader:
            company_name = row[0].upper()
            zip_code = row[1]

            if not match_zip(zip_code):
                print(f"Error: the company {company_name} was not saved in the"
                      "data base because has an invalid zip code {zip_code}")
                continue

            dict_user = {'company_name': company_name,
                         'zip_code': zip_code}
            companies.append(dict_user)

        collection.insert_many(companies)


def integrate_website_data(fname='q2_clientData.csv'):
    '''Load website data from file and integrate it to DB.'''
    db_name = get_database()

    with open(fname, 'r') as read_obj:
        csv_reader = reader(read_obj)
        collection = db_name['companies']

        companies = []

        # Define the checker that returns 'None' if the zip code is not 6 digit
        # It was decided to use only numbers.
        match_zip = re.compile('^[0-9]{6}$').match

        for row in csv_reader:
            company_name = row[0].upper()
            zip_code = row[1]
            website = row[2].lower()

            # Fetch the company from db
            company = collection.find_one({'company_name': company_name})
            # If company does not exist skip this line of CSV file
            if company is None:
                continue

            # Check if 'zip_code' is 6 digit format.
            if not match_zip(zip_code):
                print(f"Error: the company {company_name} was not saved in the"
                      f" data base because has an invalid zip code {zip_code}")
                continue
            # Check if 'zip_code' is equal to the stored zip code
            if zip_code != company['zip_code']:
                print(f"Error: the website for company {company_name} was"
                      "not saved in the data base because the zip code "
                      f"'{zip_code}' from CSV file does not match with the "
                      "stored zip code.")
                continue

            collection.update_one({"_id": company['_id']},
                                  {"$set": {"website": website}})



