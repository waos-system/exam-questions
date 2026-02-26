import urllib.request
import json

print('Fetching genres.json from localhost:8080...')

try:
    response = urllib.request.urlopen('http://localhost:8080/data/genres.json')
    content = response.read().decode('utf-8')
    data = json.loads(content)
    
    print(f'✓ HTTP Status: {response.status}')
    print(f'✓ Content-Type: {response.headers.get("Content-Type")}')
    print(f'✓ Fetched size: {len(content)} bytes')
    print(f'✓ Subjects: {len(data.get("subjects", []))}')
    
    # Check SQL and Linux
    for subject in data.get('subjects', []):
        for exam in subject.get('exams', []):
            if exam.get('id') in ['lang_sql', 'lang_linux']:
                sections = exam.get('sections', [])
                print(f'✓ {exam.get("name")}: {len(sections)} sections')
                
except Exception as e:
    print(f'ERROR: {e}')
