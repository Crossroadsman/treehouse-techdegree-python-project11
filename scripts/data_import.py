import json
from os import environ
from os import path
import sys

import django


full_path = path.abspath(__file__)  # /MyUser/Repos/Project/scripts/this_file.py
scripts_dir = path.dirname(full_path)  # /MyUser/Repos/Project/scripts

PROJ_DIR = path.dirname(scripts_dir)  # /MyUser/Repos/Project 
DATA_PATH = path.join(PROJ_DIR, 'initial_data')
DATA_FILE = 'dog_details.json'


def load_data():
    filepath = path.join(DATA_PATH, DATA_FILE)
    
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

        serializer = DogSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

    print('load_data done.')


if __name__ == '__main__':
    sys.path.append(PROJ_DIR)
    environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    django.setup()

    # Assuming your serializer is named DogSerializer
    # has to be imported after django.setup()
    try:

        from pugorugh.serializers import DogSerializer
    except ImportError:
        raise ImportError('serializers.py must contain a properly '
            'implemented DogSerializer class for this import to work.')

    load_data()