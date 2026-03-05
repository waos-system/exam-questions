import json
import os

def update_toeic_listening_photo_question():
    file_path = r"c:\git\waos\exam-questions\data\english\questions_en_toeic_listening.json"

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for question in data['questions']:
        if question['id'] == 'en_toeic_listening_001':
            # Update English question
            photo_description = "In the photograph, the man is holding a phone to his ear."
            question['question'] = f"Look at the photo. {photo_description} What is the man doing?\n(A) He is reading a document\n(B) He is having a meeting\n(C) He is making a phone call\n(D) He is writing in his planner"

            # Update Japanese question
            ja_photo_description = "写真では、男性は電話を耳に当てています。"
            question['ja_question'] = f"写真を見てください。{ja_photo_description}男は何をしているのですか？\n(A) 彼は書類を読んでいます\n(B) 彼は会議中です\n(C) 彼は電話をかけています\n(D) 彼はプランナーに書いています"

            break

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    update_toeic_listening_photo_question()
    print("Updated TOEIC listening photo question with description.")