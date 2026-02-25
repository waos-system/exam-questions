#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

# Generate sample questions for all sections
def generate_questions(count, prefix, baseid):
    """Generate placeholder questions"""
    questions = []
    for i in range(1, count + 1):
        q_id = f"{prefix}_{i:03d}"
        questions.append({
            "id": q_id,
            "question": f"IPA {prefix.upper()} 試験問題 {i}",
            "choices": [
                f"選択肢A - {q_id}",
                f"選択肢B - {q_id}",
                f"選択肢C - {q_id}",
                f"選択肢D - {q_id}"
            ],
            "answer": i % 4,
            "explanation": f"これは {q_id} の説明です。"
        })
    return questions

# Network Design questions
nw_design_questions = [
    {
        "id": "nw_design_001",
        "question": "エンタープライズネットワークの設計において、階層型モデルを採用する主な目的として最も適切なものはどれか。",
        "choices": [
            "スケーラビリティ、障害分離、管理性の向上",
            "ネットワーク遅延の完全な排除",
            "すべての機器で統一されたプロトコルの使用",
            "冗長性を排除して運用効率を向上させる"
        ],
        "answer": 0,
        "explanation": "階層型モデルはスケーラビリティ、障害分離、各層での設定の統一による管理性向上が利点である。"
    },
    {
        "id": "nw_design_002",
        "question": "メッシュネットワークトポロジーの特徴として最も適切なものはどれか。",
        "choices": [
            "構成が単純でコストが低い",
            "多数のリンクが冗長化され、高い可用性を提供する",
            "ネットワークの拡張時に既存機器の変更が必要ない",
            "単一障害点を排除できない"
        ],
        "answer": 1,
        "explanation": "メッシュトポロジーは複数のリンクで冗長化されており、ある経路が故障しても別の経路で通信可能で高い可用性を実現する。"
    },
    {
        "id": "nw_design_003",
        "question": "キャンパスネットワークにおいて、複数の建物間を接続する際の最適な方式として最も適切なものはどれか。",
        "choices": [
            "各建物間を直接イーサネットケーブルで接続",
            "光ファイバーケーブルの使用",
            "無線LANのみを利用した接続",
            "アナログ通信回線による接続"
        ],
        "answer": 1,
        "explanation": "建物間の長距離接続には光ファイバーケーブルが電磁干渉への耐性、広帯域幅、長距離伝送特性により最適である。"
    },
    {
        "id": "nw_design_004",
        "question": "WANの設計において、MPLS技術を導入する主な利点として最も適切なものはどれか。",
        "choices": [
            "ネットワークの総コストを50パーセント以上削減できる",
            "QoS制御、トラフィック・エンジニアリング、VPN機能の統合",
            "BGPルーティングを完全に置き換える",
            "すべてのパケットのセキュリティを暗号化する"
        ],
        "answer": 1,
        "explanation": "MPLSはQoS制御、トラフィック・エンジニアリング、VPN構築など複数の機能を効率的に実装できる。"
    },
    {
        "id": "nw_design_005",
        "question": "アクセスネットワークの設計において、802.11acと802.11axの主な相違点として適切でないものはどれか。",
        "choices": [
            "802.11axは5GHz帯に加えて6GHz帯を利用できる",
            "802.11axはOFDMA技術により複数デバイスの同時利用が効率化される",
            "802.11acは2.4GHz帯のみで動作する",
            "802.11axはMU-MIMOとDL-OFDMAにより高スループットを実現"
        ],
        "answer": 2,
        "explanation": "802.11acは5GHz帯で動作し、802.11axも主に5GHz帯で動作する。802.11acは2.4GHz帯では動作しない。"
    },
]

# Add remaining design questions
for i in range(6, 51):
    nw_design_questions.append({
        "id": f"nw_design_{i:03d}",
        "question": f"ネットワーク設計に関する質問{i}",
        "choices": [
            f"選択肢A",
            f"選択肢B",
            f"選択肢C",
            f"選択肢D"
        ],
        "answer": i % 4,
        "explanation": f"これは質問{i}の説明です。"
    })

