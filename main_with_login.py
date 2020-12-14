from getpass import getpass

import requests
from consumer.app import App

api_server = 'http://localhost:8000/api/v1'


def main(name: str):
    if name == '__main__':
        App(key=login()).run()


def login():
    username = input('Username: ')
    password = getpass('Password: ')

    response = requests.post(url=f'{api_server}/auth/login/', data={'username': username, 'password': password})
    if response.status_code != 200:
        print("Wrong credentials!")
        exit()
    else:
        json = response.json()
        return json['key']


main(__name__)
