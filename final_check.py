import json
import os

print('✅ JSON Validation Results:')
files = [
    'data/sc/questions_sc_governance.json', 
    'data/sc/questions_sc_technology.json', 
    'data/sc/questions_sc_incident.json', 
    'data/sc/questions_sc_assessment.json'
]

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
            count = len(data.get('questions', []))
            fname = f.split('/')[-1]
            print(f'  OK: {fname} - {count} questions')
    except Exception as e:
        print(f'  ERROR {f}: {str(e)}')

print('\ngenres.json SC section counts:')
with open('data/genres.json', 'r', encoding='utf-8') as file:
    genres = json.load(file)
    for exam in genres:
        if exam.get('id') == 'cert':
            for ex in exam.get('exams', []):
                if ex.get('id') == 'exam_sc':
                    for sec in ex.get('sections', []):
                        print(f'  {sec.get("id")}: {sec.get("count")} questions')