# Network Protocol questions
nw_protocol_questions = [
    {
        "id": "nw_protocol_001",
        "question": "TCPの3ウェイハンドシェイクにおいて、SYNフラッド攻撃に対する効果的な防御方法として最も適切なものはどれか。",
        "choices": [
            "すべてのICMPパケットをフィルタリング",
            "SYN Cookieの仕組みを採用したファイアウォール",
            "TCP接続数の制限なし",
            "すべてのポート80トラフィックの遮断"
        ],
        "answer": 1,
        "explanation": "SYN Cookieはサーバー側で状態を保持しない方式で、不完全な接続テーブルのオーバーフローを防止する。"
    },
    {
        "id": "nw_protocol_002",
        "question": "BGPの属性のうち、ローカルプリファレンスの主な役割として最も適切なものはどれか。",
        "choices": [
            "隣接ASへの経路広告範囲を制限する",
            "自AS内で複数の外部経路がある場合の優先度を制御",
            "ネットワークのホップ数を最小化する",
            "受信したASパスをすべて無視する"
        ],
        "answer": 1,
        "explanation": "ローカルプリファレンスは自AS内で複数の外部経路が存在する場合に、どの経路を優先するかを制御する。"
    },
    {
        "id": "nw_protocol_003",
        "question": "IPv6のアドレス種類のうち、最も適切でない説明はどれか。",
        "choices": [
            "ユニキャストアドレス: 単一のインターフェイスに割り当てられる",
            "マルチキャストアドレス: 複数のインターフェイスのグループに送信",
            "エニキャストアドレス: 複数のユニキャストアドレスと同一",
            "ブロードキャストアドレス: IPv6でネイティブに定義されている"
        ],
        "answer": 3,
        "explanation": "IPv6ではブロードキャストアドレスが定義されておらず、その役割はマルチキャストで実装されている。"
    },
    {
        "id": "nw_protocol_004",
        "question": "DHCPリレーエージェントの主な機能として最も適切なものはどれか。",
        "choices": [
            "DHCPサーバーの負荷分散を行う",
            "異なるサブネット間でDHCPリクエストを中継する",
            "クライアントのIPアドレスをランダムに生成",
            "DHCPサーバーの障害時に自動フェイルオーバーを行う"
        ],
        "answer": 1,
        "explanation": "DHCPリレーエージェントはDHCPクライアントとサーバーが異なるサブネットにある場合、クライアントのブロードキャストリクエストをサーバーに中継する。"
    },
    {
        "id": "nw_protocol_005",
        "question": "IGMPの役割として最も適切なものはどれか。",
        "choices": [
            "ホストとルータ間のマルチキャストグループメンバーシップ管理",
            "ユニキャストパケットのルーティングプロトコル",
            "異なるネットワークセグメント間のブリッジング",
            "DNSリゾルバーとDNSサーバー間の通信"
        ],
        "answer": 0,
        "explanation": "IGMPはホストがマルチキャストグループへの参加と脱退をルータに通知し、ルータがマルチキャストフォワーディングを管理する。"
    },
]

# Add remaining protocol questions
for i in range(6, 51):
    nw_protocol_questions.append({
        "id": f"nw_protocol_{i:03d}",
        "question": f"ネットワークプロトコルに関する質問{i}",
        "choices": [f"選択肢A", f"選択肢B", f"選択肢C", f"選択肢D"],
        "answer": i % 4,
        "explanation": f"これは質問{i}の説明です。"
    })

