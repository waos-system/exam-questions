import json

# Check the correct field type
file = 'data/lang/questions_sql_constraints.json'

with open(file, 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data.get('questions', [])

if questions:
    for i in range(min(5, len(questions))):
        q = questions[i]
        correct_val = q.get('correct')
        print(f'Q{i+1}: correct type={type(correct_val).__name__}, value={repr(correct_val)}, isinstance(int)={isinstance(correct_val, int)}')
