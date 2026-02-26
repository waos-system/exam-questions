import json

# Debug the question structure
file = 'data/lang/questions_sql_constraints.json'

with open(file, 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data.get('questions', [])

if questions:
    q = questions[0]
    print('First question keys:', list(q.keys()))
    print('\nFirst question structure:')
    
    # Try to access options
    print(f"  'options' exists: {'options' in q}")
    print(f"  'options' type: {type(q.get('options'))}")
    
    if 'options' in q:
        options = q['options']
        print(f"  'options' value: {options}")
        print(f"  'options' is list: {isinstance(options, list)}")
        if isinstance(options, list):
            print(f"  'options' count: {len(options)}")
    
    # Test the mapping
    mapped_q = dict(q)
    mapped_q['choices'] = q.get('choices') or q.get('options')
    
    print('\nAfter mapping:')
    print(f"  'choices' exists: {'choices' in mapped_q}")
    print(f"  'choices' type: {type(mapped_q.get('choices'))}")
    print(f"  'choices' value: {mapped_q.get('choices')}")
    print(f"  'choices' is list: {isinstance(mapped_q.get('choices'), list)}")
