import json
import os

# Scan English exam files for missing Japanese translations
# Assumes English files are in data/lang/questions_toeic_*.json etc.

english_prefixes = ['questions_toeic', 'questions_toefl', 'questions_eiken', 'questions_business_english']

for fname in os.listdir('data/lang'):
    if any(fname.startswith(pref) for pref in english_prefixes):
        path = os.path.join('data/lang', fname)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        qlist = data.get('questions', [])
        missing = 0
        for q in qlist:
            # english text in q['question'] and q['explanation']
            if 'ja_question' not in q or 'ja_explanation' not in q:
                missing += 1
        print(f"{fname}: {missing}/{len(qlist)} questions missing Japanese translations")

print("\nTo add translations, extend each question with 'ja_question' and 'ja_explanation' fields.")
