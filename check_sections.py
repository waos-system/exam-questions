import json

print('=== Checking genres.json structure ===\n')

with open('data/genres.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check the top-level structure
if 'subjects' not in data:
    print('ERROR: No "subjects" key in genres.json!')
    exit(1)

print(f'Found {len(data["subjects"])} subjects\n')

# Check all exams for sections
missing_sections = []
for subject in data['subjects']:
    subject_name = subject.get('name', 'Unknown')
    print(f'Subject: {subject_name}')
    
    for exam in subject.get('exams', []):
        exam_name = exam.get('name', 'Unknown')
        
        if 'sections' not in exam:
            print(f'  ERROR: Exam "{exam_name}" - NO sections property')
            missing_sections.append(exam_name)
        elif not isinstance(exam['sections'], list):
            print(f'  ERROR: Exam "{exam_name}" - sections is not array')
            missing_sections.append(exam_name)
        else:
            print(f'  OK: Exam "{exam_name}" has {len(exam["sections"])} sections')

print(f'\n=== Summary ===')
if missing_sections:
    print(f'ERROR: {len(missing_sections)} exams missing sections:')
    for name in missing_sections:
        print(f'  - {name}')
else:
    print('OK: All exams have sections property')
