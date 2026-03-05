import json

with open('data/au/questions_au_planning.json', encoding='utf-8') as f:
    data = json.load(f)

for q in data['questions'][:10]:
    print(q['id'], [len(c) for c in q['choices']], 'correct', q['answer'])
