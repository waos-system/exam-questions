import json, os, random

# shuffle choices for specified files and update answer
files = [
    'data/au/questions_au_planning.json'
]

for path in files:
    print(f"Shuffling choices in {path}")
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    changed = False
    for q in data.get('questions', []):
        choices = q.get('choices')
        if not isinstance(choices, list) or len(choices) <=1:
            continue
        # Determine correct index
        if 'answer' in q:
            corr = q['answer']
        else:
            corr = None
        # generate new order
        idxs = list(range(len(choices)))
        random.shuffle(idxs)
        new_choices = [choices[i] for i in idxs]
        new_corr = idxs.index(corr) if corr is not None else None
        if new_choices != choices:
            q['choices'] = new_choices
            if corr is not None:
                q['answer'] = new_corr
            changed = True
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print('  updated file')
    else:
        print('  no change needed')
