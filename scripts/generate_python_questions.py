import json
from pathlib import Path


def q(qid, question, choices, answer, explanation):
    return {
        "id": qid,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
    }


def make_questions(prefix, items):
    out = []
    for i, item in enumerate(items, start=1):
        out.append(
            q(
                f"{prefix}_{i:03d}",
                item[0],
                item[1],
                item[2],
                item[3],
            )
        )
    if len(out) != 30:
        raise ValueError(f"{prefix} must have 30 questions, got {len(out)}")
    return out


def build_syntax():
    items = [
        ("Pythonで単一行コメントを記述する書き方はどれか。", ["//", "#", "/* */", "--"], 1, "コメントは # で始める。"),
        ("変数xに10を代入する文として適切なものはどれか。", ["x := 10", "int x = 10", "x = 10", "let x = 10"], 2, "Pythonでは型宣言なしで x = 10 と書く。"),
        ("条件分岐で使用するキーワードはどれか。", ["if", "case", "switch", "when"], 0, "条件分岐の基本は if。"),
        ("0から4まで反復するfor文として正しいものはどれか。", ["for i in range(5):", "for(i=0;i<5;i++)", "foreach i range(5)", "for i to 5"], 0, "range(5) は 0,1,2,3,4 を生成する。"),
        ("whileループを途中で終了させる文はどれか。", ["continue", "pass", "break", "stop"], 2, "break はループ自体を終了する。"),
        ("現在の反復を飛ばして次に進める文はどれか。", ["break", "continue", "pass", "return"], 1, "continue は現在回をスキップして次へ進む。"),
        ("関数定義に使うキーワードはどれか。", ["func", "def", "lambda", "function"], 1, "通常の関数定義は def を使う。"),
        ("関数から値を返す文はどれか。", ["yield", "return", "pass", "break"], 1, "返却には return を使う。"),
        ("何もしない文として使われるものはどれか。", ["null", "pass", "void", "skip"], 1, "pass は構文上必要だが処理不要なときに使う。"),
        ("f文字列でnameを埋め込む書き方はどれか。", ["""{name}""", "f""{name}""", """$name""", "fmt(name)"], 1, "f""...{name}..."" で式を埋め込める。"),
        ("リスト内包表記として正しいものはどれか。", ["[x*x for x in range(5)]", "{x*x in range(5)}", "(x*x where x in range(5))", "[for x in range(5): x*x]"], 0, "リスト内包表記は [式 for 変数 in 反復可能オブジェクト]。"),
        ("論理ANDを表す演算子はどれか。", ["&&", "and", "&", "AND"], 1, "論理演算子は and / or / not。"),
        ("等価比較に使う演算子はどれか。", ["=", "==", ":=", "is"], 1, "== は値の等価比較。"),
        ("同一オブジェクトかどうかを判定する演算子はどれか。", ["==", "is", "=", "eq"], 1, "is は同一性判定で、値比較は ==。"),
        ("可変長の位置引数を受け取る書き方はどれか。", ["*args", "&args", "args*", "#args"], 0, "*args で位置引数をタプルとして受け取る。"),
        ("可変長のキーワード引数を受け取る書き方はどれか。", ["*kwargs", "**kwargs", "kwargs*", "##kwargs"], 1, "**kwargs で辞書として受け取る。"),
        ("デフォルト引数の評価タイミングとして正しいものはどれか。", ["関数呼び出し時", "モジュール読み込み時", "return時", "毎行実行時"], 1, "デフォルト引数は関数定義時に評価される。"),
        ("global宣言の説明として正しいものはどれか。", ["ローカル変数を作る", "外側関数の変数を指す", "モジュールレベル変数を更新可能にする", "定数宣言する"], 2, "global はモジュールスコープの変数を代入対象にする。"),
        ("nonlocal宣言の説明として正しいものはどれか。", ["グローバル変数を更新する", "直近の外側関数スコープ変数を更新する", "定数を作る", "クラス変数を定義する"], 1, "nonlocal はネストした外側関数の変数を再束縛する。"),
        ("enumerate(seq)の主な用途はどれか。", ["要素の型変換", "インデックス付き反復", "逆順反復", "要素削除"], 1, "enumerate は (index, value) を返す。"),
        ("zip(a, b)の動作として適切なものはどれか。", ["aとbを連結する", "aとbを要素ごとに組にする", "aからbを引く", "aとbをソートする"], 1, "zip は同位置の要素をまとめる。"),
        ("assert文の目的として適切なものはどれか。", ["本番エラーを必ず抑止する", "デバッグ時に前提条件を検証する", "関数を定義する", "型を固定する"], 1, "assert は前提が偽なら AssertionError を送出する。"),
        ("代入式(ウォルラス演算子)として正しいものはどれか。", ["x == 10", "x := 10", "x => 10", "x =: 10"], 1, ":= で式内代入ができる。"),
        ("リスト内包表記で偶数のみ抽出する式はどれか。", ["[x for x in nums if x % 2 == 0]", "[if x%2==0 for x in nums]", "[x if x%2==0 in nums]", "[x from nums where even]"], 0, "条件は for 句の後ろに if で記述する。"),
        ("三項演算子の書式として正しいものはどれか。", ["a ? b : c", "b if a else c", "if a then b else c", "a ?: b : c"], 1, "Pythonの条件式は 値1 if 条件 else 値2。"),
        ("with文を使う主な目的はどれか。", ["グローバル変数の宣言", "リソースの自動解放", "繰返し回数の固定", "型の強制"], 1, "with を使うと終了時に後始末が自動実行される。"),
        ("多重代入として正しいものはどれか。", ["a,b = 1,2", "a:=1,b:=2", "int a,b = 1,2", "a=1; b:=2"], 0, "タプルのアンパックで同時代入できる。"),
        ("関数アノテーションの説明として適切なものはどれか。", ["必ず実行時型チェックされる", "可読性向上や静的解析に使う", "コンパイルを高速化する", "例外を無効化する"], 1, "型ヒントは主に補助情報で、実行時強制はされない。"),
        ("例外を発生させる文はどれか。", ["throw", "raise", "except", "error"], 1, "例外送出は raise。"),
        ("モジュールを別名で読み込む構文はどれか。", ["import numpy as np", "using numpy np", "load numpy as np", "module numpy -> np"], 0, "import ... as ... で別名を付ける。"),
    ]
    return make_questions("py_syn", items)


