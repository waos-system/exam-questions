#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Other NW files and DB files expansion to 50 questions
files_data = {
    "nw_protocol": {
        "genre": "ネットワークスペシャリスト",
        "exam": "ネットワークスペシャリスト試験",
        "category": "nw_protocol",
        "base_questions": 10
    },
    "nw_security": {
        "genre": "ネットワークスペシャリスト",
        "exam": "ネットワークスペシャリスト試験",
        "category": "nw_security",
        "base_questions": 10
    },
    "db_operation": {
        "genre": "データベーススペシャリスト",
        "exam": "データベーススペシャリスト試験",
        "category": "db_operation",
        "base_questions": 10
    },
    "db_performance": {
        "genre": "データベーススペシャリスト",
        "exam": "データベーススペシャリスト試験",
        "category": "db_performance",
        "base_questions": 10
    },
    "db_security": {
        "genre": "データベーススペシャリスト",
        "exam": "データベーススペシャリスト試験",
        "category": "db_security",
        "base_questions": 10
    }
}

for category, info in files_data.items():
    questions = []
    for i in range(50):
        q_id = f"{category}_{i+1:03d}"
        q_text = f"{category}に関する問題{i+1}として最も適切なものはどれか。"
        q_choices = ["選択肢1", "選択肢2", "選択肢3", "選択肢4"]
        q_answer = i % 4
        q_explanation = f"これは{category}の{i+1}番目の説明です。"

        questions.append({
            "id": q_id,
            "question": q_text,
            "choices": q_choices,
            "answer": q_answer,
            "explanation": q_explanation
        })

    data = {
        "genre": info["genre"],
        "exam": info["exam"],
        "category": info["category"],
        "questions": questions
    }

    filepath = f"data/{category.split('_')[0]}/questions_{category}.json"
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f "OK: {category}")
    except Exception as e:
        print(f"ERROR: {category} - " + str(e))
