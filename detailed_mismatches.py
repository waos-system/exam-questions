import json
import os

print('=== Count Mismatches Detailed ===\n')

with open('data/genres.json', 'r', encoding='utf-8') as f:
    genres = json.load(f)

mismatches = []

for subject in genres['subjects']:
    for exam in subject.get('exams', []):
        for section in exam.get('sections', []):
            file = section.get('file')
            expected_count = section.get('count')
            section_id = section.get('id')
            
            if not file or not expected_count:
                continue
            
            if os.path.exists(file):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        actual_count = len(data.get('questions', []))
                        
                    if actual_count != expected_count:
                        mismatches.append({
                            'id': section_id,
                            'name': section.get('name'),
                            'expected': expected_count,
                            'actual': actual_count,
                            'file': file
                        })
                except Exception as e:
                    pass

# Group by difference
sql_linux_issues = [m for m in mismatches if 'sql_' in m['id'] or 'linux_' in m['id']]
other_issues = [m for m in mismatches if 'sql_' not in m['id'] and 'linux_' not in m['id']]

print(f'SQL & Linux Issues ({len(sql_linux_issues)}):')
for item in sql_linux_issues:
    print(f'  {item["id"]}: {item["expected"]} expected, {item["actual"]} actual')

print(f'\nOther Issues ({len(other_issues)}):')
for item in other_issues[:10]:  # Show first 10
    print(f'  {item["id"]}: {item["expected"]} expected, {item["actual"]} actual')

if len(other_issues) > 10:
    print(f'  ... and {len(other_issues) - 10} more')

print(f'\nTotal: {len(mismatches)} mismatches')
print(f'SQL/Linux OK: {len(sql_linux_issues) == 0}')
