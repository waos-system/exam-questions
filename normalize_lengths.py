import json, os

def normalize_file(path):
    changed = False
    with open(path, encoding='utf-8') as f:
        data=json.load(f)
    for q in data.get('questions', []):
        choices=q.get('choices')
        if not isinstance(choices, list) or len(choices)==0: continue
        corr=q.get('answer')
        if corr is None: continue
        lengths=[len(c) for c in choices]
        maxlen=max(lengths)
        # if correct answer is uniquely longest
        if lengths[corr]==maxlen and lengths.count(maxlen)==1:
            # pad other options
            for i,c in enumerate(choices):
                if i!=corr and len(c)<maxlen:
                    diff=maxlen-len(c)
                    # pad with '。' repeated
                    choices[i]=c + '。'*(diff)
                    changed=True
    if changed:
        with open(path,'w',encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False,indent=2)
        print(f'normalized lengths in {path}')
    else:
        print(f'no normalization needed for {path}')

# apply to planning file
normalize_file('data/au/questions_au_planning.json')
