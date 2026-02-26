import json

# genres.json から宣言されている count 値
genres_count = {
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

# 実際のファイル内の問題数
actual_files = {
    'data/lang/questions_sql_select.json': 'sql_select',
    'data/lang/questions_sql_functions.json': 'sql_functions',
    'data/lang/questions_sql_group.json': 'sql_group',
    'data/lang/questions_sql_join.json': 'sql_join',
    'data/lang/questions_sql_subquery.json': 'sql_subquery',
    'data/lang/questions_sql_dml_ddl.json': 'sql_dml_ddl',
    'data/lang/questions_sql_constraints.json': 'sql_constraints',
    'data/lang/questions_sql_window_functions.json': 'sql_window_functions',
    'data/lang/questions_sql_advanced.json': 'sql_advanced',
    'data/lang/questions_linux_commands.json': 'linux_commands',
    'data/lang/questions_linux_filesystem.json': 'linux_filesystem',
    'data/lang/questions_linux_process.json': 'linux_process',
    'data/lang/questions_linux_network.json': 'linux_network',
    'data/lang/questions_linux_packages.json': 'linux_packages',
    'data/lang/questions_linux_users_groups.json': 'linux_users_groups',
    'data/lang/questions_linux_boot_kernel.json': 'linux_boot_kernel',
    'data/lang/questions_linux_firewall.json': 'linux_firewall',
    'data/lang/questions_linux_network_dns.json': 'linux_network_dns',
    'data/lang/questions_linux_storage.json': 'linux_storage',
    'data/lang/questions_linux_sysadmin.json': 'linux_sysadmin',
}

print('Count mismatch check:\n')
mismatches = []
for filepath, key in actual_files.items():
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            actual_count = len(data.get('questions', []))
            expected_count = genres_count[key]
            match = '✓' if actual_count == expected_count else '✗ MISMATCH'
            print(f'{match} {key}: expected={expected_count}, actual={actual_count}')
            if actual_count != expected_count:
                mismatches.append((key, expected_count, actual_count))
    except Exception as e:
        print(f'ERROR {key}: {str(e)[:50]}')

if mismatches:
    print(f'\n⚠️ Found {len(mismatches)} mismatches:')
    for key, expected, actual in mismatches:
        print(f'  - {key}: genres.json says {expected}, but file has {actual}')
else:
    print('\n✅ All counts match!')
