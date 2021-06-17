import requests


def generate_animal_name(name):
    if not name :
        response = requests.get('https://random-word-form.herokuapp.com/random/adjective').json()
        adjective = response[0]

        response = requests.get('https://random-word-form.herokuapp.com/random/animal').json()
        animal = response[0]

        return f"{adjective} {animal}".title()

    return name
