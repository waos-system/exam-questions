#!/usr/bin/env python3
import json

with open('data/genres.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
for subject in data.get('subjects', []):
    for exam in subject.get('exams', []):
        if '安全' in exam.get('name', '') or 'SC' in exam.get('short', '') or 'SA' in exam.get('short', ''):
            print(f"Exam: {exam.get('id')} = {exam.get('name')}")
            for section in exam.get('sections', []):
                print(f"  Section: {section.get('id')} = {section.get('name')}")
                print(f"    File: {section.get('file')}")