def build_data():
    items = [
        ("listの末尾に要素を追加するメソッドはどれか。", ["add", "append", "push", "insert_last"], 1, "append は末尾追加。"),
        ("list.insert(i, x)の説明として正しいものはどれか。", ["末尾追加", "位置iに挿入", "要素xを削除", "すべて置換"], 1, "insert は指定位置へ挿入する。"),
        ("list.pop()の既定の動作はどれか。", ["先頭を削除して返す", "末尾を削除して返す", "全要素削除", "削除のみで返さない"], 1, "引数なし pop は末尾要素を返して削除する。"),
        ("タプルの特徴として適切なものはどれか。", ["要素の追加削除が自由", "変更可能な可変型", "不変(イミュータブル)である", "キーと値を持つ"], 2, "タプルは不変オブジェクト。"),
        ("dictでキーの存在を確認する式はどれか。", ["key in d", "d.has(key)", "contains(d,key)", "exists key d"], 0, "in 演算子でキー存在を判定する。"),
        ("d.get('k', 0)の動作として正しいものはどれか。", ["kを削除する", "kがなければ0を返す", "kを追加する", "辞書を初期化する"], 1, "get は未存在時の既定値を指定できる。"),
        ("set型の特徴として適切なものはどれか。", ["順序を保持する", "重複要素を許す", "重複を許さない", "キーと値を持つ"], 2, "setは重複を持たない集合。"),
        ("集合A,Bの共通部分を求める演算子はどれか。", ["|", "&", "^", "-"], 1, "共通部分は &。"),
        ("文字列s[2:5]の意味として正しいものはどれか。", ["2文字目のみ", "2以上5未満の部分文字列", "5から2まで逆順", "2文字削除"], 1, "スライスは終端を含まない。"),
        ("s[-1]で取得される要素はどれか。", ["先頭", "2番目", "末尾", "長さ"], 2, "負の添字 -1 は末尾。"),
        ("copy.copyの説明として正しいものはどれか。", ["深いコピー", "浅いコピー", "参照渡しのみ", "型変換"], 1, "copy.copy は浅いコピーを作る。"),
        ("copy.deepcopyが必要になりやすい場面はどれか。", ["整数だけをコピー", "入れ子の可変オブジェクトを独立複製", "文字列比較", "四則演算"], 1, "内側のオブジェクトまで複製するには deepcopy を使う。"),
        ("list.sort()とsorted(list)の違いとして適切なものはどれか。", ["どちらも新規リストを返す", "sortは破壊的、sortedは新規を返す", "sortは文字列専用", "sortedは辞書専用"], 1, "sort は元リストを並べ替える。"),
        ("sorted(data, key=len)の意味はどれか。", ["長さを削除する", "要素長を基準に並べ替える", "辞書キーのみ並べる", "逆順固定"], 1, "key に評価関数を渡せる。"),
        ("collections.Counterの主な用途はどれか。", ["出現回数集計", "要素削除", "ファイル圧縮", "日付計算"], 0, "Counter は頻度集計に使う。"),
        ("dequeの特徴として適切なものはどれか。", ["両端操作が高速", "辞書専用", "重複不可", "自動ソート"], 0, "deque は先頭末尾の追加削除に強い。"),
        ("namedtupleの利点として適切なものはどれか。", ["添字のみでアクセスする", "フィールド名で読みやすく扱える", "JSON専用型", "常に可変"], 1, "属性名で参照できる軽量タプル。"),
        ("dataclassの主な効果はどれか。", ["SQL生成", "__init__等の定型コードを自動生成", "例外無効化", "暗号化"], 1, "データ保持クラスの定型記述を減らせる。"),
        ("辞書内包表記として正しいものはどれか。", ["{k:v for k,v in pairs}", "[k:v for k,v in pairs]", "{for k,v in pairs: k:v}", "(k:v for k,v in pairs)"], 0, "辞書内包は {key:value for ...}。"),
        ("set内包表記として正しいものはどれか。", ["{x*x for x in nums}", "[x*x for x in nums]", "(x*x for x in nums)", "{x:x*x for x in nums}"], 0, "set は波括弧で値のみを並べる。"),
        ("ジェネレータ式の特徴として適切なものはどれか。", ["必ず即時に全要素を生成", "遅延評価で順次生成", "forで使えない", "listより常に高速"], 1, "必要時に値を生成するためメモリ効率が良い。"),
        ("itertools.zip_longestが属するモジュールはどれか。", ["collections", "itertools", "functools", "operator"], 1, "zip_longest は itertools。"),
        ("range(1, 10, 3)の結果はどれか。", ["1,4,7", "1,3,6,9", "0,3,6,9", "1,4,7,10"], 0, "開始1、終了10未満、刻み3。"),
        ("list.extend(iterable)の効果はどれか。", ["iterableを1要素として追加", "要素を展開して末尾に追加", "先頭挿入", "重複削除"], 1, "extend は反復可能要素を展開追加する。"),
        ("dict.items()が返すものはどれか。", ["キーのみ", "値のみ", "(キー,値)ペア", "辞書コピー"], 2, "items はキーと値の組を返す。"),
        ("setdefaultの説明として適切なものはどれか。", ["未存在キーに既定値を入れて値を返す", "必ず削除する", "辞書をソートする", "型変換する"], 0, "キーがなければ既定値で作成し、その値を返す。"),
        ("list.remove(x)の動作として正しいものはどれか。", ["添字xを削除", "値xと一致する最初の要素を削除", "末尾を削除", "全一致削除"], 1, "remove は値指定、pop は添字指定。"),
        ("defaultdict(int)の初期値として正しいものはどれか。", ["None", "0", "空文字", "空リスト"], 1, "int() の既定値は 0。"),
        ("frozensetの特徴として適切なものはどれか。", ["変更可能な集合", "不変の集合", "重複許可", "順序保持"], 1, "frozenset は不変でハッシュ可能。"),
        ("bisectモジュールの用途として適切なものはどれか。", ["正規表現", "整列済みリストへの挿入位置探索", "JSON処理", "日付処理"], 1, "二分探索で挿入位置を求める。"),
    ]
    return make_questions("py_dat", items)


