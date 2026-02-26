import json
import os

print('=== Checking specific sections that have errors ===\n')

with open('data/genres.json', 'r', encoding='utf-8') as f:
    genres = json.load(f)

# Check SQL sections
sql_sections_to_check = ['sql_constraints', 'sql_window_functions', 'sql_advanced']
linux_sections_to_check = ['linux_commands', 'linux_filesystem', 'linux_process', 'linux_network', 
                           'linux_packages', 'linux_users_groups', 'linux_boot_kernel', 'linux_firewall',
                           'linux_network_dns', 'linux_storage', 'linux_sysadmin']

print('SQL Sections:')
for subject in genres['subjects']:
    for exam in subject.get('exams', []):
        if exam.get('id') == 'lang_sql':
            for section in exam.get('sections', []):
                sec_id = section.get('id')
                if sec_id in sql_sections_to_check:
                    file_path = section.get('file')
                    count = section.get('count')
                    
                    file_exists = os.path.exists(file_path)
                    
                    # Check file validity
                    valid_json = False
                    actual_count = 0
                    if file_exists:
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                actual_count = len(data.get('questions', []))
                                valid_json = True
                        except Exception as e:
                            print(f'  ERROR reading {file_path}: {str(e)[:60]}')
                    
                    status = '✓' if (file_exists and valid_json) else '✗'
                    print(f'  {status} {sec_id}: count={count}, file_exists={file_exists}, actual_count={actual_count}')

print('\nLinux Sections:')
for subject in genres['subjects']:
    for exam in subject.get('exams', []):
        if exam.get('id') == 'lang_linux':
            for section in exam.get('sections', []):
                sec_id = section.get('id')
                if sec_id in linux_sections_to_check:
                    file_path = section.get('file')
                    count = section.get('count')
                    
                    file_exists = os.path.exists(file_path)
                    
                    # Check file validity
                    valid_json = False
                    actual_count = 0
                    if file_exists:
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                actual_count = len(data.get('questions', []))
                                valid_json = True
                        except Exception as e:
                            print(f'  ERROR reading {file_path}: {str(e)[:60]}')
                    
                    status = '✓' if (file_exists and valid_json) else '✗'
                    print(f'  {status} {sec_id}: count={count}, file_exists={file_exists}, actual_count={actual_count}')
