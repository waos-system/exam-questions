"""
Reset all ja_* translation fields to the placeholder format so they can be
re-translated properly.
"""

import json
import glob


def reset_file(path):
    """Reset ja_* fields to placeholder format."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    changed = False
    for q in data.get('questions', []):
        jq = q.get('ja_question')
        if jq and not jq.startswith('[Japanese translation needed'):
            q['ja_question'] = f"[Japanese translation needed: {q.get('question', '')[:50]}...]"
            changed = True
        
        je = q.get('ja_explanation')
        if je and not je.startswith('[Japanese translation needed'):
            q['ja_explanation'] = f"[Japanese translation needed: {q.get('explanation', '')[:50]}...]"
            changed = True
    
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    return False


def main():
    patterns = [
        'data/english/questions_en_toeic_*.json',
        'data/english/questions_en_toefl_*.json',
    ]
    
    for pat in patterns:
        for fname in sorted(glob.glob(pat)):
            if reset_file(fname):
                print(f"✓ Reset {fname}")


if __name__ == '__main__':
    main()