def build_oop():
    items = [
        ("クラス定義の開始キーワードはどれか。", ["class", "struct", "type", "object"], 0, "クラス定義は class で始める。"),
        ("インスタンスメソッド第1引数の慣習名はどれか。", ["this", "self", "me", "obj"], 1, "Pythonでは self が慣習。"),
        ("コンストラクタとして呼ばれるメソッドはどれか。", ["__new__", "__init__", "init", "constructor"], 1, "初期化処理は __init__。"),
        ("文字列表現を返す特殊メソッドはどれか。", ["__print__", "__str__", "__reprs__", "__text__"], 1, "人間向けの表現は __str__。"),
        ("開発者向けの再現可能表現に使うのはどれか。", ["__repr__", "__str__", "__format__", "__dump__"], 0, "__repr__ はデバッグ向け表現。"),
        ("継承を表す書き方として正しいものはどれか。", ["class Child extends Parent:", "class Child(Parent):", "class Child <- Parent:", "inherit Child(Parent):"], 1, "基底クラスは括弧内に書く。"),
        ("親クラスのメソッド呼出しに使う関数はどれか。", ["parent()", "super()", "base()", "root()"], 1, "super() でMROに従って親実装を呼ぶ。"),
        ("カプセル化の説明として適切なものはどれか。", ["すべて公開する", "内部実装を隠し公開インタフェース経由で操作する", "継承を禁止する", "型を固定する"], 1, "利用者は公開メソッドを通して操作する。"),
        ("名前修飾(マングリング)が起きる命名はどれか。", ["_x", "__x", "x__", "___x___"], 1, "先頭二重アンダースコアは _ClassName__x に変換される。"),
        ("プロパティを定義するデコレータはどれか。", ["@property", "@getter", "@field", "@accessor"], 0, "@property でメソッドを属性風に使える。"),
        ("classmethodの第1引数として渡るものはどれか。", ["self", "cls", "obj", "module"], 1, "クラス自身が cls に渡る。"),
        ("staticmethodの特徴として正しいものはどれか。", ["selfが必須", "clsが必須", "self/clsを自動で受け取らない", "継承不可"], 2, "ユーティリティ関数的に使える。"),
        ("抽象基底クラスで抽象メソッドを作るデコレータはどれか。", ["@abstract", "@abc", "@abstractmethod", "@virtual"], 2, "abcモジュールの @abstractmethod を使う。"),
        ("多態性(ポリモーフィズム)の説明として適切なものはどれか。", ["同名操作が型ごとに異なる振る舞いをする", "常に同じ実装を使う", "継承しない", "関数を使わない"], 0, "共通インタフェースで複数型を扱える。"),
        ("メソッドオーバーライドの説明として正しいものはどれか。", ["同名メソッドを子クラスで再定義", "関数名変更", "引数を削除", "モジュール分割"], 0, "子クラス側で振る舞いを差し替える。"),
        ("ダックタイピングの考え方として適切なものはどれか。", ["型名一致が必須", "必要なメソッドを持てば利用可能", "継承関係が必須", "ジェネリクス必須"], 1, "振る舞い重視で利用可否を判断する。"),
        ("MROが関係するのはどの場面か。", ["ファイルI/O", "多重継承時のメソッド探索順", "整数演算", "例外処理"], 1, "Method Resolution Order で探索順が決まる。"),
        ("データクラスで不変オブジェクト化する指定はどれか。", ["frozen=True", "immutable=True", "const=True", "final=True"], 0, "@dataclass(frozen=True) で再代入を防ぎやすくする。"),
        ("__slots__の主な効果はどれか。", ["必ず高速化", "属性名を固定しメモリ削減に寄与", "継承禁止", "例外無効化"], 1, "不要な __dict__ を持たせない設計ができる。"),
        ("演算子オーバーロードで加算に対応する特殊メソッドはどれか。", ["__sum__", "__add__", "__plus__", "__calc__"], 1, "+ 演算子は __add__ を呼ぶ。"),
        ("比較演算<に対応する特殊メソッドはどれか。", ["__cmp__", "__lt__", "__less__", "__low__"], 1, "< は __lt__。"),
        ("インスタンスが呼び出し可能になる特殊メソッドはどれか。", ["__run__", "__call__", "__invoke__", "__exec__"], 1, "__call__ 実装で obj() が可能。"),
        ("__iter__で返すべきものはどれか。", ["リスト", "文字列", "イテレータ", "整数"], 2, "反復プロトコルではイテレータを返す。"),
        ("__next__が送出すべき終了例外はどれか。", ["EOFError", "StopIteration", "RuntimeError", "ValueError"], 1, "反復終了は StopIteration。"),
        ("例外クラスの作成として適切なものはどれか。", ["class MyErr(object):", "class MyErr(Exception):", "def MyErr(Exception):", "exception MyErr:"], 1, "独自例外は Exception かその派生を継承する。"),
        ("mix-inクラスの狙いとして適切なものはどれか。", ["単一責務の機能を横断的に追加", "巨大クラスを作る", "I/O専用にする", "継承を減らせない"], 0, "再利用しやすい小さな機能単位を合成する。"),
        ("isinstance(obj, C)の目的はどれか。", ["同一性判定", "型・継承関係の判定", "等価比較", "属性追加"], 1, "継承を含めてインスタンス判定する。"),
        ("hasattr(obj, 'name')の意味はどれか。", ["属性nameが存在するか確認", "属性nameを削除", "属性nameを追加", "型を比較"], 0, "存在チェックに使う。"),
        ("getattr(obj, 'x', 0)の説明として正しいものはどれか。", ["必ず0を返す", "xが無ければ0を返す", "xを削除する", "xを追加する"], 1, "第3引数は未存在時の既定値。"),
        ("setattr(obj, 'x', 1)の効果はどれか。", ["属性xを取得", "属性xに1を設定", "属性xを削除", "属性xを比較"], 1, "動的に属性値を設定できる。"),
    ]
    return make_questions("py_oop", items)


