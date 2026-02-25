#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

nw_operation = {
    "genre": "ネットワークスペシャリスト",
    "exam": "ネットワークスペシャリスト試験",
    "category": "nw_operation",
    "questions": [
        {"id": "nw_operation_001", "question": "ネットワーク監視における重要なメトリクスとして最も適切なものはどれか。", "choices": ["任意の値", "トラフィック量、レイテンシ、パケットロス率、リンク利用率"], "answer": 1, "explanation": "ネットワーク監視：帯域利用率・パケットロス・遅延・エラー率をKPIに設定。閾値超過で自動アラート。"},
        {"id": "nw_operation_002", "question": "SNMP（Simple Network Management Protocol）の主な目的として最も適切なものはどれか。", "choices": ["ルーティングプロトコル", "ネットワークデバイスの監視・管理、統計情報収集"], "answer": 1, "explanation": "SNMP：ネットワークデバイス（ルータ・スイッチ）の状態監視、パフォーマンス情報取得。v3で認証・暗号化。"},
        {"id": "nw_operation_003", "question": "NetFlow/sFlow の主な用途として最も適切なものはどれか。", "choices": ["リアルタイム制御", "トラフィックフローの詳細分析、アプリケーション識別、使用量把握"], "answer": 1, "explanation": "NetFlow：ネットワークフロー情報を収集・分析。送信元・宛先・ポート・プロトコル等から通信パターン把握。"},
        {"id": "nw_operation_004", "question": "帯域幅管理（Bandwidth Management）の主な目的として最も適切なものはどれか。", "choices": ["全トラフィック等速", "トラフィック優先度付け・制限、ネットワーク効率化、QoS確保"], "answer": 1, "explanation": "帯域幅管理：優先度に基づき帯域配分。ベストエフォート・保証帯域設定で、重要通信確保。"},
        {"id": "nw_operation_005", "question": "トラフィックシェーピング（Traffic Shaping）の役割として最も適切なものはどれか。", "choices": ["トラフィック破棄", "トラフィック流量制御、バースト削減、WAN回線最適化"], "answer": 1, "explanation": "トラフィックシェーピング：バッファリング・遅延によりトラフィック平準化。WAN最適化。"},
        {"id": "nw_operation_006", "question": "ネットワークトラブルシューティングの基本的なアプローチとして最も適切なものはどれか。", "choices": ["ランダムな推測", "OSIモデル層別分析、計画的な絞込み、再現可能性確認"], "answer": 1, "explanation": "トラブルシューティング：物理層→データリンク層…と段階的に診断。ping・tracert・tcpdump等ツール活用。"},
        {"id": "nw_operation_007", "question": "ネットワークドキュメンテーションが重要である理由として最も適切なものはどれか。", "choices": ["不要", "構成把握、変更管理、障害対応迅速化、知識共有"], "answer": 1, "explanation": "ネットワーク図、IP管理表、ルーティング設定の文書化。障害時の原因特定・復旧加速。"},
        {"id": "nw_operation_008", "question": "変更管理（Change Management）プロセスが必須とされる理由として最も適切なものはどれか。", "choices": ["不要", "計画的な変更、テスト・検証、影響分析、ロールバック準備"], "answer": 1, "explanation": "変更管理：計画→テスト→承認→実施→検証。予期しない障害防止。"},
        {"id": "nw_operation_009", "question": "構成管理（Configuration Management）の主な目的として最も適切なものはどれか。", "choices": ["記録不要", "デバイス設定の正確性確認、バージョン管理、バックアップ"], "answer": 1, "explanation": "構成管理：すべてのネットワークデバイスの設定を中央管理・バージョン管理。障害時復旧容易化。"},
        {"id": "nw_operation_010", "question": "インシデント対応計画（Incident Response Plan）に含めるべき要素として最も適切なものはどれか。", "choices": ["対応不要", "検知・報告・対応・復旧・事後分析・改善の流れ"], "answer": 1, "explanation": "インシデント対応計画：検知→クライアント通知→対応チーム召集→復旧→検証→事後レビュー。MTTR最小化。"}
    ]
}

try:
    with open(r"C:\git\waos\exam-questions\data\nw\questions_nw_operation.json", 'w', encoding='utf-8') as f:
        json.dump(nw_operation, f, ensure_ascii=False, indent=2)
    print("OK: nw_operation")
except Exception as e:
    print("ERROR: nw_operation - " + str(e))
