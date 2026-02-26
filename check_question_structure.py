import json

# Check the structure of one question from each problematic section
files_to_check = [
    'data/lang/questions_sql_constraints.json',
    'data/lang/questions_sql_window_functions.json',
    'data/lang/questions_sql_advanced.json',
    'data/lang/questions_linux_commands.json',
]

for filepath in files_to_check:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        questions = data.get('questions', [])
        print(f'\n{filepath}:')
        print(f'  Total questions: {len(questions)}')
        
        if questions:
            q = questions[0]
            print(f'  First question keys: {list(q.keys())}')
            print(f'  Has "choices"? {"choices" in q}')
            if 'choices' in q:
                print(f'  Number of choices: {len(q["choices"])}')
            
            # Check a few more
            for i in range(min(3, len(questions))):
                q = questions[i]
                has_choices = 'choices' in q
                has_question = 'question' in q
                has_id = 'id' in q
                print(f'    Q{i}: id={has_id}, question={has_question}, choices={has_choices}')
    except Exception as e:
        print(f'{filepath}: ERROR - {str(e)[:80]}')
