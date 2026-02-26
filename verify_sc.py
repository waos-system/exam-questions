import json
import os

files = [
    'data/sc/questions_sc_governance.json',
    'data/sc/questions_sc_technology.json',
    'data/sc/questions_sc_incident.json',
    'data/sc/questions_sc_assessment.json'
]

for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
            count = len(data.get('questions', []))
            print(f'{f.split("/")[-1]}: {count} questions')
    else:
        print(f'{f}: FILE NOT FOUND')
