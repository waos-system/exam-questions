import json

# Check the structure of problematic files
files = [
    'data/lang/questions_linux_firewall.json',
    'data/lang/questions_linux_network_dns.json'
]

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        questions = data.get('questions', [])
        print(f'\n{filepath}:')
        print(f'  Total questions: {len(questions)}')
        
        if questions:
            q = questions[0]
            print(f'  First question keys: {list(q.keys())}')
            
            # Check options
            options = q.get('options')
            print(f'  options type: {type(options).__name__}')
            print(f'  options value: {options}')
            
            # Check correct
            correct = q.get('correct')
            print(f'  correct type: {type(correct).__name__}')
            print(f'  correct value: {correct}')
    except Exception as e:
        print(f'{filepath}: ERROR - {str(e)[:80]}')
