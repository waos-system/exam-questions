import json

# SQL と Linux の実際の count 値
corrections = {
    'sql_select': 10,
    'sql_functions': 10,
    'sql_group': 10,
    'sql_join': 10,
    'sql_subquery': 10,
    'sql_dml_ddl': 10,
    'sql_constraints': 50,
    'sql_window_functions': 50,
    'sql_advanced': 50,
    'linux_commands': 50,
    'linux_filesystem': 50,
    'linux_process': 50,
    'linux_network': 50,
    'linux_packages': 50,
    'linux_users_groups': 50,
    'linux_boot_kernel': 50,
    'linux_firewall': 50,
    'linux_network_dns': 50,
    'linux_storage': 50,
    'linux_sysadmin': 50,
}

# Load genres.json
with open('data/genres.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update counts
changes = 0
for subject in data['subjects']:
    if 'exams' not in subject:
        continue
    for exam in subject['exams']:
        if 'sections' not in exam:
            continue
        for section in exam['sections']:
            sec_id = section.get('id')
            if sec_id in corrections:
                old_count = section.get('count')
                new_count = corrections[sec_id]
                if old_count != new_count:
                    print(f'Updating {sec_id}: {old_count} -> {new_count}')
                    section['count'] = new_count
                    changes += 1

# Save
with open('data/genres.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nTotal changes: {changes}')
print('OK: genres.json updated')