# Network Security questions
nw_security_questions = [
    {
        "id": "nw_security_001",
        "question": "IPsecのトランスポートモードとトンネルモードの主な相違として最も適切なものはどれか。",
        "choices": [
            "トランスポートモードはIPヘッダを含むペイロード全体を暗号化",
            "トンネルモードはエンドホスト間で使用され、トランスポートモードはゲートウェイ間で使用される",
            "トンネルモードは新しいIPヘッダを付加してカプセル化した上で暗号化",
            "トランスポートモードは機密性のみ、トンネルモードは完全性も提供"
        ],
        "answer": 2,
        "explanation": "トンネルモードは元のパケット全体をカプセル化して新しいIPヘッダを付加し、その結果を暗号化する。"
    },
    {
        "id": "nw_security_002",
        "question": "TLS 1.3における改善点として最も適切でないものはどれか。",
        "choices": [
            "0-RTTによる高速ハンドシェイク",
            "すべての暗号スイートでPerfect Forward Secrecy対応化",
            "古い暗号アルゴリズムの全廃止",
            "セッション再開機構の完全削除"
        ],
        "answer": 3,
        "explanation": "TLS 1.3でもセッション再開機構は存在し、PSKを使用した再開メカニズムが定義されている。"
    },
    {
        "id": "nw_security_003",
        "question": "PKIにおけるCAの職責として最も適切でないものはどれか。",
        "choices": [
            "申請者の認証と証明書発行",
            "証明書の失効管理",
            "暗号キーペアの生成と秘密鍵の保管管理",
            "タイムスタンプサービスの提供"
        ],
        "answer": 2,
        "explanation": "秘密鍵はエンドエンティティが安全に生成・保管するべきで、CAが生成・保管することは信頼性を損なう。"
    },
    {
        "id": "nw_security_004",
        "question": "VPN環境におけるスプリットトンネリングの主なセキュリティリスクとして最も適切でないものはどれか。",
        "choices": [
            "ローカルネットワークへのマルウェア侵入経路の形成",
            "企業ネットワークとインターネット間のトラフィック分散による負荷軽減",
            "ISPレベルのMITM攻撃によるローカルトラフィックの盗聴",
            "ローカルマシンから企業システムへの直接アクセス可能化"
        ],
        "answer": 1,
        "explanation": "スプリットトンネリングは負荷分散効果があるが、セキュリティリスクが大きいため通常は禁止される。"
    },
    {
        "id": "nw_security_005",
        "question": "Kerberos認証における、チケットの主な役割として最も適切なものはどれか。",
        "choices": [
            "ユーザーの身元確認を行うためのパスワード",
            "クライアント側でネットワークリソースへのアクセスを証明する",
            "サーバー側で複数ユーザーの識別情報を記録",
            "マルチキャストグループへの参加権を管理"
        ],
        "answer": 1,
        "explanation": "Kerberosチケットは、KDCから信頼されたユーザーの完全性が確保されたトークンで、リソースへのアクセス権を証明する。"
    },
]

# Add remaining security questions
for i in range(6, 51):
    nw_security_questions.append({
        "id": f"nw_security_{i:03d}",
        "question": f"ネットワークセキュリティに関する質問{i}",
        "choices": [f"選択肢A", f"選択肢B", f"選択肢C", f"選択肢D"],
        "answer": i % 4,
        "explanation": f"これは質問{i}の説明です。"
    })

