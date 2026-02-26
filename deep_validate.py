import json

try:
    with open('data/genres.json', 'r', encoding='utf-8') as f:
        genres = json.load(f)
    
    print('=== Deep validation of genres.json ===\n')
    
    # Check structure
    if not isinstance(genres, dict):
        print('ERROR: Root is not a dict')
        exit(1)
    
    subjects = genres.get('subjects', [])
    if not subjects:
        print('ERROR: No subjects')
        exit(1)
    
    for i, subject in enumerate(subjects):
        subj_name = subject.get('name', f'Subject{i}')
        exams = subject.get('exams', [])
        print(f'\nSubject {i}: {subj_name}')
        
        if not isinstance(exams, list):
            print(f'  ERROR: exams is not array')
            continue
        
        for j, exam in enumerate(exams):
            exam_name = exam.get('name', f'Exam{j}')
            sections = exam.get('sections', [])
            
            if not isinstance(sections, list):
                print(f'  ERROR: {exam_name} - sections is not array')
                continue
            
            print(f'    {exam_name}: {len(sections)} sections')
            
            # Check each section
            for k, sec in enumerate(sections):
                if not isinstance(sec, dict):
                    print(f'      ERROR: Section {k} is not dict')
                    continue
                
                if 'file' not in sec:
                    print(f'      WARNING: {sec.get("name", f"Sec{k}")} - no file')
                if 'count' not in sec:
                    print(f'      WARNING: {sec.get("name", f"Sec{k}")} - no count')
    
    print('\n✅ Structure validation complete!')
    
except json.JSONDecodeError as e:
    print(f'ERROR: JSON Syntax - {e}')
except Exception as e:
    print(f'ERROR: {e}')
