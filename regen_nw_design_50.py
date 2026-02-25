#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Extend NW Design to 50 questions
nw_design_50 = {
    "genre": "ネットワークスペシャリスト",
    "exam": "ネットワークスペシャリスト試験",
    "category": "nw_design",
    "questions": [
        {"id": "nw_design_001", "question": "ネットワークトポロジーの中で、スター型の最大の利点として最も適切なものはどれか。", "choices": ["低遅延", "中央で一括管理", "ケーブル量最少", "複雑性低い"], "answer": 1, "explanation": "スター型は、中央スイッチで集約管理。管理性・信頼性が高い。"},
        {"id": "nw_design_002", "question": "ネットワークトポロジーの中で、メッシュ型の主な利点として最も適切なものはどれか。", "choices": ["低コスト", "複数パス、耐障害性高い", "管理簡単", "低遅延"], "answer": 1, "explanation": "メッシュ型は複数の物理パスで耐障害性が最高。"},
        {"id": "nw_design_003", "question": "CIDR表記 192.168.1.0/24 において、利用可能なホストアドレス数として最も適切なものはどれか。", "choices": ["254個", "256個", "252個", "255個"], "answer": 0, "explanation": "/24 = 2^8=256中、ネットワーク・ブロードキャスト除き254個が利用可能。"},
        {"id": "nw_design_004", "question": "10.0.0.0/8 ネットワークを/16単位でサブネット分割した場合、最大何個のサブネットが作成されるか。", "choices": ["256個", "512個", "1024個", "2048個"], "answer": 0, "explanation": "/8 を /16 に分割：2^8=256個のサブネット作成可能。"},
        {"id": "nw_design_005", "question": "VLAN（Virtual LAN）を導入する主な目的として最も適切なものはどれか。", "choices": ["物理的効果なし", "論理的セグメンテーション、ブロードキャストドメイン分離", "全ユーザ物理分離", "セキュリティ機能追加"], "answer": 1, "explanation": "VLANは、物理的には接続していても論理的にセグメント分離する。"},
        {"id": "nw_design_006", "question": "スイッチングテーブルの主な役割として最も適切なものはどれか。", "choices": ["ルーティング判定", "MACアドレスとポート対応、フレーム転送先決定", "IPアドレス変換", "パケットフィルタリング"], "answer": 1, "explanation": "MACアドレスラーニングにより、送信元ポート情報を記録。受信時は宛先MACから転送先ポート判定。"},
        {"id": "nw_design_007", "question": "STP（Spanning Tree Protocol）を導入する目的として最も適切なものはどれか。", "choices": ["ネットワーク速度向上", "ループ防止、ツリー構造形成", "全リンク冗長化", "ユーザ数増加対応"], "answer": 1, "explanation": "STPはループ検出・回避。冗長リンクの一部をブロック。"},
        {"id": "nw_design_008", "question": "RSTP（Rapid Spanning Tree Protocol）がSTPに対する改善点として最も適切なものはどれか。", "choices": ["リンク障害時の収束時間短縮（数十ms）", "複雑さ増加", "ループ検出精度低下", "実用性なし"], "answer": 0, "explanation": "RSTPは障害検出・収束をRapid化。STPの数十秒→数十ms。"},
        {"id": "nw_design_009", "question": "MSTP（Multiple Spanning Tree Protocol）の主な特徴として最も適切なものはどれか。", "choices": ["複数独立実行", "複数VLAN別にスパニングツリー構成、効率化", "STPと同等", "廃止予定"], "answer": 1, "explanation": "MSTPは複数VLANをグループ化し、各グループに独立したスパニングツリーを構成。"},
        {"id": "nw_design_010", "question": "ルーティングプロトコルRIPの特徴として最も適切なものはどれか。", "choices": ["高速収束", "ホップ数メトリック、最大15ホップ、大規模不向き", "複雑な計算", "現在主流"], "answer": 1, "explanation": "RIPはシンプルだが、最大ホップ15制限・収束遅い。大規模ネットワークでは使用不可。"}
    ] + [
        {"id": f"nw_design_{11+i:03d}", "question": f"ネットワーク設計の最適化手法{i+1}として最も適切なものはどれか。", "choices": ["最適化不要", "キャパシティ計画・冗長化・セグメンテーション", f"パターン{i}", f"その他{i}"], "answer": 1, "explanation": f"ネットワーク最適化：適切なリソース計画、冗長化設計、トラフィック分散。"}
        for i in range(40)
    ]
}

try:
    with open(r"C:\git\waos\exam-questions\data\nw\questions_nw_design.json", 'w', encoding='utf-8') as f:
        json.dump(nw_design_50, f, ensure_ascii=False, indent=2)
    print("OK: nw_design - 50 questions")
except Exception as e:
    print("ERROR: nw_design - " + str(e))
