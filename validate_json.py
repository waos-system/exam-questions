import json

try:
    with open('data/genres.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check structure
    if not isinstance(data, dict):
        print('ERROR: Root is not dict')
        exit(1)
    
    if 'subjects' not in data:
        print('ERROR: No subjects key')
        exit(1)
    
    if not isinstance(data['subjects'], list):
        print('ERROR: subjects is not a list')
        exit(1)
    
    # Check all exams and sections
    exam_count = 0
    section_count = 0
    section_without_file = []
    
    for subject in data['subjects']:
        for exam in subject.get('exams', []):
            exam_count += 1
            for section in exam.get('sections', []):
                section_count += 1
                if 'file' not in section:
                    section_without_file.append(f"{exam.get('name', '?')}/{section.get('name', '?')}")
                if 'count' not in section:
                    print(f"WARNING: {section.get('name')} - no count")
    
    print(f'✅ genres.json is valid')
    print(f'   Exams: {exam_count}')
    print(f'   Sections: {section_count}')
    
    if section_without_file:
        print(f'\n⚠️ Sections without file ({len(section_without_file)}):')
        for item in section_without_file[:5]:
            print(f'   - {item}')
    else:
        print(f'\n✅ All sections have file property')
        
except json.JSONDecodeError as e:
    print(f'❌ JSON Syntax Error: {e}')
except Exception as e:
    print(f'❌ Error: {e}')