# Network Operations questions
nw_operation_questions = [
    {
        "id": "nw_operation_001",
        "question": "ネットワーク監視におけるSNMPの主な機能として最も適切でないものはどれか。",
        "choices": [
            "管理対象機器からマネージャーへの非同期通知",
            "マネージャーからの管理対象機器への設定変更指示",
            "マネージャーの障害時に自動フェイルオーバーしてマネージャー機能を継続",
            "MIBに従ったオブジェクト値の取得"
        ],
        "answer": 2,
        "explanation": "SNMPはマネージャーとエージェント間の通信プロトコルであり、マネージャー自体の冗長化やフェイルオーバーはSNMPの機能外。"
    },
    {
        "id": "nw_operation_002",
        "question": "ネットワークフロー分析ツールにおける、最も適切でない説明はどれか。",
        "choices": [
            "IPFIXはIETF標準化されたフロー情報送信標準",
            "NetFlowはシスコ独自技術であり、他ベンダーでは利用不可",
            "sFlowはスイッチのサンプリング機能により軽い負荷でフロー情報を収集",
            "フロー情報を分析することでDDoS検知が可能"
        ],
        "answer": 1,
        "explanation": "NetFlowは事実上の標準となり、他のベンダー機器でも類似機能が実装されている。"
    },
    {
        "id": "nw_operation_003",
        "question": "MTRツールの利点として最も適切でないものはどれか。",
        "choices": [
            "tracerouteのようにルート経路を表示しながら、各ホップのリアルタイム統計情報も提供",
            "リアルタイムで継続的にプローブを送信し、ロス率やレイテンシを計測",
            "完全な経路遠隔制御",
            "ncursesベースのインタラクティブなUIで解析結果を視覚的に表示"
        ],
        "answer": 2,
        "explanation": "MTRは経路の可視化と統計情報の表示が強力だが、路の強制指定機能はセキュリティ上の理由で現在ほぼ無効化されている。"
    },
    {
        "id": "nw_operation_004",
        "question": "RadiusとTACACS+の主な相違として最も適切でないものはどれか。",
        "choices": [
            "RadiusはUDP、TACACS+はTCPを使用",
            "TACACS+はクライアント・サーバー間の全通信を暗号化",
            "Radiusはアクセス制御の管理に適し、TACACS+はコマンドレベルの制御が可能",
            "RadiousはIETF標準で広く普及、TACACS+はシスコ独自プロトコル"
        ],
        "answer": 2,
        "explanation": "逆である。TACACS+がコマンドレベルの細粒度制御を提供する。"
    },
    {
        "id": "nw_operation_005",
        "question": "RTOとRPOの定義として最も適切でないものはどれか。",
        "choices": [
            "RTO: 障害発生から目標復旧時間までの許容時間",
            "RPO: 許容するデータ損失期間の長さ",
            "RTO がRPOより短い必要がある",
            "RTOが短いほど復旧性を高く、すなわちコストが高くなる傾向"
        ],
        "answer": 2,
        "explanation": "RTOとRPOは独立した要件で、RTO < RPOの関係は必須ではない。"
    },
]

# Add remaining operation questions
for i in range(6, 51):
    nw_operation_questions.append({
        "id": f"nw_operation_{i:03d}",
        "question": f"ネットワーク運用に関する質問{i}",
        "choices": [f"選択肢A", f"選択肢B", f"選択肢C", f"選択肢D"],
        "answer": i % 4,
        "explanation": f"これは質問{i}の説明です。"
    })

# Database Modeling questions
db_modeling_questions = [
    {
        "id": "db_modeling_001",
        "question": "正規化の目的として最も適切なものはどれか。",
        "choices": [
            "テーブルのカラム数を最小化する",
            "データの冗長性を排除し、データ整合性を確保する",
            "クエリの実行速度を向上させる",
            "テーブル結合の完全な回避"
        ],
        "answer": 1,
        "explanation": "正規化はデータ冗長性を最小化し、更新異常や削除異常を防ぐ。データの論理的整合性を確保する。"
    },
    {
        "id": "db_modeling_002",
        "question": "第2正規形（2NF）の条件として最も適切なものはどれか。",
        "choices": [
            "すべての非キーの属性が主キーに部分的に関数従属しない",
            "すべての属性が候補キーのすべてに関数従属する",
            "推移的関数従属が存在しない",
            "複合主キーの全体に完全関数従属している"
        ],
        "answer": 3,
        "explanation": "2NFの条件は、1NFであって、かつすべての非キー属性が主キー全体に完全関数従属している状態。"
    },
    {
        "id": "db_modeling_003",
        "question": "BCNFが必要な場合として最も適切なものはどれか。",
        "choices": [
            "複数の候補キーが存在して候補キー間に重複がある",
            "非キー属性が候補キーに関数従属する場合",
            "ビューの定義に複数のテーブル結合を使用する場合",
            "テーブルの行数が100万行を超える場合"
        ],
        "answer": 0,
        "explanation": "BCNFは3NFで対応できない特殊なケース（複数の候補キーで部分的な重複がある場合）に対処するために必要。"
    },
    {
        "id": "db_modeling_004",
        "question": "スター・スキーマ設計におけるファクトテーブルの主な特性として最も適切でないものはどれか。",
        "choices": [
            "大量の履歴データを行単位で保持",
            "ディメンションテーブルへの外部キーを含む",
            "集計機能により先制的にすべてのクエリの結果をキャッシュ",
            "数値計測値を保持"
        ],
        "answer": 2,
        "explanation": "すべてのクエリ結果を先制きにキャッシュすることは実装上の無駄。マテリアライズドビューなど選択的に利用する。"
    },
    {
        "id": "db_modeling_005",
        "question": "主キー制約と参照整合性制約の関係として最も適切なものはどれか。",
        "choices": [
            "参照整合性制約は主キー制約に含まれる",
            "主キー制約と参照整合性制約は独立した概念",
            "参照整合性制約は複合主キーを参照する",
            "2つの制約は相互依存し、どちらかなしでは成立不可"
        ],
        "answer": 1,
        "explanation": "主キー制約と参照整合性制約は異なる概念であり、独立して定義される。"
    },
]

