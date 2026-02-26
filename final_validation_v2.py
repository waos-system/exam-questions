import json
import os

# Final comprehensive validation with proper format detection
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
    """Validate a single question file with format detection"""
    if not os.path.exists(filepath):
        return {'exists': False, 'error': 'File not found'}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        questions = data.get('questions', [])
        if not isinstance(questions, list):
            return {'exists': True, 'error': 'Questions is not a list'}
        
        # Validate each question
        answers = ['A', 'B', 'C', 'D', 'E', 'F']
        invalid_questions = []
        
        for q in questions:
            errors = []
            
            if not q.get('id'):
                errors.append('missing_id')
            if not q.get('question'):
                errors.append('missing_question')
            
            # Format 1: options (dict) + correct (string)
            # Format 2: choices (array) + answer (int)
            has_options = isinstance(q.get('options'), dict) and len(q.get('options', {})) > 0
            has_correct_str = isinstance(q.get('correct'), str) and q['correct'].upper() in answers
            
            has_choices = isinstance(q.get('choices'), list) and len(q.get('choices', [])) > 0
            has_answer_int = isinstance(q.get('answer'), int)
            
            # Either format 1 OR format 2 should be valid
            if not ((has_options and has_correct_str) or (has_choices and has_answer_int)):
                errors.append('invalid_choices_or_options')
            
            if not q.get('explanation'):
                errors.append('missing_explanation')
            
            if errors:
                invalid_questions.append({'id': q.get('id'), 'errors': errors})
        
        return {
            'exists': True,
            'total': len(questions),
            'valid': len(questions) - len(invalid_questions),
            'invalid_count': len(invalid_questions),
            'sample_invalid': invalid_questions[:2] if invalid_questions else []
        }
        
    except json.JSONDecodeError as e:
        return {'exists': True, 'error': f'JSON error: {str(e)[:50]}'}
    except Exception as e:
        return {'exists': True, 'error': str(e)[:50]}

print('='*70)
print('FINAL VALIDATION OF ERROR SECTIONS (Format Detection)')
print('='*70)

base_path = 'data/lang/'
total_files = 0
total_valid = 0

for category, files in error_sections.items():
    print(f'\n{category} Sections:')
    
    for filename in files:
        filepath = os.path.join(base_path, filename)
        result = validate_file(filepath)
        total_files += 1
        
        if result.get('exists'):
            total = result.get('total', 0)
            valid = result.get('valid', 0)
            total_valid += valid
            
            status = '✓' if valid == total else '✗'
            print(f'  {status} {filename}: {valid}/{total} valid')
            
            if result.get('invalid_count', 0) > 0:
                print(f'      Issues: {result.get("sample_invalid")}')
        else:
            print(f'  ✗ {filename}: {result.get("error")}')

print(f'\n{"-"*70}')
print(f'Total Questions Validated: {total_files * 50}')
print(f'Total Valid Questions: {total_valid}')

expected = sum(len(files) for files in error_sections.values()) * 50
if total_valid == expected:
    print(f'\n✓ ALL FIXES COMPLETE - All {expected} questions are valid!')
else:
    print(f'\n✗ {expected - total_valid} questions still have issues')
