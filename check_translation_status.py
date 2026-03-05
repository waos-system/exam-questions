"""
Check which TOEIC/TOEFL files have been translated to Japanese.
"""

import json
import glob


def check_file(path):
    """Check how many questions have Japanese translations."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total = 0
    ja_q = 0
    ja_e = 0
    
    for q in data.get('questions', []):
        total += 1
        
        # Check if ja_question has been translated (not just English)
        jq = q.get('ja_question', '')
        if jq and jq != q.get('question', '') and not jq.startswith('['):
            ja_q += 1
        
        # Check if ja_explanation has been translated (not just English)
        je = q.get('ja_explanation', '')
        if je and je != q.get('explanation', '') and not je.startswith('['):
            ja_e += 1
    
    return total, ja_q, ja_e


def main():
    patterns = [
        'data/english/questions_en_toeic_*.json',
        'data/english/questions_en_toefl_*.json',
    ]
    
    print("Translation Status for TOEIC/TOEFL Files")
    print("=" * 70)
    
    total_all = 0
    total_ja_q = 0
    total_ja_e = 0
    
    for pat in patterns:
        for fname in sorted(glob.glob(pat)):
            total, ja_q, ja_e = check_file(fname)
            status_q = f"✓ {ja_q}/{total}" if ja_q == total else f"✗ {ja_q}/{total}"
            status_e = f"✓ {ja_e}/{total}" if ja_e == total else f"✗ {ja_e}/{total}"
            
            print(f"{fname:<50} Q:{status_q:-<10} E:{status_e:-<10}")
            
            total_all += total
            total_ja_q += ja_q
            total_ja_e += ja_e
    
    print("=" * 70)
    print(f"TOTAL: Questions translated: {total_ja_q}/{total_all} ({100*total_ja_q//total_all}%)")
    print(f"TOTAL: Explanations translated: {total_ja_e}/{total_all} ({100*total_ja_e//total_all}%)")


if __name__ == '__main__':
    main()
