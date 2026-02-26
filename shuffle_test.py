import json
import random

# verify that randomizeQuestion in JS produces different answer distribution
# We can't execute JS here; replicate algorithm in Python to ensure randomness

def randomize_question(q):
    # q has 'choices' list and 'answer' index
    choices = q['choices'][:]
    idxs = list(range(len(choices)))
    random.shuffle(idxs)
    new_choices = [choices[i] for i in idxs]
    new_answer = idxs.index(q['answer'])
    return new_choices, new_answer

# load file
file = 'data/lang/questions_sql_constraints.json'
with open(file, 'r', encoding='utf-8') as f:
    data = json.load(f)
questions = data.get('questions', [])

# convert options->choices and correct->answer
answers_map = ['A','B','C','D','E','F']
converted = []
for q in questions:
    choices = list(q.get('options', {}).values())
    correct = q.get('correct')
    answer_idx = answers_map.index(correct) if isinstance(correct, str) and correct in answers_map else 0
    converted.append({'choices': choices, 'answer': answer_idx})

# do many randomizations and count distribution for first question
counts = [0]*len(converted[0]['choices'])
for _ in range(1000):
    _, ans = randomize_question(converted[0])
    counts[ans] += 1

print('Distribution of answer positions after shuffling', counts)
if max(counts) - min(counts) > 200:
    print('Warning: distribution uneven')
else:
    print('Shuffle seems random enough')
