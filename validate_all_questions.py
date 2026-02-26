import json

# Comprehensive test of the fixes
test_files = [
    'data/lang/questions_sql_constraints.json',
    'data/lang/questions_sql_window_functions.json',
    'data/lang/questions_sql_advanced.json',
    'data/lang/questions_linux_commands.json',
    'data/lang/questions_linux_users_groups.json',
]

def test_all_questions():
    total_tests = 0
    passed_tests = 0
    
    for filepath in test_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            questions = data.get('questions', [])
            print(f'\n{filepath.split("/")[-1]}:')
            print(f'  Total: {len(questions)} questions')
            
            # Test each question
            valid_count = 0
            for q in questions:
                total_tests += 1
                
                # Check required fields (as they appear in JSON files)
                has_id = 'id' in q
                has_question = 'question' in q
                has_options = 'options' in q and isinstance(q['options'], dict)
                has_correct = 'correct' in q and isinstance(q['correct'], int)
                has_explanation = 'explanation' in q
                
                if all([has_id, has_question, has_options, has_correct, has_explanation]):
                    valid_count += 1
                    passed_tests += 1
                else:
                    print(f'    Invalid Q{q.get("id")}: id={has_id}, q={has_question}, opts={has_options}, correct={has_correct}, exp={has_explanation}')
            
            print(f'  ✓ Valid: {valid_count}/{len(questions)}')
            
        except Exception as e:
            print(f'{filepath}: ERROR - {str(e)[:100]}')
    
    print(f'\n\nTotal: {passed_tests}/{total_tests} questions valid')
    print('✓ All questions have required structure!' if passed_tests == total_tests else '✗ Some questions invalid')
    return passed_tests == total_tests

if __name__ == '__main__':
    test_all_questions()
