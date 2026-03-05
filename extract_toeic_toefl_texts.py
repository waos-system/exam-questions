"""
Extract all unique questions and explanations from TOEIC/TOEFL JSON files
to prepare them for translation.
"""

import json
import glob
from collections import defaultdict

def extract_texts(patterns):
    """Extract all questions and explanations from files."""
    questions = defaultdict(list)
    explanations = defaultdict(list)
    
    for pat in patterns:
        for fname in sorted(glob.glob(pat)):
            with open(fname, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for q in data.get('questions', []):
                question_text = q.get('question', '')
                explanation_text = q.get('explanation', '')
                
                questions[question_text].append(fname)
                explanations[explanation_text].append(fname)
    
    return questions, explanations


def main():
    patterns = [
        'data/english/questions_en_toeic_*.json',
        'data/english/questions_en_toefl_*.json',
    ]
    
    questions, explanations = extract_texts(patterns)
    
    print(f"Unique questions: {len(questions)}")
    print(f"Unique explanations: {len(explanations)}")
    
    # Sample of questions
    print("\n--- Sample Questions (first 20) ---")
    for i, q in enumerate(list(questions.keys())[:20]):
        print(f"{i+1}. {q[:80]} ...")


if __name__ == '__main__':
    main()
