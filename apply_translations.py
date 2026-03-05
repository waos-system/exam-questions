"""
Apply comprehensive dictionary-based translations to TOEIC/TOEFL questions.
This script uses the translation dictionary to fill ja_question and ja_explanation
fields that currently contain placeholders.
"""

import json
import glob
from translate_dict import translate_field, TRANSLATION_DICTIONARY


def process_file(path):
    """Process a single JSON question file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR reading {path}: {e}")
        return 0, 0
    
    changed = False
    count_q = 0
    count_e = 0
    
    for q in data.get('questions', []):
        # Translate question
        jq = q.get('ja_question', '')
        if jq and jq.startswith('[Japanese translation needed'):
            orig_q = q.get('question', '')
            new_q = translate_field(orig_q, TRANSLATION_DICTIONARY)
            q['ja_question'] = new_q
            changed = True
            count_q += 1
        
        # Translate explanation
        je = q.get('ja_explanation', '')
        if je and je.startswith('[Japanese translation needed'):
            orig_e = q.get('explanation', '')
            new_e = translate_field(orig_e, TRANSLATION_DICTIONARY)
            q['ja_explanation'] = new_e
            changed = True
            count_e += 1
    
    if changed:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"ERROR writing {path}: {e}")
            return 0, 0
    
    return count_q, count_e


def main():
    """Process all TOEIC/TOEFL question files."""
    patterns = [
        'data/english/questions_en_toeic_*.json',
        'data/english/questions_en_toefl_*.json',
    ]
    
    total_q = 0
    total_e = 0
    
    for pat in patterns:
        for fname in sorted(glob.glob(pat)):
            cq, ce = process_file(fname)
            if cq + ce > 0:
                print(f"✓ {fname}: {cq} questions, {ce} explanations")
            total_q += cq
            total_e += ce
    
    print(f"\nTotal translated: {total_q} questions, {total_e} explanations")
    if total_q + total_e == 0:
        print("No placeholders found or all already translated.")


if __name__ == '__main__':
    main()
