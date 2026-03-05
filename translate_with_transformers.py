"""
Translate TOEIC/TOEFL English texts to Japanese using Helsinki-NLP/opus-mt-en-ja model.
This uses a pre-trained offline translation model, no internet required.
"""

import json
import glob
from transformers import MarianMTModel, MarianTokenizer

# Load model and tokenizer
print("Loading translation model...")
model_name = "Helsinki-NLP/opus-mt-en-ja"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

print("Model loaded successfully")


def translate_text(text):
    """Translate English text to Japanese."""
    if not text or len(text.strip()) == 0:
        return ""
    
    # Tokenize
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    
    # Generate translation
    translated = model.generate(**inputs)
    
    # Decode
    result = tokenizer.decode(translated[0], skip_special_tokens=True)
    return result


def process_file(path):
    """Process a single JSON question file."""
    print(f"Processing {path}...")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR reading {path}: {e}")
        return 0, 0
    
    changed = False
    count_q = 0
    count_e = 0
    
    for i, q in enumerate(data.get('questions', [])):
        # Translate question if it's still in placeholder or English
        jq = q.get('ja_question', '')
        if not jq or jq == q.get('question', '') or jq.startswith('[Japanese translation needed'):
            try:
                new_q = translate_text(q.get('question', ''))
                q['ja_question'] = new_q
                changed = True
                count_q += 1
                print(f"  [{i+1}] Q: {q.get('question', '')[:50]}... → {new_q[:50]}...")
            except Exception as e:
                print(f"  [{i+1}] Q ERROR: {str(e)[:50]}")
        
        # Translate explanation if it's still in placeholder or English
        je = q.get('ja_explanation', '')
        if not je or je == q.get('explanation', '') or je.startswith('[Japanese translation needed'):
            try:
                new_e = translate_text(q.get('explanation', ''))
                q['ja_explanation'] = new_e
                changed = True
                count_e += 1
                # Don't print each explanation to avoid spam
            except Exception as e:
                print(f"  [{i+1}] E ERROR: {str(e)[:50]}")
    
    if changed:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Saved: {count_q} questions, {count_e} explanations")
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
            total_q += cq
            total_e += ce
    
    print(f"\n✓ Total translated: {total_q} questions, {total_e} explanations")


if __name__ == '__main__':
    main()