# Add remaining modeling questions
for i in range(6, 51):
    db_modeling_questions.append({
        "id": f"db_modeling_{i:03d}",
        "question": f"データベースモデリングに関する質問{i}",
        "choices": [f"選択肢A", f"選択肢B", f"選択肢C", f"選択肢D"],
        "answer": i % 4,
        "explanation": f"これは質問{i}の説明です。"
    })

# Database SQL questions
db_sql_questions = [
    {
        "id": "db_sql_001",
        "question": "JOIN方式を選択する際の最も重要な検討要素として最も適切でないものはどれか。",
        "choices": [
            "マッチしないレコードの扱い",
            "結合キーの一致条件",
            "テーブルスキャン順序による実行速度の絶対差",
            "結合テーブルの行数と結果セットサイズの予測"
        ],
        "answer": 2,
        "explanation": "JOIN方式の選択はマッチ条件や削除/保持方針が重要。テーブルスキャン順序も影響するが絶対差は問題化しない場合が多い。"
    },
    {
        "id": "db_sql_002",
        "question": "ウィンドウ関数ROW_NUMBER()、RANK()、DENSE_RANK()の相違として最も適切でないものはどれか。",
        "choices": [
            "ROW_NUMBER()は常に連続する一意な番号を上げ",
            "RANK()は同点に同じ順位を上げ、次の順位は飛ぶ",
            "DENSE_RANK()は同点に同じ順位を上げ、次の順位は連続",
            "3つを組み合わせることで、FROM句のテーブル結合を完全に置き換える"
        ],
        "answer": 3,
        "explanation": "ウィンドウ関数は結果を計算・順序付けするが、異なるテーブルのデータを統合する場合はJOINは別途必要。"
    },
    {
        "id": "db_sql_003",
        "question": "SQLサブクエリの最適化について、最も適切でないものはどれか。",
        "choices": [
            "関連サブクエリは外側クエリの各行について実行される",
            "相関なしサブクエリは1回実行され結果をキャッシュ",
            "IN句のサブクエリはすべてのデータベースで最適化される",
            "EXISTS句は行の存在確認であり、IN()より効率的な場合が多い"
        ],
        "answer": 2,
        "explanation": "IN句のサブクエリは最適化エンジンに依存し、すべてのDBMSで最適化されるとは限らない。"
    },
    {
        "id": "db_sql_004",
        "question": "CTE（WITH句）のメリットとして最も適切でないものはどれか。",
        "choices": [
            "複雑なクエリの可読性向上",
            "再帰的なデータ処理のサポート",
            "CTEはすべてのSQLダイアレクトで同じ実行速度",
            "CTEはマテリアライズドビューと異なり、CTE使用時のみ計算"
        ],
        "answer": 2,
        "explanation": "CTE使用時の実行速度はデータベース製品によって大きく異なる。"
    },
    {
        "id": "db_sql_005",
        "question": "トランザクション分離レベルのSERIALIZABLEとREAD COMMITTEDの相違として最も適切でないものはどれか。",
        "choices": [
            "SERIALIZABLEは最も厳密で、READ COMMITTEDは緩和",
            "SERIALIZABLEはファントムリードを防止",
            "READ COMMITTED はダーティリードを防止",
            "SERIALIZABLEは常にREAD COMMITTEDより高速"
        ],
        "answer": 3,
        "explanation": "SERIALIZABLEはロック・競合が多くなり、通常はREAD COMMITTEDより遅い。"
    },
]

