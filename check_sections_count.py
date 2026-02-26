#!/usr/bin/env python3
"""Check all sections and their question counts"""

import json
import os
from pathlib import Path

# Load genres.json
with open('data/genres.json', 'r', encoding='utf-8') as f:
    genres = json.load(f)

# Collect sections with less than 50 questions
sections_to_augment = []

for subject in genres.get('subjects', []):
    subject_name = subject.get('name', 'Unknown')
    
    for exam in subject.get('exams', []):
        exam_name = exam.get('name', 'Unknown')
        exam_id = exam.get('id', 'unknown')
        
        for section in exam.get('sections', []):
            section_name = section.get('name', 'Unknown')
            section_id = section.get('id', 'unknown')
            file_path = section.get('file', '')
            expected_count = section.get('count', 0)
            
            # Check if file exists and count questions
            if file_path and os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        actual_count = len(data.get('questions', []))
                        
                        if actual_count < 50:
                            sections_to_augment.append({
                                'exam': exam_name,
                                'exam_id': exam_id,
                                'section': section_name,
                                'section_id': section_id,
                                'file': file_path,
                                'current_count': actual_count,
                                'needed_count': 50 - actual_count,
                                'expected_count': expected_count
                            })
                            
                            print(f"✓ {exam_name} > {section_name}: {actual_count}問 (目標: 50, 必要: {50-actual_count})")
                        
                except Exception as e:
                    print(f"✗ {exam_name} > {section_name}: エラー - {str(e)}")
            else:
                print(f"✗ {exam_name} > {section_name}: ファイルが見つかりません - {file_path}")

print(f"\n=== 要追加セクション: {len(sections_to_augment)} ===")
for info in sections_to_augment:
    print(f"{info['exam']} > {info['section']}: {info['needed_count']}問必要")

# Save to JSON for later use
with open('sections_to_augment.json', 'w', encoding='utf-8') as f:
    json.dump(sections_to_augment, f, ensure_ascii=False, indent=2)
