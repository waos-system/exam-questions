#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate high-quality SC exam questions based on actual exam content"""

import json

# SC Technology (セキュリティ技術) - 50 questions
sc_technology_questions = {
    "genre": "情報処理安全確保支援士試験",
    "exam": "SC",
    "category": "sc_technology",
    "questions": [
        {"id": "sc_tech_001", "question": "公開鍵基盤（PKI）における電子証明書の失効確認方法として最も一般的なのはどれか。", "choices": ["定期的にメール送信される公式リスト", "CRL（証明書失効リスト）またはOCSP（オンライン証明書状態プロトコル）", "ユーザが手動で確認する", "ファイアウォールで自動検出"], "answer": 1, "explanation": "CRLとOCSPは、電子証明書の失効状態をリアルタイムで確認するための標準的なメカニズムです。"},
        {"id": "sc_tech_002", "question": "TLS 1.3での改善点として最も重要なのは何か。", "choices": ["通信速度のみ向上", "ハンドシェイクの削減により通信遅延を短縮し、Forward Secrecyを強化", "すべての暗号スイートを廃止", "認証の廃止"], "answer": 1, "explanation": "TLS 1.3は1-RTTハンドシェイク対応とすべての接続でForward Secrecyを実装しました。"},
        {"id": "sc_tech_003", "question": "AES-GCMモード暗号化の特徴として最も正確なのはどれか。", "choices": ["認証なしの暗号化のみ", "データの暗号化と認証を同時に提供", "リアルタイム性能が劣る", "IPv6専用"], "answer": 1, "explanation": "AES-GCMは認証付き暗号化（AEAD）を提供し、データの機密性と完全性を同時に保証します。"},
        {"id": "sc_tech_004", "question": "多要素認証（MFA）の実装において、フィッシング攻撃に最も強いのはどれか。", "choices": ["SMS OTP", "メールOTP", "FIDO2セキュリティキー", "セキュリティ質問プラス動的パスワード"], "answer": 2, "explanation": "FIDO2はチャレンジ・レスポンス認証でフィッシングサイトを検出でき、最もフィッシングに耐性があります。"},
        {"id": "sc_tech_005", "question": "OAuth 2.0のAuthorizationコードフローについて、最も重要なセキュリティ対策は何か。", "choices": ["コードの長期有効性", "コードの短期有効性とPKCE（Proof Key for Code Exchange）の使用", "コードのクライアント側保存", "HTTPS不要"], "answer": 1, "explanation": "コードは数分の短期有効性を持ち、PKCEでコード横取り攻撃を防止します。"},
        {"id": "sc_tech_006", "question": "Zero Trust Architectureにおける基本原則として最も適切なのはどれか。", "choices": ["社内ネットワークは無条件に信頼", "すべてのアクセスを検証・暗号化・最小権限で制御", "外部のみ警戒", "一度認証されたら信頼"], "answer": 1, "explanation": "Zero Trustは内部・外部を区別せず、すべてのアクセスを常に検証する設計原則です。"},
        {"id": "sc_tech_007", "question": "ネットワークセグメンテーション（マイクロセグメンテーション）の主な効果はどれか。", "choices": ["ネットワーク速度向上のみ", "横展開攻撃の抑止・リスク局所化・侵害の影響を最小化", "コスト削減のみ", "ユーザ利便性向上"], "answer": 1, "explanation": "マイクロセグメンテーションは侵害範囲を限定し、攻撃者の横展開を制限する効果的な防御戦略です。"},
        {"id": "sc_tech_008", "question": "データ分類（Data Classification）における最高機密レベルの情報として最も該当するのはどれか。", "choices": ["公開Webサイトコンテンツ", "内部組織図", "経営戦略・財務情報・個人情報・知的財産権", "一般的なIT手順書"], "answer": 2, "explanation": "最高機密レベルは特別な保護が必要な、重要なビジネス資産と規制対象データです。"},
        {"id": "sc_tech_009", "question": "エンドポイント保護（Endpoint Protection）の最新トレンドとして最も重要なのは何か。", "choices": ["ウイルススキャンのみ", "EDR（Endpoint Detection and Response）による行動分析と自動対応", "ファイアウォール設置のみ", "OSアップデート"], "answer": 1, "explanation": "EDRは単なる検知にとどまらず、疑わしい行動をリアルタイムで分析し自動対応します。"},
        {"id": "sc_tech_010", "question": "API セキュリティにおいて、認証と認可の区別として最も正確なのはどれか。", "choices": ["両者は同じ概念である", "認証は本人確認、認可はアクセス権限の確認", "認証のみが重要である", "APIs は認証不要"], "answer": 1, "explanation": "認証（Authentication）は「あなたは誰か」、認可（Authorization）は「何ができるか」を判定します。"},
        {"id": "sc_tech_011", "question": "DNSSEC（DNS Security Extensions）の主な目的は何か。", "choices": ["DNS応答速度の向上", "DNS応答の真正性・完全性を保証・DNS キャッシュポイズニング攻撃防止", "インターネット遅延の改善", "ユーザのプライバシー保護のみ"], "answer": 1, "explanation": "DNSSECはデジタル署名によりDNS応答の正当性を保証し、DNS偽造攻撃を防止します。"},
        {"id": "sc_tech_012", "question": "Web Application Firewall（WAF）の主要機能として最も適切なのはどれか。", "choices": ["ネットワークレベルのすべてのパケット検査", "SQLインジェクション・XSS・CSRF等のWebアプリ攻撃検知・遮断", "OS レベルのシステムコール監視", "バックアップ管理"], "answer": 1, "explanation": "WAFはアプリケーションレイヤーで動作し、一般的なWeb攻撃パターンを検知・ブロックします。"},
        {"id": "sc_tech_013", "question": "クラウドストレージでの顧客管理暗号化キー（CMEK）使用の最大利点は何か。", "choices": ["费用削減", "クラウドプロバイダーがデータにアクセス不可・顧客が完全な制御権を保持", "パフォーマンス向上", "設定の簡素化"], "answer": 1, "explanation": "CMEK使用により、たとえクラウドプロバイダーでも顧客データを復号できず、完全な暗号化が保証されます。"},
        {"id": "sc_tech_014", "question": "ハードウェアセキュリティモジュール（HSM）の主な用途として最も重要なのは何か。", "choices": ["ネットワークスイッチの管理", "秘密鍵の安全な保管と暗号操作の実行", "ユーザのグラフィカルインターフェース管理", "メール送信のみ"], "answer": 1, "explanation": "HSMは秘密鍵がシステム外に出ない専用ハードウェアで、暗号操作の最高レベルのセキュリティを提供します。"},
        {"id": "sc_tech_015", "question": "Secure Boot の主な機能として最も正確なのはどれか。", "choices": ["OS起動速度の向上", "改ざんされたブートローダーの読み込み防止・起動前の整合性検証", "アプリケーション実行の高速化", "ユーザのパスワード生成"], "answer": 1, "explanation": "Secure Bootは起動時にファームウェア・ブートローダーのデジタル署名を検証し、改ざんを検出します。"},
        {"id": "sc_tech_016", "question": "Container イメージスキャンの目的として最も重要なのは何か。", "choices": ["コンテナの実行速度測定", "既知の脆弱性を含むライブラリ・依存関係の検出", "ディスク領域の最適化", "ユーザインターフェース改善"], "answer": 1, "explanation": "イメージスキャンはコンテナに含まれるベースイメージやライブラリの既知脆弱性を検出し、デプロイ前に対処します。"},
        {"id": "sc_tech_017", "question": "Service Mesh（istio等）の主な役割として最も適切なのは何か。", "choices": ["CPU負荷の軽減", "マイクロサービス間通信の暗号化・トラフィック管理・可視化", "ストレージの自動拡張", "デスクトップUI の統一"], "answer": 1, "explanation": "Service Meshはマイクロサービス間の通信（East-West Traffic）を安全に管理・監視します。"},
        {"id": "sc_tech_018", "question": "Post-Quantum Cryptography への移行が必要な理由は何か。", "choices": ["現在のRSAが効率的でない", "将来の量子コンピュータによるRSA・ECC の破られるリスク対策", "クラウド速度向上", "リモートワーク対応"], "answer": 1, "explanation": "量子コンピュータは現在の公開鍵暗号を破ることが理論的に知られているため、耐性の高い暗号への移行が必要です。"},
        {"id": "sc_tech_019", "question": "DLP（Data Loss Prevention）ソリューションの主要機能は何か。", "choices": ["ネットワーク速度向上", "機密データの無許可送信検知・遮断・監査ログ記録", "ユーザのパスワード管理", "バックアップ自動化"], "answer": 1, "explanation": "DLPは機密データが組織外に流出するのを防ぎ、検知・遮断・監査を行う総合的なソリューションです。"},
        {"id": "sc_tech_020", "question": "Threat Intelligence 共有の効果として最も重要なのは何か。", "choices": ["脅威情報の独占", "業界全体での攻撃パターン・IoC（Indicators of Compromise）の共有・集団防御強化", "競合企業への情報開示のみ", "セキュリティチームの縮小"], "answer": 1, "explanation": "脅威インテリジェンスを共有することで、業界全体で最新の脅威に対する防御を強化できます。"},
        {"id": "sc_tech_021", "question": "Cyber Kill Chain 分析の学習目的として最も適切なのは何か。", "choices": ["攻撃を完全に防止できる", "攻撃の各段階を理解・各段階での対抗措置を設計", "ネットワーク速度向上", "ユーザのパスワード変更"], "answer": 1, "explanation": "Kill Chain分析により、RECONからEXFILまで各段階を理解し、防御・検知・対応の戦略を構築します。"},
        {"id": "sc_tech_022", "question": "Privilege Access Management（PAM）の主な目標は何か。", "choices": ["すべてのユーザに管理者権限付与", "特権アカウントの使用を制御・監査・最小権限実行を確保", "セキュリティチーム廃止", "監査ログ削除"], "answer": 1, "explanation": "PAMは最も重要な特権アカウント（管理者）の使用を厳密に制御し、不正利用を防止します。"},
        {"id": "sc_tech_023", "question": "Behavioral Analysis（行動分析）による脅威検知の利点は何か。", "choices": ["既知脅威処理のみ", "未知の異常な行動パターンを検出・ゼロデイ攻撃や内部脅威を発見", "定義済みシグネチャのマッチングのみ", "実施が簡単"], "answer": 1, "explanation": "行動分析は既知のシグネチャにない異常な活動を検出し、未知の脅威検知が可能です。"},
        {"id": "sc_tech_024", "question": "SIEM（Security Information and Event Management）の中核機能として最も重要なのは何か。", "choices": ["ユーザのパスワード自動生成", "複数ツールのログ集約・相関分析・セキュリティイベント検知", "アプリケーション開発のみ", "ファイル転送速度"], "answer": 1, "explanation": "SIEMは複数セキュリティツールからのログを集約・分析し、複雑な攻撃パターンを検знید."},
        {"id": "sc_tech_025", "question": "Deception Technology（ハニーポット・ハニートークン）の使用効果は何か。", "choices": ["本番システムのセキュリティ向上のみ", "攻撃者の存在と行動パターンを検出・本番システムへの侵害の早期警告", "ネットワーク速度向上", "ユーザ利便性向上"], "answer": 1, "explanation": "デセプション技術は偽の価値あるリソースを配置し、攻撃者の侵入を即座に検知します。"},
        {"id": "sc_tech_026", "question": "Software Composition Analysis（SCA）ツールの主な機能は何か。", "choices": ["ソースコード記述の美学検証", "オープンソースライブラリの脆弱性・ライセンス問題の検出", "UI デザイン評価", "ユーザマニュアル作成"], "answer": 1, "explanation": "SCAはオープンソース依存関係をスキャンし、既知脆弱性やライセンス違反を検出します。"},
        {"id": "sc_tech_027", "question": "IoT セキュリティの課題として最も深刻なのは何か。", "choices": ["デバイス販売数の増加", "計算能力・メモリの制限・従来のセキュリティ対策実装の困難さ", "ユーザインターフェースの複雑性", "通信速度"], "answer": 1, "explanation": "IoTデバイスは計算能力・メモリが限定的なため、複雑なセキュリティ対策が実装しにくい課題があります。"},
        {"id": "sc_tech_028", "question": "Industrial Control Systems（ICS）攻撃への対策として最も重要なのは何か。", "choices": ["一般的なアンチウイルス導入のみ", "エアギャップ・冗長性・可用性の確保・物理的セキュリティ", "Windowsアップデーターのみ", "セキュリティ対策なし"], "answer": 1, "explanation": "ICS攻撃は物理的危害をもたらすため、エアギャップ・冗長システム・多層防御が必須です。"},
        {"id": "sc_tech_029", "question": "Supply Chain Attack 対策として最も効果的なのは何か。", "choices": ["ベンダーを無制限に信頼", "ベンダーセキュリティ評価・契約義務・定期監査・セキュアな開発実践", "セキュリティ投資なし", "すべてをオンプレミス化"], "answer": 1, "explanation": "サプライチェーン攻撃防止には、ベンダーのセキュリティ管理と継続的な監視が必須です。"},
        {"id": "sc_tech_030", "question": "攻撃面管理（Attack Surface Management）の主な目的は何か。", "choices": ["攻撃者の採用", "組織の公開リソース・脆弱性・設定誤りの継続的検出・可視化", "セキュリティ予算削減", "攻撃完全防止"], "answer": 1, "explanation": "攻撃面管理は外部攻撃者視点で、組織が暴露したすべてのリスク要因を持続的に発見・評価します。"}
    ]
}

# Continue adding questions...
with open('data/sc/questions_sc_technology.json', 'w', encoding='utf-8') as f:
    json.dump(sc_technology_questions, f, ensure_ascii=False, indent=2)
    print('✓ questions_sc_technology.json: 30問更新（残り20問は別途処理）')

print("\n=== SC試験問題の質的改善開始 ===")
