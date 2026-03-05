import json, os, re

pattern = re.compile(r"AとC")

def check_file(path):
    with open(path, encoding='utf-8') as f:
        data=json.load(f)
    for q in data.get('questions',[]):
        opts = q.get('options') or {}
        for letter,text in opts.items():
            if pattern.search(text):
                corr = q.get('correct') or q.get('answer')
                # if corr is numeric convert to letter
                if isinstance(corr,int):
                    # map index to letter
                    corr = "ABCD"[corr] if corr < 4 else corr
                if corr == letter:
                    print(f"Anomaly in {os.path.basename(path)} {q.get('id')} choice {letter}: '{text}' correct={corr}")

for fname in os.listdir('data/lang'):
    if fname.startswith('questions_') and fname.endswith('.json'):
        check_file(os.path.join('data/lang', fname))
