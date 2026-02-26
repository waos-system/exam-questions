import json
import os

# Final comprehensive validation of all error sections
error_sections = {
    'SQL': [
        'questions_sql_constraints.json',
        'questions_sql_window_functions.json', 
        'questions_sql_advanced.json'
    ],
    'Linux': [
        'questions_linux_commands.json',
        'questions_linux_users_groups.json',
        'questions_linux_boot_kernel.json',
        'questions_linux_firewall.json',
        'questions_linux_network_dns.json',
        'questions_linux_storage.json',
        'questions_linux_sysadmin.json'
    ]
}

def validate_file(filepath):
    """Validate a single question file"""
    if not os.path.exists(filepath):
        return {'exists': False, 'error': 'File not found'}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        questions = data.get('questions', [])
        if not isinstance(questions, list):
            return {'exists': True, 'error': 'Questions is not a list'}
        
        # Validate each question has required fields
        answers = ['A', 'B', 'C', 'D', 'E', 'F']
        invalid_questions = []
        
        for q in questions:
            errors = []
            
            if not q.get('id'):
                errors.append('missing_id')
            if not q.get('question'):
                errors.append('missing_question')
            
            options = q.get('options')
            if not isinstance(options, dict) or len(options) == 0:
                errors.append('invalid_options')
            
            correct = q.get('correct')
            if not correct or (isinstance(correct, str) and correct.upper() not in answers):
                errors.append('invalid_correct')
            
            if not q.get('explanation'):
                errors.append('missing_explanation')
            
            if errors:
                invalid_questions.append({'id': q.get('id'), 'errors': errors})
        
        return {
            'exists': True,
            'total': len(questions),
            'valid': len(questions) - len(invalid_questions),
            'invalid_count': len(invalid_questions),
            'sample_invalid': invalid_questions[:3] if invalid_questions else []
        }
        
    except json.JSONDecodeError as e:
        return {'exists': True, 'error': f'JSON error: {str(e)[:50]}'}
    except Exception as e:
        return {'exists': True, 'error': str(e)[:50]}

print('='*60)
print('FINAL VALIDATION OF ERROR SECTIONS')
print('='*60)

base_path = 'data/lang/'
total_files = 0
total_valid = 0

for category, files in error_sections.items():
    print(f'\n{category} Sections:')
    category_valid = 0
    
    for filename in files:
        filepath = os.path.join(base_path, filename)
        result = validate_file(filepath)
        total_files += 1
        
        if result.get('exists'):
            total = result.get('total', 0)
            valid = result.get('valid', 0)
            total_valid += valid
            category_valid += valid
            
            status = '✓' if valid == total else '✗'
            print(f'  {status} {filename}: {valid}/{total} valid')
            
            if result.get('invalid_count', 0) > 0:
                print(f'      Sample invalid: {result["sample_invalid"]}')
        else:
            print(f'  ✗ {filename}: {result.get("error")}')

print(f'\n{"-"*60}')
print(f'Total Files: {total_files}')
print(f'Total Valid Questions: {total_valid}')
print(f'\n✓ Fix Complete!' if total_valid == sum(len(files) for files in error_sections.values()) * 50 else '✗ Issues Remaining')
