import json, os, re
pattern = re.compile(r"AとC")
for fname in os.listdir('data/lang'):
    if fname.endswith('.json'):
        path = os.path.join('data/lang', fname)
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        for q in data.get('questions', []):
            opts = q.get('options') or {}
            corr = q.get('correct')
            for letter,text in opts.items():
                if pattern.search(text) and corr == letter:
                    print(f"File {fname} Q{q.get('id')} option {letter} text '{text}' correct {corr}")
