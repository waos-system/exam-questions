#!/usr/bin/env python3
"""
Add Japanese translation templates to English exam questions.
For now, adds fields that frontend can display separately.
"""

import json
import os

def process_english_file(filepath):
    """Add ja_question and ja_explanation fields with guidance"""
    print(f"Processing {os.path.basename(filepath)}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data.get('questions', [])
    updated = 0
    
    for q in questions:
        # If question has ja_question already, skip
        if 'ja_question' in q and 'ja_explanation' in q:
            continue
        
        # Add placeholder if missing (frontend will show English as default)
        if 'ja_question' not in q:
            q['ja_question'] = '[Japanese translation needed: ' + q.get('question', '')[:50] + '...]'
            updated += 1
        
        if 'ja_explanation' not in q:
            q['ja_explanation'] = '[Japanese translation needed: ' + q.get('explanation', '')[:50] + '...]'
            updated += 1
    
    if updated > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Updated {updated} questions with translation placeholders")
    else:
        print(f"  Already has placeholders (0 updates)")
    
    return updated

def main():
    """Main entry point"""
    data_dir = 'data/english'
    files = sorted([
        os.path.join(data_dir, f) 
        for f in os.listdir(data_dir)
        if f.startswith('questions_en_') and f.endswith('.json')
    ])
    
    print(f"Found {len(files)} English exam files\n")
    
    total_updated = 0
    for filepath in files:
        total_updated += process_english_file(filepath)
    
    print(f"\nNote: Translation fields added. These should be filled with proper Japanese translations.")
    print(f"Total fields added: {total_updated}")

if __name__ == '__main__':
    main()
