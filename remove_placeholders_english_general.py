"""
Remove Japanese translation needed placeholders from English general files.
This removes the placeholder text for files that don't need Japanese translation.
"""

import json
import glob


def process_file(path):
    """Remove Japanese translation needed placeholders."""
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
        # Remove placeholder from ja_question
        jq = q.get('ja_question', '')
        if jq.startswith('[Japanese translation needed'):
            q['ja_question'] = ''
            changed = True
            count_q += 1
        
        # Remove placeholder from ja_explanation
        je = q.get('ja_explanation', '')
        if je.startswith('[Japanese translation needed'):
            q['ja_explanation'] = ''
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
    """Process all English general files (excluding TOEIC/TOEFL)."""
    patterns = [
        'data/english/questions_en_*.json',
    ]
    
    # Exclude TOEIC/TOEFL files
    exclude_patterns = ['toeic', 'toefl']
    
    total_q = 0
    total_e = 0
    
    print("Removing Japanese translation needed placeholders from English general files...")
    
    for pat in patterns:
        for fname in sorted(glob.glob(pat)):
            # Skip TOEIC/TOEFL files
            if any(excl in fname.lower() for excl in exclude_patterns):
                continue
                
            cq, ce = process_file(fname)
            if cq + ce > 0:
                print(f"  ✓ {fname}: {cq} questions, {ce} explanations")
            total_q += cq
            total_e += ce
    
    print(f"\nTotal removed: {total_q} questions, {total_e} explanations")
    print("English general files now have empty ja_* fields instead of placeholders.")


if __name__ == '__main__':
    main()
