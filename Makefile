#Challenge Makefile
deps: 
	python3.9 -m pip install -r requirements.txt 

setup:
	export FLASK_ENV=development
	export FLASK_APP=yawoen_api

start:
#TODO: commands necessary to start the API
	flask run

check:
#TODO: include command to test the code and show the results

test:
	python3.9 -m unittest tests/test_yawoen_api.py

lint:
	yala yawoen_api/__init__.py tests/test_yawoen_api.py	

