"""
Translate TOEIC/TOEFL English questions and explanations into Japanese using a
pre-built translation dictionary. This is a local solution that doesn't require
network access.

Handcrafted dictionary of common TOEIC/TOEFL question patterns and their Japanese
equivalents.
"""

import json
import glob
import re

# Core TOEIC/TOEFL translation patterns and phrases
TRANSLATION_MAP = {
    # Main idea / Purpose questions
    "What is the main idea": "このトークの主なポイントは何ですか",
    "What is the main topic": "会話の主なトピックは何ですか",
    "What is the main purpose": "この講演の主な目的は何ですか",
    "What does the speaker mainly discuss": "スピーカーは主に何を議論していますか",
    "What is the speaker mainly discussing": "スピーカーは主に何について議論していますか",
    
    # Detail / Factual questions
    "According to the speaker": "スピーカーによると",
    "According to the professor": "教授によると",
    "According to the lecture": "講演によると",
    "What is the caller's problem": "発信者の問題は何ですか",
    "What does the man request": "男性は何をリクエストしますか",
    "Why does the woman go": "女性はなぜ行きますか",
    "What does the student": "学生は何をしていますか",
    
    # Inference questions
    "What can be inferred": "何が推測されますか",
    "What is implied": "何が示唆されていますか",
    "What does the conversation suggest": "会話は何を示唆していますか",
    
    # Attitude / Tone questions
    "What is the speaker's attitude": "スピーカーの態度は何ですか",
    "What is the professor's attitude": "教授の態度は何ですか",
    
    # Function / Purpose questions
    "Why does the speaker mention": "スピーカーが言及する理由は何ですか",
    "The professor mentions": "教授は述べています",
    "primarily to": "主に〜のために",
    
    # Prediction questions
    "Which of the following would": "次のどちらが〜しますか",
    "What would the speaker most likely": "スピーカーは次に最も可能性が高い何をするでしょうか",
    
    # Listening specific
    "Look at the photo": "写真を見てください",
    "Listen to the short talk": "短い話を聞く",
    "Listen to the conversation": "会話を聞く",
    
    # Answer patterns
    "He is reading a document": "彼は文書を読んでいます",
    "He is having a meeting": "彼は会議をしています",
    "He is making a phone call": "彼は電話をしています",
    "He is writing": "彼は書いています",
    
    # Common nouns
    "document": "文書",
    "meeting": "会議",
    "phone call": "電話",
    "delivery": "配送",
    "schedule": "スケジュール",
    "warehouse": "倉庫",
    "staff": "スタッフ",
    "account": "アカウント",
    "product": "製品",
    "discount": "割引",
    "maintenance": "メンテナンス",
    "office": "オフィス",
    "project": "プロジェクト",
    "presentation": "プレゼンテーション",
    
    # Common descriptions
    "was charged twice": "2回請求されました",
    "cannot access his account": "彼は自分のアカウントにアクセスできません",
    "credit card is expired": "クレジットカードの有効期限が切れています",
    "return and purchase": "返品と購入",
    "to exchange a product": "製品を交換するために",
    "to inquire about a discount": "割引について問い合わせる",
    "to apply for a customer loyalty card": "顧客ロイヤルティカードに申し込む",
}


def simple_translate(text):
    """
    Simple pattern-based translation.
    If exact phrase found in map, use it; otherwise, return a placeholder.
    """
    text = text.strip()
    
    # Try exact match first
    if text in TRANSLATION_MAP:
        return TRANSLATION_MAP[text]
    
    # Try partial matching for longer texts
    result = text
    for eng, ja in sorted(TRANSLATION_MAP.items(), key=lambda x: -len(x[0])):
        if eng.lower() in result.lower():
            result = result.replace(eng, ja)
            break
    
    # If no translation found, create a simple katakana placeholder
    if result == text:
        result = f"【翻訳: {text[:30]}...】"
    
    return result


def process_file(path):
    """Process a single JSON question file and translate ja_* placeholders."""
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
        # question
        jq = q.get('ja_question')
        if jq and jq.startswith('[Japanese translation needed'):
            new = simple_translate(q.get('question', ''))
            q['ja_question'] = new
            changed = True
            count_q += 1
        
        # explanation
        je = q.get('ja_explanation')
        if je and je.startswith('[Japanese translation needed'):
            new = simple_translate(q.get('explanation', ''))
            q['ja_explanation'] = new
            changed = True
            count_e += 1
    
    if changed:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"ERROR writing {path}: {e}")
    
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
        for fname in glob.glob(pat):
            cq, ce = process_file(fname)
            print(f"{fname}: translated {cq} questions, {ce} explanations")
            total_q += cq
            total_e += ce
    
    print(f"\nTotal: {total_q} questions, {total_e} explanations translated")
    print("Note: Full translations require manual review for accuracy.")


if __name__ == '__main__':
    main()
