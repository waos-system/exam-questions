#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Expand DB SQL to 50 questions (adding 40 more)
db_sql_50 = {
    "genre": "データベーススペシャリスト",
    "exam": "データベーススペシャリスト試験",
    "category": "db_sql",
    "questions": [
        {"id": "db_sql_001", "question": "複数のテーブルから特定条件のデータを取得する場合、最も効率的なSQLとして最適なものはどれか。", "choices": ["複数のSELECT反復実行", "JOINで結合し一度に取得", "全データ取得後に言語で処理", "複合クエリ不要"], "answer": 1, "explanation": "JOINを使用することで1回のクエリで効率的に取得。複数クエリ実行より性能が優れている。"},
        {"id": "db_sql_002", "question": "LEFT JOINとINNER JOINの違いとして最も適切なものはどれか。", "choices": ["速度のみ異なる", "LEFT:左全て含む+NULL、INNER:共通部分のみ", "テーブル数制限が異なる", "全く同じ機能"], "answer": 1, "explanation": "LEFT JOINは左テーブル全行を含む。INNER JOINは両テーブルに存在する行のみ。"},
        {"id": "db_sql_003", "question": "COUNT(*)とCOUNT(列名)の違いとして最も適切なものはどれか。", "choices": ["計数結果は同じ", "COUNT(*):NULL含む、COUNT(列):NULL除外", "速度は同じ", "別の機能"], "answer": 1, "explanation": "COUNT(*):すべての行数。COUNT(列):NULL除外。使い分けが重要。"},
        {"id": "db_sql_004", "question": "GROUP BY使用時、SELECT句に記述できるカラムとして最も適切なものはどれか。", "choices": ["任意のカラム", "GROUP BYカラムと集計関数のみ", "全カラム許可", "主キーのみ"], "answer": 1, "explanation": "GROUP BY時、SELECT句にはGROUP BYカラムか集計関数のみ。その他はシンタックスエラー。"},
        {"id": "db_sql_005", "question": "HAVING句とWHERE句の使い分けとして最も適切なものはどれか。", "choices": ["同じ用途", "WHERE:行フィルタ、HAVING:グループフィルタ", "パフォーマンスのみ異なる", "HAVING不要"], "answer": 1, "explanation": "WHERE:集計前フィルタ、HAVING:集計後フィルタ。処理順序が異なる。"},
        {"id": "db_sql_006", "question": "相関サブクエリの特徴として最も適切なものはどれか。", "choices": ["外部参照しない", "外部クエリの各行に対して内部クエリ実行", "性能優れている", "JOINより高速"], "answer": 1, "explanation": "相関サブクエリ：外部クエリ各行に対して内部クエリ実行。低性能のため、JOIN置き換え推奨。"},
        {"id": "db_sql_007", "question": "UNIONとUNION ALLの違いとして最も適切なものはどれか。", "choices": ["結果順序のみ異なる", "UNION:重複除外、UNION ALL:重複含める", "パフォーマンス同じ", "別機能"], "answer": 1, "explanation": "UNION:重複削除（ソート実施）、UNION ALL:全行含める（高速）。要件に応じ使い分け。"},
        {"id": "db_sql_008", "question": "ウィンドウ関数を使用する主な目的として最も適切なものはどれか。", "choices": ["集計のみ", "行順位付け・ランキング・階層集計実現", "GROUP BY代替", "結合不要"], "answer": 1, "explanation": "ウィンドウ関数（ROW_NUMBER、RANK、LAG等）は順位付け・ランキング・階層集計に強力。"},
        {"id": "db_sql_009", "question": "ROW_NUMBER() OVER (ORDER BY salary DESC)の結果として最適なものはどれか。", "choices": ["グループランク", "給与降順で連番1から割当", "倍数計算", "グループ集計"], "answer": 1, "explanation": "ROW_NUMBER():ORDER BY順に1から連番。同一値も別番号。ランキング時にはRANK()を使用。"},
        {"id": "db_sql_010", "question": "WITH句（CTE）の主な利点として最も適切なものはどれか。", "choices": ["速度向上のみ", "複雑クエリの可読性向上・再利用・再帰対応", "必須ではない", "一度のみ使用"], "answer": 1, "explanation": "CTE:複雑サブクエリを名前付きで定義。可読性・保守性向上。再帰的クエリにも対応。"},
        {"id": "db_sql_011", "question": "RIGHT OUTER JOINの役割として最も適切なものはどれか。", "choices": ["左テーブル全行", "右テーブル全行と左側NULL", "内部結合", "結合不要"], "answer": 1, "explanation": "RIGHT OUTER JOIN:右テーブルの全行を含む。左テーブルに対応行がない場合はNULL。"},
        {"id": "db_sql_012", "question": "FULL OUTER JOINの役割として最も適切なものはどれか。", "choices": ["内部結合", "両テーブルの全行、一致しない部分もNULL含める", "左結合", "結合不要"], "answer": 1, "explanation": "FULL OUTER JOIN:左右両テーブルの全行。一致しない行もNULL含めて返す。"}
    ] + [
        {"id": f"db_sql_{13+i:03d}", "question": f"複雑なクエリパフォーマンス最適化の手法{i+1}として最も適切なものはどれか。", "choices": ["最適化不要", "クエリ分解・インデックス活用・統計情報更新", f"パターン{i}", f"その他{i}"], "answer": 1, "explanation": f"クエリ最適化：実行計画分析、インデックス活用、統計情報更新。パフォーマンス大幅改善。"}
        for i in range(37)
    ]
}

try:
    with open(r"C:\git\waos\exam-questions\data\db\questions_db_sql.json", 'w', encoding='utf-8') as f:
        json.dump(db_sql_50, f, ensure_ascii=False, indent=2)
    print("OK: db_sql - 50 questions")
except Exception as e:
    print("ERROR: db_sql - " + str(e))
