"""
Fill ja_question and ja_explanation with English text as placeholders.
This allows the frontend to display the fields even if translations aren't ready yet.
Users can later replace these with actual Japanese translations.
"""

import json
import glob


def process_file(path):
    """Fill ja_* fields with English text."""
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
        # Question
        jq = q.get('ja_question', '')
        orig_q = q.get('question', '')
        
        # If ja_question is missing, placeholder, or doesn't match English,
        # fill with English copy
        if not jq or jq.startswith('[Japanese translation needed') or jq == orig_q:
            # Only update if empty or placeholder
            if not jq or jq.startswith('[Japanese translation needed'):
                q['ja_question'] = orig_q
                changed = True
                count_q += 1
        
        # Explanation
        je = q.get('ja_explanation', '')
        orig_e = q.get('explanation', '')
        
        if not je or je.startswith('[Japanese translation needed') or je == orig_e:
            if not je or je.startswith('[Japanese translation needed'):
                q['ja_explanation'] = orig_e
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
    
    print("Filling ja_* fields with English text as placeholders...")
    
    for pat in patterns:
        for fname in sorted(glob.glob(pat)):
            cq, ce = process_file(fname)
            if cq + ce > 0:
                print(f"✓ {fname}: {cq} questions, {ce} explanations")
            total_q += cq
            total_e += ce
    
    print(f"\nTotal updated: {total_q} questions, {total_e} explanations")


if __name__ == '__main__':
    main()
