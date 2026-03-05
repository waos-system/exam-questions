"""
Translate remaining English fields in general English categories (non-TOEIC/TOEFL)
using Google Translate via googletrans library.

This handles files like business, grammar, vocabulary, etc. that weren't part of
the TOEIC/TOEFL translation process.
"""

import json
import glob
import time
from googletrans import Translator

# Initialize translator
translator = Translator()


def translate_text(text, max_retries=3):
    """Translate English text to Japanese with retries."""
    if not text or len(text.strip()) == 0:
        return ""

    for attempt in range(max_retries):
        try:
            # googletrans API: translate(text, dest='ja')
            result = translator.translate(text, dest='ja')
            if result and hasattr(result, 'text'):
                return result.text
            return text  # Fallback to original if translation fails
        except Exception as e:
            print(f"    Translation error (attempt {attempt+1}/{max_retries}): {str(e)[:60]}")
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait before retry
            else:
                print(f"    Failed after {max_retries} attempts, keeping original")
                return text  # Return original text on final failure


def process_file(path):
    """Process a single JSON question file and translate remaining English fields."""
    print(f"Processing {path}...")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  ERROR reading {path}: {e}")
        return 0, 0

    changed = False
    count_q = 0
    count_e = 0

    for i, q in enumerate(data.get('questions', [])):
        # Question - translate if still in placeholder
        jq = q.get('ja_question', '')
        orig_q = q.get('question', '')

        if jq.startswith('[Japanese translation needed'):
            try:
                new_q = translate_text(orig_q)
                if new_q and new_q != orig_q:
                    q['ja_question'] = new_q
                    changed = True
                    count_q += 1
                    print(f"  ✓ Q[{i+1}]: {orig_q[:60]}... → {new_q[:60]}...")
            except Exception as e:
                print(f"  ✗ Q[{i+1}] ERROR: {str(e)[:50]}")

        # Explanation - translate if still in placeholder
        je = q.get('ja_explanation', '')
        orig_e = q.get('explanation', '')

        if je.startswith('[Japanese translation needed'):
            try:
                new_e = translate_text(orig_e)
                if new_e and new_e != orig_e:
                    q['ja_explanation'] = new_e
                    changed = True
                    count_e += 1
            except Exception as e:
                print(f"  ✗ E[{i+1}] ERROR: {str(e)[:50]}")

        # Add delay to avoid rate limiting
        if (count_q + count_e) % 5 == 0:
            time.sleep(0.5)

    if changed:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  ✅ Saved: {count_q} questions, {count_e} explanations translated")
        except Exception as e:
            print(f"  ERROR writing {path}: {e}")
            return 0, 0

    return count_q, count_e


def main():
    """Process all general English question files (excluding TOEIC/TOEFL)."""
    patterns = [
        'data/english/questions_en_*.json',
    ]

    # Exclude TOEIC/TOEFL files (already translated)
    exclude_patterns = [
        'data/english/questions_en_toeic_*.json',
        'data/english/questions_en_toefl_*.json',
    ]

    total_q = 0
    total_e = 0

    print("=" * 70)
    print("Translating remaining English fields in General English categories")
    print("=" * 70)

    for pat in patterns:
        for fname in sorted(glob.glob(pat)):
            # Skip TOEIC/TOEFL files
            if any(glob.fnmatch.fnmatch(fname, excl) for excl in exclude_patterns):
                continue

            cq, ce = process_file(fname)
            total_q += cq
            total_e += ce
            print()

            # Save progress after each file
            time.sleep(2)  # Longer delay between files

    print("=" * 70)
    print(f"✅ Total translated: {total_q} questions, {total_e} explanations")
    print("=" * 70)


if __name__ == '__main__':
    main()
