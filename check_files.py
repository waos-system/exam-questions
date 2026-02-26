#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

with open('data/genres.json', encoding='utf-8') as f:
    data = json.load(f)

missing_files = []

for subject in data['subjects']:
    for exam in subject['exams']:
        for section in exam['sections']:
            file_path = section['file']
            if not os.path.exists(file_path):
                missing_files.append({
                    'exam_name': exam['name'],
                    'exam_short': exam['short'],
                    'section_name': section['name'],
                    'section_id': section['id'],
                    'file': file_path,
                    'count': section.get('count', 'N/A')
                })

if missing_files:
    print(f"不足のファイル数: {len(missing_files)}\n")
    for item in missing_files[:20]:
        print(f"[{item['exam_short']}] {item['section_name']}")
        print(f"  ID: {item['section_id']}, Count: {item['count']}")
        print(f"  File: {item['file']}\n")
    if len(missing_files) > 20:
        print(f"... 他 {len(missing_files) - 20} 個のファイルが不足しています")
else:
    print("✓ すべてのファイルが存在します")
