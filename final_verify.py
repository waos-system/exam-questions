import json

print('Final verification:')
try:
    with open('data/genres.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print('OK: genres.json - valid JSON')
except Exception as e:
    print(f'ERROR: genres.json - {str(e)[:100]}')

# Spot check a few files
test_files = [
    'data/lang/questions_sql_select.json',
    'data/lang/questions_sql_window_functions.json',
    'data/lang/questions_linux_users_groups.json',
]

for f in test_files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            json.load(file)
        name = f.split('/')[-1]
        print(f'OK: {name}')
    except Exception as e:
        print(f'ERROR: {f}')
