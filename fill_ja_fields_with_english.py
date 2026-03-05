"""
Fill ja_question and ja_explanation fields with English text (as placeholders)
for all TOEIC/TOEFL files not yet translated.

This ensures all files have consistent ja_* fields that can later be replaced
with actual translations when they become available.
"""

import json
import glob


def process_file(path):
    """Fill ja_* fields with English text if they are missing or placeholder."""
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
        # Question - fill with English if missing or is placeholder
        jq = q.get('ja_question', '')
        orig_q = q.get('question', '')
        
        if not jq or jq.startswith('[Japanese translation needed'):
            q['ja_question'] = orig_q
            changed = True
            count_q += 1
        
        # Explanation - fill with English if missing or is placeholder
        je = q.get('ja_explanation', '')
        orig_e = q.get('explanation', '')
        
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
    
    print("Filling ja_* fields with English text...")
    
    for pat in patterns:
        for fname in sorted(glob.glob(pat)):
            cq, ce = process_file(fname)
            if cq + ce > 0:
                print(f"  ✓ {fname:<50} {cq} questions, {ce} explanations")
            total_q += cq
            total_e += ce
    
    print(f"\nTotal updated: {total_q} questions, {total_e} explanations")
    print("All ja_* fields now contain English text as placeholders.")
    print("These can be replaced with Japanese translations later.")


if __name__ == '__main__':
    main()
