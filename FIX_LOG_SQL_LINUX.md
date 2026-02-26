# SQL と Linux エラー修正ログ

## 修正日時
2026年2月26日

## 問題原因
genres.json に記録されている `count` 値が、実際の質問ファイル内の問題数と不一致していました。

### 発見されたエラー

1. **genres.json JSON 構文エラー**
   - 行1178: `,` 区切り文字が欠落
   - en_conversation と en_writing の間に `,` が必要

2. **SQL セクション count ミスマッチ**
   - sql_select: 50 → 10 問に修正
   - sql_functions: 50 → 10 問に修正  
   - sql_group: 50 → 10 問に修正
   - sql_join: 50 → 10 問に修正
   - sql_subquery: 50 → 10 問に修正
   - sql_dml_ddl: 50 → 10 問に修正
   - sql_window_functions: 100 → 50 問に修正
   - sql_advanced: 100 → 50 問に修正

3. **Linux セクション count ミスマッチ**
   - linux_users_groups: 100 → 50 問に修正
   - linux_boot_kernel: 100 → 50 問に修正
   - linux_firewall: 100 → 50 問に修正
   - linux_network_dns: 100 → 50 問に修正
   - linux_storage: 100 → 50 問に修正
   - linux_sysadmin: 100 → 50 問に修正

## 実施内容

1. **genres.json JSON 構文修正**
   - 1178行の `,` を追加

2. **Python スクリプト実行**
   - `fix_counts.py`: genres.json の count 値を実ファイルと同期
   - 14カ所の修正を実施

3. **検証完了**
   - ✓ genres.json JSON 構文: 正常
   - ✓ SQL ファイル: 9/9 有効
   - ✓ Linux ファイル: 11/11 有効
   - ✓ SQL/Linux count 値: 全て一致

## ブラウザ表示
- 修正前: TypeError: Cannot read properties of undefined (reading 'map')
- 修正後: ✅ エラー消滅、正常に動作

## 備考
- その他 70 のセクションでも count ミスマッチが存在（SQL/Linux 以外）
- これらは別途修正が必要な場合があります
