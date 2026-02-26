import json

# Test the corrected mapping
file = 'data/lang/questions_sql_constraints.json'

with open(file, 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data.get('questions', [])

# Simulate the correct mapping
answers = ['A', 'B', 'C', 'D', 'E', 'F']

mapped_questions = []
for q in questions:
    options_dict = q.get('options', {})
    choices = list(options_dict.values()) if isinstance(options_dict, dict) else []
    
    # Convert correct (string) to answer (int index)
    answer_idx = 0
    if q.get('correct') and isinstance(q['correct'], str):
        answer_idx = answers.index(q['correct'].upper()) if q['correct'].upper() in answers else 0
    
    mapped_q = dict(q)
    mapped_q['choices'] = choices
    mapped_q['answer'] = answer_idx
    mapped_questions.append(mapped_q)

# Verify mapping
print(f'File: {file}')
print(f'Total questions: {len(mapped_questions)}')

valid_count = 0
for i in range(min(5, len(mapped_questions))):
    m = mapped_questions[i]
    is_valid = all([
        m.get('id'),
        m.get('question'),
        isinstance(m.get('choices'), list) and len(m['choices']) > 0,
        isinstance(m.get('answer'), int) and 0 <= m['answer'] < len(m['choices']),
        m.get('explanation')
    ])
    
    print(f"Q{i+1}: id={m.get('id')}, choices≠count={len(m.get('choices', []))}, answer={m.get('answer')}, valid={is_valid}")
    if is_valid:
        valid_count += 1

print(f'\nFirst 5 questions: {valid_count}/5 valid')

# Check all
all_valid = 0
for m in mapped_questions:
    is_valid = all([
        m.get('id'),
        m.get('question'),
        isinstance(m.get('choices'), list) and len(m['choices']) > 0,
        isinstance(m.get('answer'), int) and 0 <= m['answer'] < len(m['choices']),
        m.get('explanation')
    ])
    if is_valid:
        all_valid += 1

print(f'All questions: {all_valid}/{len(mapped_questions)} valid')