def build_lib():
    items = [
        ("日付時刻を扱う標準ライブラリはどれか。", ["datetime", "timelib", "calendarx", "clock"], 0, "datetime が基本。"),
        ("JSON文字列をPythonオブジェクトへ変換する関数はどれか。", ["json.dump", "json.loads", "json.load", "json.dumps"], 1, "loads は文字列入力。"),
        ("PythonオブジェクトをJSON文字列にする関数はどれか。", ["json.dump", "json.loads", "json.load", "json.dumps"], 3, "dumps は文字列出力。"),
        ("正規表現検索に使う標準モジュールはどれか。", ["regex", "re", "pattern", "regexp"], 1, "標準は re。"),
        ("ファイルパスをオブジェクト指向で扱うモジュールはどれか。", ["os.path", "pathlib", "filepath", "dirlib"], 1, "pathlib.Path で操作できる。"),
        ("コマンドライン引数解析に使う標準モジュールはどれか。", ["getopt2", "argparse", "cli", "params"], 1, "argparse が標準。"),
        ("CSV読み書きに使う標準モジュールはどれか。", ["csv", "table", "spread", "sheet"], 0, "csv モジュールを使う。"),
        ("ハッシュ計算に使う標準モジュールはどれか。", ["digest", "crypto", "hashlib", "checksum"], 2, "SHA-256等は hashlib。"),
        ("Base64エンコードに使う標準モジュールはどれか。", ["binascii", "base64", "codec64", "ascii64"], 1, "base64 が基本。"),
        ("一時ファイル生成に使う標準モジュールはどれか。", ["tmp", "temp", "tempfile", "scratch"], 2, "tempfile で安全に作成する。"),
        ("ログ出力をレベル管理する標準モジュールはどれか。", ["trace", "logging", "logger", "syslogx"], 1, "logging はINFO/ERROR等を扱える。"),
        ("itertools.product(A,B)の意味はどれか。", ["共通部分", "直積(全組合せ)", "差集合", "重複削除"], 1, "全組合せを生成する。"),
        ("itertools.chain(a,b)の用途はどれか。", ["和集合", "複数イテラブルの連結", "並列化", "辞書化"], 1, "順に要素を取り出せる。"),
        ("functools.partialの主な用途はどれか。", ["一部引数を固定した関数を作る", "関数を削除", "例外を隠す", "並列実行"], 0, "同じ引数を何度も渡す場面で有用。"),
        ("functools.lru_cacheの効果として適切なものはどれか。", ["ログ保存", "関数結果のキャッシュ", "型検査", "並べ替え"], 1, "同一入力の再計算を抑える。"),
        ("operator.itemgetter(1)の主な用途はどれか。", ["要素削除", "添字1の要素を取り出す関数生成", "型変換", "和集合"], 1, "sortedのkey等で使える。"),
        ("decimal.Decimalを使う理由として適切なものはどれか。", ["速度最優先", "10進小数の誤差を抑えた計算", "文字列比較", "画像処理"], 1, "金額計算などで有用。"),
        ("fractions.Fraction(1,3)の特徴はどれか。", ["浮動小数で保持", "有理数として厳密表現", "文字列化専用", "整数化する"], 1, "分数のまま演算できる。"),
        ("uuid.uuid4()の用途はどれか。", ["連番生成", "ランダムUUID生成", "日付作成", "暗号鍵生成"], 1, "識別子として衝突しにくい値を作れる。"),
        ("subprocess.runの主な用途はどれか。", ["HTTP通信", "外部コマンド実行", "画像表示", "DB接続"], 1, "シェルコマンドの実行制御に使う。"),
        ("glob('*.py')の説明として正しいものはどれか。", ["正規表現検索", "パターン一致するファイル一覧取得", "CSV解析", "圧縮"], 1, "ワイルドカードでファイル探索する。"),
        ("shutil.copy(src, dst)の効果はどれか。", ["移動する", "コピーする", "削除する", "圧縮する"], 1, "コピーして元ファイルは残る。"),
        ("os.environの用途はどれか。", ["時刻取得", "環境変数の参照・設定", "例外記録", "暗号化"], 1, "実行環境の設定値を扱う。"),
        ("urllib.parse.urlencodeの主用途はどれか。", ["HTML整形", "クエリ文字列生成", "TLS通信", "DNS解決"], 1, "辞書等からクエリを作る。"),
        ("pathlibで存在確認に使うメソッドはどれか。", ["exists()", "isthere()", "check()", "present()"], 0, "Path.exists()で存在確認できる。"),
        ("statistics.meanの説明として適切なものはどれか。", ["中央値", "平均値", "最頻値", "分散"], 1, "mean は算術平均。"),
        ("collections.defaultdict(list)の利点はどれか。", ["キー未存在時に空リストを自動生成", "重複禁止", "順序固定", "型固定"], 0, "初期化コードを簡潔にできる。"),
        ("heapq.heappush/heappopの用途はどれか。", ["連結リスト", "ヒープ(優先度付きキュー)", "正規表現", "JSON"], 1, "最小要素を効率よく取り出せる。"),
        ("random.sample(pop, k)の説明として正しいものはどれか。", ["重複あり抽出", "重複なし抽出", "常に先頭k件", "常に同一結果"], 1, "sampleは重複なし抽出。"),
        ("typing.Optional[int]の意味はどれか。", ["intのみ", "intまたはNone", "Noneのみ", "任意型"], 1, "Optional[T]は T | None を表す。"),
    ]
    return make_questions("py_lib", items)


