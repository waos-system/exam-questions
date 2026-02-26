import json

# Test the correct mapping from options dict to choices array
file = 'data/lang/questions_sql_constraints.json'

with open(file, 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data.get('questions', [])

if questions:
    q = questions[0]
    print('Original question:')
    print(f"  options type: {type(q.get('options'))}")
    
    # Simulate the JavaScript mapping
    options_dict = q.get('options', {})
    choices_array = list(options_dict.values()) if isinstance(options_dict, dict) else []
    
    print(f'\nAfter mapping options dict to choices array:')
    print(f"  choices type: {type(choices_array)}")
    print(f"  choices is list: {isinstance(choices_array, list)}")
    print(f"  choices count: {len(choices_array)}")
    print(f"  choices sample: {choices_array[:2]}")
    
    # Verify all questions can be mapped properly
    valid_count = 0
    for q in questions:
        choices = list(q.get('options', {}).values()) if isinstance(q.get('options'), dict) else []
        if q.get('id') and q.get('question') and isinstance(choices, list) and len(choices) > 0:
            valid_count += 1
    
    print(f'\nAll questions valid after mapping: {valid_count}/{len(questions)}')
    print(f'✓ Mapping works correctly!' if valid_count == len(questions) else '✗ Some questions invalid')
