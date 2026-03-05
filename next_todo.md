前提事項
・エラーが発生した場合は処理を中断するのではなく、エラーが解消するまで調査と再実行を繰り返し実施すること
・追加する問題は過去にその試験で出題された文言や内容に対する問題であること。過去問題の調査をした資料はすでに存在するのでそれを使用し、今ある問題と重複した内容にならないようにすること。
・以下のTodosの内容を実行すること

TODOS
以下はレビューで発生した問題点と実施済みの修正／追加したスクリプトの一覧です。

1. **不適切な選択肢表現**
   - 数字を使って "何番と何番" と記述する形式は不適切であるため
     自動・手動で全件修正済み。
   - 例: linux_network_dns で "選択肢1と3両方正しい" を
     "ip link set eth0 mtu 1500 と ifconfig eth0 mtu 1500 の両方" に
     変更。
   - 他にも "選択肢1と2両方正しい" などがあったため同様に修正。
   - 検出用スクリプト `find_ac_anomalies.py` を追加し、同種パターン
     の自動発見が可能。

2. **重複・矛盾する正解表記**
   - C の選択肢内に "AとC" などが含まれているものは全件調査し
     D ではなく正しい選択肢へ修正済み。
   - 上記スクリプトでもチェックできるため、今後の追加時も実行。

3. **システム監査技術者：システム監査計画 の偏り** ✅ 完了
   - 正解選択肢が最も長文になるバイアスを検出。
   - `shuffle_section.py` で選択肢をシャッフルし、`normalize_lengths.py`
     で他の選択肢を長さ揃えしてバイアスを除去。
   - 現在 50 問すべてで "正解が唯一最長" という状態は解消済み。

4. **TOEIC/TOEFL の日本語解説** ✅ 完全完了
   - `add_translation_fields.py` により 7 ファイル 350 問に
     ja_question/ja_explanation フィールドを追加済み。
   - 最初の辞書ベース翻訳（`translate_dict.py`）：TOEFL Listening の一部（15 問）のみ翻訳
   - **オンライン翻訳の実施:**
     - `translate_google_online.py` でGoogle翻訳をオンラインで実行
     - 残り335問のすべての英語フィールドを日本語に自動翻訳完了
   
   **最終翻訳結果（100% 完了）:**
     - TOEIC Listening: 50/50 ✓
     - TOEIC Reading: 50/50 ✓
     - TOEIC Vocab: 50/50 ✓
     - TOEFL Listening: 50/50 ✓
     - TOEFL Reading: 50/50 ✓
     - TOEFL Speaking: 50/50 ✓
     - TOEFL Writing: 50/50 ✓
     - **合計: 350/350 質問 (100%) + 350/350 解説 (100%)**
   
   **使用技術:**
   - googletrans ライブラリ（Google翻訳API）
   - マルチファイル処理、リトライ機能、レート制限対応を実装

---

上記のスクリプトは `scripts/` ではなくルートに置かれています。
ファイルを更新したら、`validate_all_questions.py` 等で検証を
忘れないでください。

修正完了後は本ファイルに進捗を追記してください。

---

## 収集された翻訳スクリプト（ルート階層）
- `translate_dict.py` - TOEIC/TOEFL 共通パターンの辞書（日本語翻訳マッピング）
- `apply_translations.py` - 辞書を使用して ja_* フィールドを翻訳
- `reset_translations.py` - ja_* フィールドをプレースホルダーにリセット（再翻訳用）
- `fill_ja_fields_with_english.py` - 英語で埋める補助スクリプト
- `check_translation_status.py` - 翻訳状況の確認用スクリプト
- `translate_google_online.py` - Google翻訳によるオンライン翻訳（最終使用スクリプト）

**削除済みパッケージ:**
- transformers, torch, fugashi, unidic-lite, sentencepiece（オフライン翻訳用）- ネットワーク制限に対応するため削除

**使用中のパッケージ:**
- googletrans 4.0.0rc1（Google翻訳API）
- `translate_google_online.py` - **Google翻訳によるオンライン翻訳（最終使用スクリプト）**

**削除済みパッケージ:**
- transformers, torch, fugashi, unidic-lite, sentencepiece（オフライン翻訳用）

**使用中のパッケージ:**
- googletrans 4.0.0rc1（Google翻訳API）