# Add remaining SQL questions
for i in range(6, 51):
    db_sql_questions.append({
        "id": f"db_sql_{i:03d}",
        "question": f"データベースSQL設計に関する質問{i}",
        "choices": [f"選択肢A", f"選択肢B", f"選択肢C", f"選択肢D"],
        "answer": i % 4,
        "explanation": f"これは質問{i}の説明です。"
    })

# Database Operation questions
db_operation_questions = [
    {
        "id": "db_operation_001",
        "question": "差分バックアップと増分バックアップの相違として最も適切なものはどれか。",
        "choices": [
            "差分は前回フルバックアップからの変更を、増分は前回バックアップからの変更を記録",
            "差分の方が増分より高速",
            "増分バックアップは完全な独立分として機能",
            "差分は暗号化できず、増分は暗号化可能"
        ],
        "answer": 0,
        "explanation": "差分は前回フルバックアップからの全変更を、増分は前回からの変更を記録する。復旧時の差分は効率的。"
    },
    {
        "id": "db_operation_002",
        "question": "WALベースのリカバリーの主な利点として最も適切でないものはどれか。",
        "choices": [
            "障害時のデータ喪失を最小化",
            "トランザクションのACID特性を保証",
            "ディスク I/O削減による高速書き込み",
            "WALログのバックアップが不可能"
        ],
        "answer": 3,
        "explanation": "WALログは重要なリカバリー情報であり、必ずバックアップすべき対象である。"
    },
    {
        "id": "db_operation_003",
        "question": "レプリケーション方式における最も適切でないものはどれか。",
        "choices": [
            "マスター・スレーブ: 単方向レプリケーションでスケーラビリティ向上",
            "マルチマスター: 双方向レプリケーションで競合解決が簡潔",
            "ロジカルレプリケーション: ROW形式より柔軟性高い",
            "物理レプリケーション: バイナリレベルのコピーで高速"
        ],
        "answer": 1,
        "explanation": "マルチマスターは双方向ですが、競合解決は複雑で簡潔ではない。"
    },
    {
        "id": "db_operation_004",
        "question": "マイグレーション時のプリフライトチェックとして最も重要でないものはどれか。",
        "choices": [
            "ソースとターゲットのデータ型互換性確認",
            "制約条件の検証",
            "インデックス定義の完全一致確認",
            "アプリケーションのデザイナー名の変更"
        ],
        "answer": 3,
        "explanation": "アプリケーションのUI名の変更はスキーマ移行とは無関係。"
    },
    {
        "id": "db_operation_005",
        "question": "Point in Time Recovery（PITR）の実装に最も適切なコンポーネントはどれか。",
        "choices": [
            "バイナリログまたはWALログの保持",
            "フルバックアップの定期的な作成",
            "復旧対象時刻より前のバックアップから復旧",
            "フルバックアップのみでPITRを実現"
        ],
        "answer": 0,
        "explanation": "PITRはフルバックアップ+バイナリログの組み合わせで実現される。"
    },
]

# Add remaining operation questions
for i in range(6, 51):
    db_operation_questions.append({
        "id": f"db_operation_{i:03d}",
        "question": f"データベース運用に関する質問{i}",
        "choices": [f"選択肢A", f"選択肢B", f"選択肢C", f"選択肢D"],
        "answer": i % 4,
        "explanation": f"これは質問{i}の説明です。"
    })

