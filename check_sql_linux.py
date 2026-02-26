import json

# Load and check genre.json
with open('data/genres.json', 'r', encoding='utf-8') as f:
    genres = json.load(f)

# Get SQL and Linux exams
for subject in genres['subjects']:
    for exam in subject.get('exams', []):
        if exam.get('id') in ['lang_sql', 'lang_linux']:
            print(f"Exam: {exam.get('name')}")
            print(f"  ID: {exam.get('id')}")
            print(f"  Has sections: {'sections' in exam}")
            
            sections = exam.get('sections', [])
            print(f"  Section count: {len(sections)}")
            
            for sec in sections[:3]:
                print(f"    - {sec.get('id')}: count={sec.get('count')}, file={sec.get('file')}")
            print()
