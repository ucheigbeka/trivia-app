# Trivia App

Trivia App is a web application for uploading and answering trivia questions. These questions span across a range of categories:
- Science
- Art
- Geography
- History
- Entertainment
- Sports

![Screenshot](screenshot.png)

All backend code follows [PEP8 style guidelines](https://peps.python.org/pep-0008/).

## Getting Started
The project is divided into two sections; a frontend and backend

### Frontend

The frontend is a React app that interacts with the backend.
[Nodejs](https://nodejs.org/en/download/) is required for building and running the frontend.

Run `npm -v` to ensure that node is properly installed and working.

To run the frontend, navigate to root directory (`./frontend`) and execute the following commands.

```bash
npm install
```

```bash
npm start
```

This should start a server on [http://localhost:3000](http://localhost:3000).

### Backend

The backend is a REST api built with the python Flask framework. Complete description of the api can be found in the [API documentation](./backend/README.md).

#### Dependencies
- Python >= 3.10
- PostgreSQL >= 11.3

### Instructions
- Create a new postgresql user `postgres`
- Create the db and test dbs
```bash
createdb -U postgres trivia
createdb -U postgres trivia_test
```
- Load `./backend/trivia.psql` into the `trivia` db
```bash
psql -U postgres trivia < ./backend/trivia.psql
```
- Navigate into the `./backend` directory and create a new python virtual environment
```bash
cd ./backend
python -m venv ./venv
```
- Start the virtual environment
```bash
source ./venv/Script/activate
```
- Install all the dependencies with `pip`
```bash
pip install -r requirements.txt
```
- Create a `.env` file with all your database configurations
```dotenv
PASSWORD=*****
DATABASE_PATH=postgresql://postgres:${PASSWORD}@localhost:5432/trivia
TEST_DATABASE_PATH=postgresql://postgres:${PASSWORD}@localhost:5432/trivia_test
```
- Configure your environment
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
```
- Run the all the tests to make sure everything is okay
```bash
python -m unittest test_flaskr.py
```
- Start your flask server
```bash
flask run
```
The server should on the default domain [http://localhost:5000](http://localhost:5000).

## Authors

The Udacity team and yours truly