def build_io():
    items = [
        ("テキストファイルを読み取り専用で開くモードはどれか。", ["w", "a", "r", "x"], 2, "r は読み取り専用。"),
        ("追記モードはどれか。", ["w", "a", "r+", "x"], 1, "a は末尾へ追記する。"),
        ("with open(...)を使う利点はどれか。", ["速度向上のみ", "自動でcloseされる", "エラー無効化", "常に書込専用"], 1, "コンテキスト終了時にクローズされる。"),
        ("UTF-8を指定して開く書き方はどれか。", ["open(p,'r',codec='utf8')", "open(p,'r',encoding='utf-8')", "open(p,'r',charset='utf-8')", "open(p,'r',utf8=True)"], 1, "encoding引数で文字コードを指定する。"),
        ("readline()の動作として適切なものはどれか。", ["全行読み込む", "1行ずつ読み込む", "1文字読む", "末尾に追記"], 1, "readlineは1行取得。"),
        ("readlines()の戻り値はどれか。", ["文字列1つ", "行文字列のリスト", "整数", "辞書"], 1, "各行を要素とするリスト。"),
        ("バイナリ書込モードはどれか。", ["wb", "wt", "rb", "ab+"], 0, "wb はバイナリ書込み。"),
        ("jsonファイルを読み込む関数はどれか。", ["json.dump", "json.loads", "json.load", "json.dumps"], 2, "load はファイルオブジェクトから読む。"),
        ("json.dump(obj, f)の説明として正しいものはどれか。", ["JSON文字列を返す", "ファイルへJSONとして書き出す", "ファイル削除", "辞書作成"], 1, "dumpはファイルへ出力する。"),
        ("例外捕捉の構文として正しいものはどれか。", ["catch ValueError:", "except ValueError:", "rescue ValueError:", "error ValueError:"], 1, "except で捕捉する。"),
        ("finally節の役割として適切なものはどれか。", ["例外時のみ実行", "成功時のみ実行", "成否に関わらず後始末を実行", "任意で無視"], 2, "クリーンアップ処理を置く。"),
        ("例外を明示的に送出する文はどれか。", ["raise", "throw", "except", "error"], 0, "raiseで例外を発生させる。"),
        ("except Exception as e の e は何を表すか。", ["ファイル名", "捕捉した例外オブジェクト", "関数名", "行番号"], 1, "例外情報を参照できる。"),
        ("複数例外をまとめて捕捉する正しい書式はどれか。", ["except ValueError, TypeError:", "except (ValueError, TypeError):", "except [ValueError, TypeError]:", "except ValueError|TypeError:"], 1, "タプルで指定する。"),
        ("存在確認してから削除する安全な書き方はどれか。", ["os.remove(path)", "if os.path.exists(path): os.remove(path)", "delete(path)", "path.unlink(force=True)"], 1, "存在しない場合の例外を避けやすい。"),
        ("pathlibでファイルを削除するメソッドはどれか。", ["remove", "delete", "unlink", "erase"], 2, "Path.unlink() を使う。"),
        ("WindowsでCSV書込み時に空行問題を避ける指定はどれか。", ["encoding='utf-8'", "newline=''", "mode='rb'", "dialect='unix'"], 1, "open時に newline='' を指定する。"),
        ("標準入力から1行受け取る関数はどれか。", ["read", "scan", "input", "gets"], 2, "input() が標準入力を読む。"),
        ("標準エラー出力へ出す書き方はどれか。", ["print(msg, file=sys.stderr)", "print.stderr(msg)", "stderr.print(msg)", "sys.error(msg)"], 0, "printのfile引数で切替える。"),
        ("logging.exception()の特徴として適切なものはどれか。", ["例外情報付きでログ出力", "例外を無効化", "ログ削除", "DEBUG固定"], 0, "トレースバック情報を含めて記録する。"),
        ("unittestでテストケース基底クラスはどれか。", ["unittest.Test", "unittest.Case", "unittest.TestCase", "unittest.BaseCase"], 2, "TestCase を継承してテストを書く。"),
        ("unittestで等価比較に使うメソッドはどれか。", ["assertEqual", "assertSame", "assertEq", "assertIdentity"], 0, "期待値と実測値の比較に使う。"),
        ("指定例外の発生を検証する書き方はどれか。", ["with self.assertRaise(...):", "with self.assertRaises(...):", "with self.raises(...):", "with raise.assert(...):"], 1, "assertRaisesをコンテキストで使う。"),
        ("contextlib.suppress(FileNotFoundError)の用途はどれか。", ["すべての例外を隠す", "対象例外のみ握りつぶして続行", "ログを止める", "強制終了"], 1, "特定例外だけ無視したいときに使う。"),
        ("shutil.move(src, dst)の説明として正しいものはどれか。", ["コピーのみ", "移動する", "圧縮する", "暗号化する"], 1, "ファイル/ディレクトリを移動する。"),
        ("pickle利用時の注意として適切なものはどれか。", ["常に安全", "信頼できないデータは読み込まない", "JSONより可読性が高い", "文字列専用"], 1, "任意コード実行リスクがあるため入力元を限定する。"),
        ("TemporaryDirectory()の利点はどれか。", ["常に永続化", "終了時に自動削除", "Windows専用", "圧縮専用"], 1, "with終了で一時ディレクトリを片付ける。"),
        ("open(..., 'x')の意味はどれか。", ["追記", "新規作成専用(存在時エラー)", "読取専用", "バイナリ専用"], 1, "既存ファイルを誤上書きしにくい。"),
        ("バッファを明示的に書き出すメソッドはどれか。", ["flush", "commit", "sync", "save"], 0, "flushでバッファ内容を出力先へ送る。"),
        ("トランザクション的に安全に更新する方針として適切なものはどれか。", ["直接上書きのみ", "一時ファイルへ書いてから置換", "失敗時は無視", "読み取り専用で開く"], 1, "中断時の破損リスクを減らせる。"),
    ]
    return make_questions("py_io", items)


def write_file(path: Path, genre: str, questions):
    payload = {"genre": genre, "exam": "Python試験", "questions": questions}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def update_genres():
    p = Path("data/genres.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    programming = next((s for s in data.get("subjects", []) if s.get("id") == "programming"), None)
    if not programming:
        return
    py = next((e for e in programming.get("exams", []) if e.get("id") == "lang_python"), None)
    if not py:
        return
    for sec in py.get("sections", []):
        sec["count"] = 30
        sec["coming_soon"] = False
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    syntax = build_syntax()
    data_q = build_data()
    oop = build_oop()
    lib = build_lib()
    io = build_io()

    write_file(Path("data/lang/questions_python_syntax.json"), "Python基礎文法", syntax)
    write_file(Path("data/lang/questions_python_data.json"), "コレクションとデータ構造", data_q)
    write_file(Path("data/lang/questions_python_oop.json"), "クラスとオブジェクト指向", oop)
    write_file(Path("data/lang/questions_python_lib.json"), "標準ライブラリ", lib)
    write_file(Path("data/lang/questions_python_io.json"), "ファイル・例外・テスト", io)
    update_genres()

    print("generated:", len(syntax), len(data_q), len(oop), len(lib), len(io))


if __name__ == "__main__":
    main()
