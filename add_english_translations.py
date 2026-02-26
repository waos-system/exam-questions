#!/usr/bin/env python3
"""
Add Japanese translations to English exam questions, using Claude via Anthropic API.
For each English question, generate a Japanese version of the question and explanation.
"""

import json
import os
import sys
import anthropic

# English exam prefixes to process
ENGLISH_EXAMS = [
    'questions_toeic',
    'questions_toefl',
    'questions_eiken',
    'questions_business_english'
]

def get_english_exams():
    """List all English exam files that need translations"""
    files = []
    data_dir = 'data/english'
    for fname in os.listdir(data_dir):
        if fname.startswith('questions_en_') and fname.endswith('.json'):
            files.append(os.path.join(data_dir, fname))
    return sorted(files)

def needs_translation(question):
    """Check if question is missing Japanese translations"""
    return 'ja_question' not in question or 'ja_explanation' not in question

def translate_to_japanese(client, english_text, context_type='question'):
    """Use Claude to translate English text to Japanese"""
    prompt = f"""Translate the following {context_type} to natural, clear Japanese that a native speaker would understand:

{english_text}

Respond ONLY with the Japanese translation, no additional text."""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text.strip()

def process_english_file(filepath, client):
    """Add Japanese translations to an English question file"""
    print(f"\nProcessing {os.path.basename(filepath)}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data.get('questions', [])
    updated = 0
    
    for i, q in enumerate(questions):
        if needs_translation(q):
            print(f"  Translating Q{i+1}...", end='', flush=True)
            
            try:
                # Translate question
                if 'ja_question' not in q and 'question' in q:
                    q['ja_question'] = translate_to_japanese(client, q['question'], 'question')
                
                # Translate explanation
                if 'ja_explanation' not in q and 'explanation' in q:
                    q['ja_explanation'] = translate_to_japanese(client, q['explanation'], 'explanation')
                
                updated += 1
                print(" ✓")
            except Exception as e:
                print(f" ✗ ({str(e)[:50]})")
                continue
    
    if updated > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Saved {updated} translations")
    else:
        print(f"  Already complete (0 updates needed)")
    
    return updated

def main():
    """Main entry point"""
    files = get_english_exams()
    
    if not files:
        print("No English exam files found")
        return
    
    print(f"Found {len(files)} English exam files")
    
    # Initialize Anthropic client
    try:
        client = anthropic.Anthropic()
    except Exception as e:
        print(f"Error: Could not initialize Anthropic client: {e}")
        print("Please set ANTHROPIC_API_KEY environment variable")
        return
    
    total_updated = 0
    for filepath in files:
        total_updated += process_english_file(filepath, client)
    
    print(f"\n✓ Total translations added: {total_updated}")

if __name__ == '__main__':
    main()
