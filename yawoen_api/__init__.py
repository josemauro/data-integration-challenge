"""Module to provide the data integration API Yawoen."""
import os
import random
import re
from csv import reader

from flask import Flask
from pymongo import MongoClient


def create_app(test_config=None):
    """Create and configure the app."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Endpoint to load csv data
    @app.route('/csvdata')
    def api_load_csv():
        file_path = 'yawoen_api/q1_catalog.csv'
        response = _load_csv(file_path)
        return response

    # Endpoint to load website data
    @app.route('/websitetedata')
    def api_load_website_data():
        file_path = 'yawoen_api/q2_clientData.csv'
        response = _load_website_data(file_path)
        return response

    return app


def get_database():
    '''Get MongoDB client.'''
    client = MongoClient('localhost', 27017)

    return client['yawoen-data']


def _load_csv(file_path):
    '''Load data from CSV file.'''
    if not os.path.exists(file_path):
        return (f"Error loading data from file '{file_path}'.\n"
                "The file does not exist!")

    db_name = get_database()

    with open(file_path, 'r') as read_obj:
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

        return 'Data loaded from CSV file.'


def _load_website_data(file_path):
    '''Load website data from file and integrate it to DB.'''
    if not os.path.exists(file_path):
        return (f"Error loading the website data from file '{file_path}'.\n"
                "The file does not exist!")

    db_name = get_database()

    with open(file_path, 'r') as read_obj:
        csv_reader = reader(read_obj)
        collection = db_name['companies']

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

        return "Website data loaded!"
