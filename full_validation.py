import json
import os

print('=== Complete System Validation ===\n')

# 1. genres.json validation
print('1. Genres.json structure:')
try:
    with open('data/genres.json', 'r', encoding='utf-8') as f:
        genres = json.load(f)
    print('   ✓ JSON syntax OK')
    
    total_exams = 0
    total_sections = 0
    
    for subject in genres['subjects']:
        for exam in subject.get('exams', []):
            total_exams += 1
            for section in exam.get('sections', []):
                total_sections += 1
    
    print(f'   ✓ Total exams: {total_exams}')
    print(f'   ✓ Total sections: {total_sections}')
except Exception as e:
    print(f'   ✗ ERROR: {str(e)[:80]}')

# 2. Question files validation
print('\n2. Question files count verification:')

mismatches = []
file_errors = []

for subject in genres['subjects']:
    for exam in subject.get('exams', []):
        for section in exam.get('sections', []):
            file = section.get('file')
            expected_count = section.get('count')
            
            if not file or not expected_count:
                continue
            
            if os.path.exists(file):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        actual_count = len(data.get('questions', []))
                        
                    if actual_count != expected_count:
                        mismatches.append({
                            'section': section.get('id'),
                            'expected': expected_count,
                            'actual': actual_count
                        })
                except Exception as e:
                    file_errors.append({'file': file, 'error': str(e)[:50]})
            else:
                file_errors.append({'file': file, 'error': 'File not found'})

if not mismatches:
    print('   ✓ All section counts match file contents')
else:
    print(f'   ✗ Found {len(mismatches)} mismatches:')
    for item in mismatches[:5]:  # Show first 5
        print(f'     - {item["section"]}: expected {item["expected"]}, got {item["actual"]}')

if not file_errors:
    print('   ✓ All files exist and are valid JSON')
else:
    print(f'   ✗ Found {len(file_errors)} file errors:')
    for item in file_errors[:3]:  # Show first 3
        print(f'     - {item["file"]}: {item["error"]}')

# 3. SQL files validation
print('\n3. SQL question files:')
sql_files = ['data/lang/questions_sql_select.json', 'data/lang/questions_sql_functions.json',
             'data/lang/questions_sql_group.json', 'data/lang/questions_sql_join.json',
             'data/lang/questions_sql_subquery.json', 'data/lang/questions_sql_dml_ddl.json',
             'data/lang/questions_sql_constraints.json', 'data/lang/questions_sql_window_functions.json',
             'data/lang/questions_sql_advanced.json']

sql_ok = 0
for f in sql_files:
    if os.path.exists(f):
        try:
            with open(f, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if 'questions' in data:
                    sql_ok += 1
        except:
            pass

print(f'   ✓ Valid SQL files: {sql_ok}/{len(sql_files)}')

# 4. Linux files validation
print('\n4. Linux question files:')
linux_files = ['data/lang/questions_linux_commands.json', 'data/lang/questions_linux_filesystem.json',
               'data/lang/questions_linux_process.json', 'data/lang/questions_linux_network.json',
               'data/lang/questions_linux_packages.json', 'data/lang/questions_linux_users_groups.json',
               'data/lang/questions_linux_boot_kernel.json', 'data/lang/questions_linux_firewall.json',
               'data/lang/questions_linux_network_dns.json', 'data/lang/questions_linux_storage.json',
               'data/lang/questions_linux_sysadmin.json']

linux_ok = 0
for f in linux_files:
    if os.path.exists(f):
        try:
            with open(f, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if 'questions' in data:
                    linux_ok += 1
        except:
            pass

print(f'   ✓ Valid Linux files: {linux_ok}/{len(linux_files)}')

print('\n=== Summary ===')
if not mismatches and not file_errors and sql_ok == len(sql_files) and linux_ok == len(linux_files):
    print('✅ All systems operational!')
else:
    print('⚠️ Issues detected - see above for details')
