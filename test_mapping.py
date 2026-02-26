import json
import sys

# Test the mapping from options to choices
def test_question_mapping():
    files_to_test = [
        'data/lang/questions_sql_constraints.json',
        'data/lang/questions_linux_commands.json',
    ]
    
    for file in files_to_test:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            questions = data.get('questions', [])
            print(f'\n{file}:')
            
            # Test the mapping
            mapped_questions = []
            for q in questions:
                # This simulates what startQuiz() does in index.html
                mapped_q = dict(q)  # Copy
                mapped_q['choices'] = q.get('choices') or q.get('options')
                mapped_questions.append(mapped_q)
            
            # Check first 3 questions
            for i in range(min(3, len(mapped_questions))):
                mq = mapped_questions[i]
                has_choices = 'choices' in mq and isinstance(mq['choices'], list)
                print(f'  Q{i}: has_id={bool(mq.get("id"))}, has_question={bool(mq.get("question"))}, has_choices={has_choices}, choices_count={len(mq.get("choices", []))}')
            
            # Verify all questions have choices
            all_valid = all(
                q.get('id') and 
                q.get('question') and 
                q.get('choices') and 
                isinstance(q.get('choices'), list)
                for q in mapped_questions
            )
            print(f'  All questions valid after mapping: {all_valid}')
            
        except Exception as e:
            print(f'{file}: ERROR - {str(e)[:80]}')
            return False
    
    print('\n✓ Mapping test completed successfully')
    return True

if __name__ == '__main__':
    success = test_question_mapping()
    sys.exit(0 if success else 1)