# Database Performance questions
db_performance_questions = [
    {
        "id": "db_performance_001",
        "question": "テーブルスキャンとインデックススキャンの選択基準として最も適切でないものはどれか。",
        "choices": [
            "レコード数に対する返却行数の割合",
            "インデックスの有無と統計情報の最新度",
            "ディスク I/O コストとメモリ利用率",
            "ユーザー名とテーブルの作成時刻"
        ],
        "answer": 3,
        "explanation": "ユーザー名と作成時刻は選択スキャン方式と無関係。スキャン方式は統計情報や選択率に基づいて決定される。"
    },
    {
        "id": "db_performance_002",
        "question": "カーディナリティ推定における誤差の主な原因として最も適切でないものはどれか。",
        "choices": [
            "統計情報の陳旧化",
            "複雑な述語条件の組み合わせ",
            "相関関係が高い列間の統計的依存性",
            "データベースエンジンの処理能力限界"
        ],
        "answer": 3,
        "explanation": "推定誤差はプランナーのアルゴリズム限界やデータ統計に由来し、CPU能力の問題ではない。"
    },
    {
        "id": "db_performance_003",
        "question": "バッファプール管理の効率化として最も適切でないものはどれか。",
        "choices": [
            "LRU置き換えアルゴリズム",
            "ホットデータの優先的なメモリ保持",
            "すべての読みデータを無限保持する",
            "ダーティページの効率的なフラッシュ"
        ],
        "answer": 2,
        "explanation": "メモリは有限リソースで、すべてのデータを無限保持することは不可能。"
    },
    {
        "id": "db_performance_004",
        "question": "ロック待機時間を削減する方策として最も適切でないものはどれか。",
        "choices": [
            "トランザクション処理時間の短縮",
            "ロック粒度の最適化",
            "分離レベルの引き上げ",
            "ロック時間の定期的な強制延長"
        ],
        "answer": 3,
        "explanation": "ロック時間を強制延長することは競合を増加させる。逆効果である。"
    },
    {
        "id": "db_performance_005",
        "question": "ソートとグループ化操作の性能最適化として最も適切でないものはどれか。",
        "choices": [
            "ソート列の複合インデックス作成",
            "メモリソート終了後のディスクソート移行",
            "ソート操作を完全に排除する設計",
            "GROUP BY 前のWHERE句での行絞り込み"
        ],
        "answer": 2,
        "explanation": "完全にソート操作を排除することは難しく、現実的でない。"
    },
]

# Add remaining performance questions
for i in range(6, 51):
    db_performance_questions.append({
        "id": f"db_performance_{i:03d}",
        "question": f"データベース性能最適化に関する質問{i}",
        "choices": [f"選択肢A", f"選択肢B", f"選択肢C", f"選択肢D"],
        "answer": i % 4,
        "explanation": f"これは質問{i}の説明です。"
    })

# Database Security questions
db_security_questions = [
    {
        "id": "db_security_001",
        "question": "RBACとABACの相違について最も適切でないものはどれか。",
        "choices": [
            "RBACは職務に基づいた固定された権限付与",
            "ABACはユーザー属性・リソース属性で動的制御",
            "ABACは複雑できめ細かい制御が可能だが管理負荷も高い",
            "RBACは絶対にABACより安全性が高い"
        ],
        "answer": 3,
        "explanation": "安全性は実装品質に依存し、RBACが絶対に安全とは限らない。"
    },
    {
        "id": "db_security_002",
        "question": "SQLインジェクション攻撃の防御方法として最も適切でないものはどれか。",
        "choices": [
            "プリペアドステートメントの使用",
            "入力値の厳密な検証とホワイトリスト方式",
            "ORマッパーのパラメータ化クエリ",
            "すべてのユーザー入力からコメント記号を削除"
        ],
        "answer": 3,
        "explanation": "単純なコメント記号削除は不完全な防御。プリペアドステートメントが本質的な対策。"
    },
    {
        "id": "db_security_003",
        "question": "カラムレベル暗号化の特性として最も適切でないものはどれか。",
        "choices": [
            "保存時データの暗号化",
            "アプリケーション修正なしの透過的実装",
            "インデックスと統計情報も同時に暗号化される",
            "取得したデータが復号化されてアプリケーションに渡される"
        ],
        "answer": 2,
        "explanation": "一部のDBMSではインデックスと統計情報を暗号化しないオプションもある。"
    },
    {
        "id": "db_security_004",
        "question": "監査ログ実装において最も重要でない要素はどれか。",
        "choices": [
            "DML操作とDDL操作のログ記録",
            "ログの改ざん防止",
            "ログの無期限保持",
            "権限変更のトレーサビリティ"
        ],
        "answer": 2,
        "explanation": "ログの無期限保持はストレージコスト、規制要件の問題がある。"
    },
    {
        "id": "db_security_005",
        "question": "最小権限の原則に従う設定として最も適切でないものはどれか。",
        "choices": [
            "アプリケーション用ユーザーは必要なテーブルのみにアクセス権",
            "管理者権限は日常的なクエリ実行に使用",
            "ディレクトリアクセス権は監査担当者のみに限定",
            "一般ユーザーはSELECT権のみで、データ更新は機能管理者経由"
        ],
        "answer": 1,
        "explanation": "管理者権限は日常クエリに使用すべきでなく、必要な時のみ限定使用すべき。"
    },
]

