# QuizForge — 環境構築・運用ガイド

## 目次
1. [ファイル構成](#ファイル構成)
2. [ローカル環境の起動](#ローカル環境の起動)
3. [本番環境へのデプロイ](#本番環境へのデプロイ)
4. [問題・ジャンルの追加方法](#問題ジャンルの追加方法)
5. [トラブルシューティング](#トラブルシューティング)

---

## ファイル構成

```
quizforge/
├── index.html                          ← サイト本体（単一HTMLファイル）
├── data/
│   ├── genres.json                     ← ジャンル階層の定義ファイル（★メイン管理）
│   ├── fe/                             ← 基本情報技術者試験の問題
│   │   ├── questions_fe_computer.json  │
│   │   ├── questions_fe_system.json    │
│   │   ├── questions_fe_software.json  │
│   │   ├── questions_fe_hardware.json  │
│   │   ├── questions_fe_network.json   │  各10問
│   │   ├── questions_fe_db.json        │
│   │   ├── questions_fe_security.json  │
│   │   ├── questions_fe_algorithm.json │
│   │   ├── questions_fe_management.json│
│   │   └── questions_fe_strategy.json  │
│   ├── ap/                             ← 応用情報（準備中）
│   └── sg/                             ← セキュリティマネジメント（準備中）
└── SETUP.md                            ← このファイル
```

---

## ローカル環境の起動

> ⚠️ `index.html` をブラウザで**直接ダブルクリック**して開くと、  
> JSONファイルの読み込みが「CORS制限」でブロックされます。  
> **必ずローカルサーバを経由**してアクセスしてください。

### 方法 A：Node.js（npx serve）— 推奨

```bash
# Node.js がインストール済みの場合（バージョン確認）
node -v

# プロジェクトフォルダに移動
cd /path/to/quizforge

# ワンコマンドで起動（インストール不要）
npx serve .

# ブラウザで開く
# → http://localhost:3000
```

### 方法 B：Python（標準ライブラリのみ）

```bash
# Python 3 の場合
cd /path/to/quizforge
python3 -m http.server 8080

# ブラウザで開く
# → http://localhost:8080
```

```bash
# Python 2 の場合（古い環境）
python -m SimpleHTTPServer 8080
```

### 方法 C：VS Code（Live Server 拡張）

1. VS Code に「**Live Server**」拡張機能をインストール
2. `index.html` をエディタで開く
3. 右下の「**Go Live**」ボタンをクリック
4. ブラウザが自動で開き、ファイル変更を自動リロード

### 方法 D：PHP（Webサーバ内蔵）

```bash
cd /path/to/quizforge
php -S localhost:8080

# → http://localhost:8080
```

---

## 本番環境へのデプロイ

このサイトは**静的ファイルのみ**で構成されています（サーバサイド処理なし）。  
静的ホスティングサービスに対応しています。

---

### 方法 1：GitHub Pages（無料・おすすめ）

#### 初回セットアップ

```bash
# 1. GitHubでリポジトリを作成（Public推奨）
# 2. ローカルにリポジトリを初期化
cd /path/to/quizforge
git init
git add .
git commit -m "first commit"

# 3. GitHubにプッシュ
git remote add origin https://github.com/YOUR_USERNAME/quizforge.git
git push -u origin main
```

#### GitHub Pages を有効化

```
GitHubリポジトリ → Settings → Pages
→ Source: "Deploy from a branch"
→ Branch: main / root
→ Save
```

#### 公開URL

```
https://YOUR_USERNAME.github.io/quizforge/
```

#### 更新のデプロイ

```bash
git add .
git commit -m "問題を追加"
git push
# → 約1〜2分後に自動で反映
```

---

### 方法 2：Netlify（ドラッグ＆ドロップ）

1. [https://netlify.com](https://netlify.com) にアクセス・サインアップ
2. ダッシュボードの「**Sites**」→ フォルダをドラッグ＆ドロップ
3. 数秒で公開 → ランダムなURLが発行される
4. カスタムドメインも無料で設定可能

```
公開URL例: https://quizforge-abc123.netlify.app
```

#### GitHubと連携した自動デプロイ

```
Netlify → New Site → Import from GitHub
→ リポジトリを選択 → Deploy
→ pushするたびに自動デプロイ
```

---

### 方法 3：Vercel

```bash
# Vercel CLI をインストール
npm install -g vercel

# プロジェクトフォルダでデプロイ
cd /path/to/quizforge
vercel

# 本番デプロイ
vercel --prod
```

---

### 方法 4：レンタルサーバ（FTP）

XserverやさくらインターネットなどのレンタルサーバへFTPで全ファイルをアップロードします。

```
アップロード先（例）:
/public_html/quizforge/
  ├── index.html
  └── data/
      ├── genres.json
      └── fe/
          └── *.json
```

> **注意：** ファイルのパス（data/ ディレクトリ構造）を保持したままアップロードしてください。

---

## 問題・ジャンルの追加方法

### 1. 問題ファイルの追加

`data/` 以下に任意のフォルダ名でJSONを配置します。

**問題ファイルの形式（例: data/fe/questions_fe_newgenre.json）**

```json
{
  "genre": "ジャンル名",
  "exam": "試験名",
  "questions": [
    {
      "id": "一意のID（例: fe_new_001）",
      "question": "問題文をここに記述する。\n改行はそのまま書けます。",
      "choices": [
        "選択肢A",
        "選択肢B",
        "選択肢C（正解）",
        "選択肢D"
      ],
      "answer": 2,
      "explanation": "正解はCです。なぜなら〜という理由です。追加の解説を詳しく書けます。"
    }
  ]
}
```

**フィールド仕様：**

| フィールド | 型 | 説明 |
|---|---|---|
| `id` | string | 全問題でユニークなID |
| `question` | string | 問題文（`\n`で改行可） |
| `choices` | string[] | 選択肢の配列（2〜6個対応） |
| `answer` | number | 正解の選択肢インデックス（0始まり） |
| `explanation` | string | 解説文 |

---

### 2. genres.json への登録

`data/genres.json` を編集してジャンルを追加します。

#### 新しいセクション（既存の試験に追加）

```json
{
  "id": "fe_newgenre",
  "name": "新しいジャンル名",
  "icon": "🔬",
  "description": "ジャンルの説明文",
  "file": "data/fe/questions_fe_newgenre.json",
  "count": 10
}
```

→ `fe` の `sections` 配列に追加するだけで自動表示されます。

#### 新しい試験区分を追加

```json
{
  "id": "new_exam",
  "name": "新しい試験名",
  "short": "NE",
  "level": "レベル3",
  "icon": "🔵",
  "description": "試験の説明",
  "color": "#8b5cf6",
  "sections": [
    {
      "id": "ne_section1",
      "name": "セクション名",
      "icon": "📘",
      "description": "セクションの説明",
      "file": "data/new_exam/questions_ne_section1.json",
      "count": 10
    }
  ]
}
```

→ `subjects[0].exams` 配列に追加するだけです。

#### 準備中のセクションを表示（coming soon）

```json
{
  "id": "upcoming_section",
  "name": "準備中セクション",
  "icon": "🔜",
  "description": "近日公開予定",
  "file": "data/upcoming.json",
  "count": 0,
  "coming_soon": true
}
```

---

### 3. 英語・他教科の追加例

新しい教科（subjects）を追加する場合は `subjects` 配列に追記します。

```json
{
  "subjects": [
    { "id": "it_exam", ... },
    {
      "id": "english",
      "name": "英語",
      "icon": "🇬🇧",
      "description": "TOEIC・英検・センター英語など",
      "exams": [
        {
          "id": "toeic",
          "name": "TOEIC L&R",
          "short": "TOEIC",
          "level": "スコア制",
          "icon": "🟠",
          "description": "リスニング・リーディングの問題",
          "color": "#f97316",
          "sections": [
            {
              "id": "toeic_vocab",
              "name": "語彙・単語",
              "icon": "📖",
              "description": "Part 5・6の語彙問題",
              "file": "data/toeic/questions_toeic_vocab.json",
              "count": 10
            }
          ]
        }
      ]
    }
  ]
}
```

---

## トラブルシューティング

### ❌ 「データ読み込みエラー」が表示される

**原因：** HTMLファイルをブラウザで直接ダブルクリックして開いている（file://プロトコル）

**解決策：** ローカルサーバを経由してアクセスする
```bash
npx serve .   # または python3 -m http.server 8080
```

---

### ❌ JSONを追加したのにサイトに反映されない

**確認ポイント：**
1. `data/genres.json` に正しく `file` パスが記載されているか確認
2. JSONファイルのパスが `genres.json` の記載と一致しているか確認
3. JSONの構文エラーがないか確認（ブラウザのDevTools → Consoleタブ）

```bash
# JSONの構文チェック（Python）
python3 -c "import json; json.load(open('data/genres.json'))"
echo "OK"
```

---

### ❌ 問題がシャッフルされてほしくない

`index.html` の以下の行を編集します。

```javascript
// シャッフルを無効にする場合
questions = [...data.questions];  // shuffle() を削除

// シャッフルを有効にする場合（デフォルト）
questions = shuffle([...data.questions]);
```

---

### ❌ GitHub Pagesでアクセスできない

- `Settings → Pages` が正しく設定されているか確認
- リポジトリが **Public** になっているか確認（PrivateはProプランが必要）
- デプロイに最大5分かかる場合があります

---

## よくある運用パターン

### 問題を増やすワークフロー

```
1. 問題をJSONファイルに追記（またはファイル新規作成）
2. genres.json を更新（count を更新、または新規セクションを追加）
3. git commit & push → 自動デプロイ
```

### 問題ファイルの命名規則（推奨）

```
data/{試験ID}/questions_{試験ID}_{セクションID}.json

例:
data/fe/questions_fe_algorithm.json
data/ap/questions_ap_network.json
data/toeic/questions_toeic_vocab.json
data/eiken/questions_eiken2_grammar.json
```
