"""Translate TOEIC/TOEFL English questions and explanations into Japanese.

This script looks for files in data/english matching "questions_en_toeic*" or
"questions_en_toefl*" and uses googletrans to populate any
"ja_question"/"ja_explanation" fields that start with
"[Japanese translation needed".

It overwrites the file in place and prints a summary of how many entries were
translated.
"""

import json
import glob
from googletrans import Translator

translator = Translator()

def translate_text(text):
    # some placeholders contain the original english plus bracketed options;
    # we'll just translate the english portion ignoring the prefix marker if any.
    # The english is the question or explanation itself.
    return translator.translate(text, dest='ja').text


def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    changed = False
    count_q = 0
    count_e = 0
    for q in data.get('questions', []):
        # question
        jq = q.get('ja_question')
        if jq and jq.startswith('[Japanese translation needed'):
            # use q['question'] as source
            new = translate_text(q.get('question', ''))
            q['ja_question'] = new
            changed = True
            count_q += 1
        # explanation
        je = q.get('ja_explanation')
        if je and je.startswith('[Japanese translation needed'):
            new = translate_text(q.get('explanation', ''))
            q['ja_explanation'] = new
            changed = True
            count_e += 1
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return count_q, count_e


def main():
    patterns = [
        'data/english/questions_en_toeic_*.json',
        'data/english/questions_en_toefl_*.json',
    ]
    total_q = 0
    total_e = 0
    for pat in patterns:
        for fname in glob.glob(pat):
            cq, ce = process_file(fname)
            print(f"{fname}: translated {cq} questions, {ce} explanations")
            total_q += cq
            total_e += ce
    print(f"Total: {total_q} questions, {total_e} explanations translated")


if __name__ == '__main__':
    main()