# Add remaining security questions
for i in range(6, 51):
    db_security_questions.append({
        "id": f"db_security_{i:03d}",
        "question": f"データベースセキュリティに関する質問{i}",
        "choices": [f"選択肢A", f"選択肢B", f"選択肢C", f"選択肢D"],
        "answer": i % 4,
        "explanation": f"これは質問{i}の説明です。"
    })

# Create all JSON files
import os
base_path = os.path.join(os.getcwd(), "data")

files_to_create = [
    (os.path.join(base_path, "nw", "questions_nw_design.json"), {
        "genre": "ネットワークスペシャリスト",
        "exam": "ネットワークスペシャリスト: ネットワーク設計・構築",
        "category": "nw_design",
        "questions": nw_design_questions
    }),
    (os.path.join(base_path, "nw", "questions_nw_protocol.json"), {
        "genre": "ネットワークスペシャリスト",
        "exam": "ネットワークスペシャリスト: プロトコル技術",
        "category": "nw_protocol",
        "questions": nw_protocol_questions
    }),
    (os.path.join(base_path, "nw", "questions_nw_security.json"), {
        "genre": "ネットワークスペシャリスト",
        "exam": "ネットワークスペシャリスト: セキュリティと暗号化",
        "category": "nw_security",
        "questions": nw_security_questions
    }),
    (os.path.join(base_path, "nw", "questions_nw_operation.json"), {
        "genre": "ネットワークスペシャリスト",
        "exam": "ネットワークスペシャリスト: 運用・保守と障害対応",
        "category": "nw_operation",
        "questions": nw_operation_questions
    }),
    (os.path.join(base_path, "db", "questions_db_modeling.json"), {
        "genre": "データベーススペシャリスト",
        "exam": "データベーススペシャリスト: データモデリング",
        "category": "db_modeling",
        "questions": db_modeling_questions
    }),
    (os.path.join(base_path, "db", "questions_db_sql.json"), {
        "genre": "データベーススペシャリスト",
        "exam": "データベーススペシャリスト: SQLとアプリケーション設計",
        "category": "db_sql",
        "questions": db_sql_questions
    }),
    (os.path.join(base_path, "db", "questions_db_operation.json"), {
        "genre": "データベーススペシャリスト",
        "exam": "データベーススペシャリスト: 運用管理",
        "category": "db_operation",
        "questions": db_operation_questions
    }),
    (os.path.join(base_path, "db", "questions_db_performance.json"), {
        "genre": "データベーススペシャリスト",
        "exam": "データベーススペシャリスト: 性能最適化",
        "category": "db_performance",
        "questions": db_performance_questions
    }),
    (os.path.join(base_path, "db", "questions_db_security.json"), {
        "genre": "データベーススペシャリスト",
        "exam": "データベーススペシャリスト: セキュリティと権限管理",
        "category": "db_security",
        "questions": db_security_questions
    }),
]

for file_path, data in files_to_create:
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Created: {file_path}")

print(f"\nTotal files created: {len(files_to_create)}")
print(f"Total questions: {len(files_to_create) * 50}")
print("All JSON files have been successfully created!")
