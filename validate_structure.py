import json

print('Genres.json structure validation:\n')

try:
    with open('data/genres.json', 'r', encoding='utf-8') as f:
        genres = json.load(f)
    
    total_exams = 0
    total_sections = 0
    missing_sections = []
    
    for category in genres:
        cat_name = category.get('name', 'Unknown')
        if 'exams' not in category:
            print(f'ERROR: Category "{cat_name}" missing "exams" property')
            continue
        
        for exam in category['exams']:
            exam_name = exam.get('name', 'Unknown')
            total_exams += 1
            
            if 'sections' not in exam:
                print(f'ERROR: Exam "{exam_name}" missing "sections" property')
                missing_sections.append(f"{cat_name}/{exam_name}")
                continue
            
            sections = exam['sections']
            if not isinstance(sections, list):
                print(f'ERROR: Exam "{exam_name}" sections is not an array')
                missing_sections.append(f"{cat_name}/{exam_name}")
                continue
            
            total_sections += len(sections)
            
            # Check each section
            for sec in sections:
                if 'file' not in sec:
                    print(f'WARNING: Section "{sec.get("name", "Unknown")}" in "{exam_name}" missing "file"')
                if 'count' not in sec:
                    print(f'WARNING: Section "{sec.get("name", "Unknown")}" in "{exam_name}" missing "count"')

    print(f'✓ Total exams: {total_exams}')
    print(f'✓ Total sections: {total_sections}')
    
    if missing_sections:
        print(f'\n⚠️ Exams missing sections property:')
        for item in missing_sections:
            print(f'  - {item}')
    else:
        print('\n✅ All exams have sections property')
        
except Exception as e:
    print(f'ERROR: {str(e)}')
