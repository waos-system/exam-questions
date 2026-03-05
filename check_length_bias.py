import json

path='data/au/questions_au_planning.json'
with open(path,encoding='utf-8') as f:
    data=json.load(f)
count=0
for q in data.get('questions',[]):
    choices=q['choices']
    corr=q['answer']
    # compute lengths
    lens=[len(c) for c in choices]
    maxlen=max(lens)
    if lens[corr]==maxlen:
        count+=1
print(f'{count}/{len(data.get("questions",[]))} correct options still longest')
