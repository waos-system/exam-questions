# Linux システム管理と監視：ベストプラクティス研究ガイド

## 1.概要（Executive Summary）

本ガイドは、LPIC-1/2 および Linux システム管理認定資格における推奨実践(ベストプラクティス)をまとめたものです。システム管理者が効率的にシステムをモニタリングし、パフォーマンスを最適化するための実践的な知識を提供します。

---

## 2. ログファイル管理（Log File Management）

### 2.1 標準的なログ構造

Linux システムのログファイルは `/var/log` ディレクトリ配下に集約されます：

```
/var/log/
├── syslog              # 汎用システムログ（Debian/Ubuntu）
├── messages            # 汎用システムログ（RHEL/CentOS）
├── auth.log            # 認証関連ログ
├── kernel.log          # カーネル関連ログ（dmesg）
├── cron                # cron ジョブ実行ログ
├── secure              # セキュリティログ（RHEL系）
├── audit/              # auditd ログ
├── journal/            # systemd journald ログ（journal ストレージ）
└── [application]/      # 各アプリケーション固有ログ
```

**関連LPIC出題:** logファイル位置の選択問題、各ログの目的把握

### 2.2 syslog と rsyslog の違い

| 特性 | syslog | rsyslog |
|------|--------|---------|
| 世代 | 従来型（古い） | 次世代（モダン） |
| 機能 | 基本的なログ収集 | 複数出力、テンプレート機能 |
| パフォーマンス | 低速 | 高速 |
| モジュール性 | なし | あり（loadmodule） |
| リモート転送 | TCP/UDP | TLS対応 |
| 設定ファイル | /etc/syslog.conf | /etc/rsyslog.conf |

### 2.3 journalctl の利用と syslog との連携

systemd の journalctl は `/run/log/journal/` または `/var/log/journal/` に JSON形式でログを保存します：

**重要なjournalctlコマンド:**

```bash
# 最新100行表示
journalctl -n 100

# 特定サービスのログ
journalctl -u nginx -n 50

# エラーレベルのみ表示
journalctl -p err

# 日時範囲指定
journalctl --since "2024-01-01" --until "2024-01-31"

# リアルタイム監視（tail -f の代わり）
journalctl -f

# JSON形式で出力
journalctl -o json

# 起動制御（persistent storage有効化）
journalctl --flush  # メモリからディスクへ

# バイナリログサイズと保有期限の確認
journalctl --disk-usage
```

**rsyslog と journalctl の連携:**
- rsyslog は journalctl のログを吸い上げて `/var/log/syslog` に書き込み可能
- 従来型ツール互換性が必要な場合に有効

### 2.4 リモートログサーバーの構築

**rsyslog でのリモートログ転送設定例 (`/etc/rsyslog.conf`):**

```conf
# RFC 3164形式の UDP転送（セキュリティ低）
*.* @192.168.1.100:514

# RFC 5424形式の TCP転送
*.* @@192.168.1.100:514

# TLS暗号化転送（セキュリティ高）
# モジュール読み込み
module(load="imtcp")
module(load="omtls")

# TLS設定
action(type="omfwd" protocol="tcp" target="192.168.1.100" port="6514"
  streamDriver="gtls"
  streamDriverMode="1"
  streamDriverAuthMode="x509/name"
  permittedPeer="logserver.example.com"
)
```

---

## 3. ログローテーション（Log Rotation）

### 3.1 logrotate の基本概念

logrotate は定期的なログファイル分割・圧縮・削除を自動化します。

**設定ファイル構成:**
- メイン設定: `/etc/logrotate.conf`
- 個別設定: `/etc/logrotate.d/` ディレクトリ

### 3.2 logrotate 設定のベストプラクティス

```bash
/var/log/example.log {
    daily                    # 1日単位でローテーション
    rotate 7                 # 7世代保持
    compress                 # gzip圧縮
    delaycompress            # 次回ローテ時に圧縮（ホットログアクセス対策）
    missingok                # ファイル欠落時もエラーにしない
    notifempty               # 空ファイルはローテーション対象外
    create 0640 www-data adm # 新ファイルのパーミッションと所有者
    sharedscripts            # postrotate/prerotate を1度だけ実行
    postrotate
        systemctl reload rsyslog > /dev/null 2>&1 || true
    endscript
}
```

### 3.3 ローテーション頻度の選択

| 設定 | 用途 |
|------|------|
| hourly | アクセスログなど高頻度生成 |
| daily | 一般的なシステムログ |
| weekly | ログ生成量が少ない環境 |
| monthly | アーカイブ目的のみ |

### 3.4 logrotate の手動実行とテスト

```bash
# テスト実行（実際には実行しない）
logrotate -d /etc/logrotate.conf

# 強制実行
logrotate -f /etc/logrotate.conf

# トラブルシューティング
logrotate -v /etc/logrotate.conf  # verbose出力
```

---

## 4. パフォーマンスモニタリングツール

### 4.1 top / htop コマンド

**top のメモリ関連フィールド解説:**

```
VIRT = 仮想メモリ総量(プロセスが要求)
RES  = 物理メモリ使用量(実際に使用)
SHR  = 共有メモリ量(複数プロセスで共有)
%MEM = メモリ使用率(RES/総メモリ)
```

**top のインタラクティブ機能:**
```
Shift + O    # ソート順序変更（メモリ使用率別など）
1            # CPU別表示
V            # 프로세스 트리 표시
u            # ユーザー単位フィルタ
k            # プロセス Kill
r            # nice値変更
W            # 設定ファイル保存
```

### 4.2 iostat - ディスク I/O 統計

**重要なオプション:**

```bash
# ディスク詳細統計（重要）
iostat -x 1 5

# CPU統計を含める
iostat -c 1 5

# デバイス選んで表示
iostat -x sda 1 5
```

**重要なフィールド:**

| フィールド | 意味 | 閾値/注目点 |
|-----------|------|-----------|
| r/s, w/s | 読み書き要求/秒 | I/O量の指標 |
| rMB/s, wMB/s | 読み書きスループット | バンド幅利用率 |
| rrqm/s, wrqm/s | マージされた要求/秒 | I/O効率 |
| r_await, w_await | 平均遅延(ms) | **低いほど良い**（1-5ms理想） |
| svctm | **非推奨** | 古い指標、信頼性低 |
| %util | デバイス利用率 | **100%で飽和** |
| avgqu-sz | 平均キュー長 | **高いと待機多い** |

### 4.3 vmstat - 仮想メモリ統計

**基本実行:**
```bash
vmstat 1 10  # 1秒間隔で10回表示
```

**フィールド解説:**

```
r   # CPU実行待ちプロセス数（CPUコア数以下が正常）
b   # I/O待機プロセス数（大きいと過負荷）
in  # 割り込み/秒（高いとシステムコール量多）
cs  # コンテキストスイッチ/秒（高いと負荷高）
```

### 4.4 sar - 詳細統計収集（sysstat パッケージ）

**ベストプラクティス:**

```bash
# CPU使用率推移（過去からリアルタイム）
sar -u 1 5

# ディスク I/O統計
sar -d 1 5

# メモリ・スワップ
sar -r 1 5

# ネットワーク統計
sar -n DEV 1 5

# 指定日付データ取得
sar -u -f /var/log/sa/sa24
```

---

## 5. メモリパフォーマンスチューニング

### 5.1 メモリ構成の理解

```
/proc/meminfo の重要なフィールド:

MemTotal     # 物理メモリ総量
MemFree      # 直後に利用可能
MemAvailable # 実際に利用可能(キャッシュ含)
Buffers      # ディスク読み書みバッファ
Cached       # ページキャッシュ量
Dirty        # ディスクに未書き込みデータ
Swap*        # スワップメモリ統計
```

**重要: MemAvailable と MemFree の違い**

- `MemFree`: 全く使用されていないメモリ
- `MemAvailable`: キャッシュ削除で即座に利用可能なメモリ（より実用的）

### 5.2 メモリ圧力の診断と対策

```bash
# キャッシュ汚れダッシュボード
watch -n 1 'free -h && echo "---" && cat /proc/meminfo | grep -E "Dirty|Writeback"'

# キャッシュ削除（計測前クリーニング）
sync
echo 3 > /proc/sys/vm/drop_caches

# swappiness チューニング（0:swap極力使わない, 100:積極利用）
sysctl vm.swappiness=10  # デフォルト 60
echo "vm.swappiness=10" >> /etc/sysctl.conf
sysctl -p
```

### 5.3 OOMKiller と メモリ不足対策

```bash
# OOMシコアス確認
dmesg | tail | grep -i "oom\|killed"

# プロセスのメモリ上限設定
ulimit -v 1000000  # 仮想メモリ上限 (KB単位で1GB)

# cgroup v2 によるメモリ制限
echo "memory.max=1G" > /sys/fs/cgroup/test/memory.max
```

### 5.4 NUMA システムでのメモリ最適化

```bash
# NUMA情報確認
numactl --hardware

# ノード指定実行
numactl --physcpubind=0 --localalloc ./application

# メモリポリシー統計確認
numastat

# ノード間メモリマイグレーション（自動調整）
sysctl kernel.numa_balancing=1
```

---

## 6. CPU パフォーマンスチューニング

### 6.1 CPU アーキテクチャ確認

```bash
# 基本情報
lscpu

# プロセッサ数
nproc

# CPU キャッシュ階層構造
lstopo  # /libnuma-dev パッケージ必要

# ハイパースレッド確認
grep -i "sibling\|core id" /proc/cpuinfo
```

### 6.2 CPU Affinity（プロセス親和性）設定

```bash
# 特定CPU(0番)でプロセス実行
taskset -c 0 ./application

# 実行中プロセスのaffinity変更
taskset -c 0-2 -p PID

# 確認
taskset -c -p PID
ps -o psr PID  # PSR は対象CPU番号
```

### 6.3 プロセススケジューリングポリシー

```bash
# スケジューリングポリシー確認
chrt -p PID

# リアルタイムポリシー設定（root必須）
chrt -f 50 ./rt_app  # SCHED_FIFO Priority 50

# 標準ポリシーに戻す
chrt -o 0 -p PID  # SCHED_OTHER
```

**スケジューリングポリシー比較:**

| ポリシー | タイムスライス | 優先度 | 用途 |
|---------|---|---|---|
| SCHED_OTHER | あり | 0 | 通常アプリ |
| SCHED_BATCH | あり | 0 | バッチ処理 |
| SCHED_IDLE | あり | 0 | アイドル時のみ |
| SCHED_FIFO | なし | 1-99 | リアルタイム（ノンプリエンプティブ） |
| SCHED_RR | あり | 1-99 | リアルタイム（プリエンプティブ） |

### 6.4 パフォーマンスカウンタ測定（perf）

```bash
# インストール
apt-get install linux-tools-generic

# CPU キャッシュ miss 統計
perf stat ./application

# フレームグラフ生成
perf record -g ./application
perf script > out.perf
```

---

## 7. ディスク I/O チューニング

### 7.1 ディスク I/O スケジューラの選択

```bash
# 確認
cat /sys/block/sda/queue/scheduler
# 出力例: noop deadline [cfq]

# 変更（再起動で戻る）
echo deadline > /sys/block/sda/queue/scheduler

# 永続化
echo 'ACTION=="add|change", SUBSYSTEM=="block", ATTR{queue/scheduler}="deadline"' > /etc/udev/rules.d/99-io-scheduler.rules
```

**スケジューラ選択ガイダンス:**

| スケジューラ | 特性 | 推奨用途 |
|-----------|-----|--------|
| noop | シンプル（キューなし） | SSD、高速ストレージ |
| deadline | I/O公平性保証 | データベース、OLTP |
| cfq | フェアネス(デフォルト) | 汎用 |
| bfq | イオテクノロジチューニング | マルチタスクワークロード |
| kyber | レイテンシ最適化 | NVMe SSD |

### 7.2 ディスク I/O キューサイズという設定

```bash
# キュー長確認
cat /sys/block/sda/queue/nr_requests

# 増加させる（キャッシュ効果向上、レイテンシ増加可能性）
echo 1024 > /sys/block/sda/queue/nr_requests

# 永続化
echo 'ACTION=="add|change", SUBSYSTEM=="block", ATTR{queue/nr_requests}="1024"' > /etc/udev/rules.d/99-io-tunning.rules
```

### 7.3 ディスク I/O ベンチマーク

```bash
# fio インストール
apt-get install fio

# ランダム読み込みテスト
fio --name=random-read --ioengine=libaio --iodepth=32 --rw=randread --bs=4k --direct=1 --size=1G --numjobs=4 --runtime=60 --group_reporting --filename=/dev/sda3

# シーケンシャル書き込みテスト
fio --name=seq-write --ioengine=libaio --iodepth=32 --rw=write --bs=4k --direct=1 --size=1G --numjobs=4 --runtime=60 --filename=/dev/sda3
```

---

## 8. スケジューリング自動化

### 8.1 Cron の ベストプラクティス

**Crontab 形式の復習:**
```
分(0-59) 時(0-23) 日(1-31) 月(1-12) 曜日(0-6, 0=日)  コマンド
```

**実践例:**

```crontab
# 毎日午前3時にバックアップ
0 3 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1

# 毎月第1日曜日 午前2時
0 2 * * 0 [ $(date +%d) -le 07 ] && /usr/local/bin/monthly-task.sh

# 平日のみ 午前9時
0 9 * * 1-5 /usr/local/bin/workday-task.sh

# 15分間隔でチェック（*/15記法）
*/15 * * * * /usr/local/bin/check-status.sh

# 毎時間30分（:30）に実行
30 * * * * /usr/local/bin/hourly-task.sh
```

**Cron セキュリティ:**
```bash
# 許可ユーザー設定
echo "username" >> /etc/cron.allow

# ブラックリスト設定
echo "username" >> /etc/cron.deny

# crontab 実行ログ確認
grep CRON /var/log/auth.log
journalctl -u cron
```

### 8.2 systemd timer（モダン代替）

**systemd timer の構成:**

1. サービス定義 (`/etc/systemd/system/mytask.service`):
```ini
[Unit]
Description=My Periodic Task
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/mytask.sh
User=root
StandardOutput=journal
StandardError=journal
```

2. Timer 定義 (`/etc/systemd/system/mytask.timer`):
```ini
[Unit]
Description=Run MyTask every day at 3 AM
Requires=mytask.service

[Timer]
# OnCalendar フォーマット例
OnCalendar=*-*-* 03:00:00      # 毎日午前3時
OnCalendar=Mon-Fri *-*-* 09:00 # 平日午前9時
OnCalendar=*-*-01 03:00:00     # 毎月1日午前3時
OnTime=*-*-* 15:30:00          # 毎日15時30分
OnBootSec=1min                 # 起動後1分で実行
OnUnitActiveSec=2h             # 前回実行から2時間後

# ランダム遅延（負荷分散）
RandomizedDelaySec=5min

[Install]
WantedBy=timers.target
```

**systemd timer 運用:**
```bash
# Timer 有効化
systemctl enable mytask.timer
systemctl start mytask.timer

# 確認
systemctl list-timers
systemctl status mytask.timer

# 次回実行時刻確認
systemctl list-timers --all

# 実行ログ確認
journalctl -u mytask.service -n 20
```

**Cron vs systemd timer:**

| 観点 | Cron | systemd timer |
|-----|------|---|
| 学習曲線 | 低（シンプル） | 中（ini形式） |
| ログ統合 | syslog（別体系） | journalctl（統一） |
| 遅延通知 | なし | メール送信可能 |
| 環境変数 | crontab内で設定 | Unit内で統一 |
| パフォーマンス | 標準 | 若干低速 |
| 将来性 | 維持扱い | 推奨（systemd拡張） |

---

## 9. 統合的なシステム監視戦略

### 9.1 リアルタイム監修ダッシュボード構築例

```bash
#!/bin/bash
# monitor.sh - 統合監視スクリプト

while true; do
    clear
    echo "=== System Performance Monitor ==="
    echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    # CPU情報
    echo "=== CPU ==="
    top -bn1 | grep "Cpu(s)" | sed 's/.*, *\([0-9.]*\)%* id.*/\1/' | awk '{print "CPU Usage: " 100-$1 "%"}'

    # メモリ情報
    echo "=== Memory ==="
    free -h | grep ^Mem | awk '{print "Used: " $3 " / " $2}'

    # I/O情報
    echo "=== Disk I/O ==="
    iostat -dx 1 2 | tail -1 | awk '{print "%util: " $NF}'

    # プロセス情報
    echo "=== Top 5 CPU Processes ==="
    ps aux --sort=-%cpu | head -6 | tail -5 | awk '{printf "%-8s %5s%% %s\n", $1, $3, $11}'

    sleep 5
done
```

### 9.2 ログの中央集約（ELK Stack）

**最小構成例:**
```yaml
# docker-compose.yml
version: '3'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"

  kibana:
    image: docker.elastic.co/kibana/kibana:8.0.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.0.0
    volumes:
      - /var/log:/var/log:ro
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
    command: filebeat -e -strict.perms=false
```

**rsyslog → Elasticsearch 連携:**
```conf
# /etc/rsyslog.conf に追加
module(load="omelasticsearch")

action(
  type="omelasticsearch"
  server="localhost"
  serverport="9200"
  searchIndex="syslog-%asn%!YEAR!.%!MONTH!.%!DAY!"
  searchType="_doc"
  bulkmode="on"
  action.resumeretrycount="5"
)
```

---

## 10. トラブルシューティング実践ガイド

### 10.1 パフォーマンス劣化診断フロー

```
[パフォーマンス劣化報告]
    ↓
CPU使用率確認
├─ 高い(>80%) → top/htop で犯人プロセス特定
│   └─ perf stat でボトルネック分析
└─ 正常 → 次へ
    ↓
メモリ使用率確認
├─ 高い(>85%) → free -h で詳細確認
│   ├─ キャッシュ多い → drop_caches で検証
│   └─ 本当の使用 → メモリリーク疑い → valgrind
└─ 正常 → 次へ
    ↓
ディスク I/O確認
├─ %util高い → iostat -x でデバイス特定
│   └─ fio でベンチマーク、スケジューラ変更検討
└─ 正常 → 次へ
    ↓
ネットワーク確認
├─ 高遅延 → mtr, traceroute
└─ 帯域幅制限 → iftop, nethogs
```

### 10.2 メモリリーク検出例

```bash
# valgrind インストール
apt-get install valgrind

# 実行
valgrind --leak-check=full --show-leak-kinds=all ./your_program

# 出力例の解釈:
# "definitely lost" → 修正必須
# "indirectly lost" → 参照関係の破綻
# "possibly lost" → ポインタ喪失の可能性
```

### 10.3 システムコール追跡

```bash
# open()システムコール追跡
strace -e trace=open,read ls /tmp

# ファイルディスクリプタ追跡
strace -e trace=file ls /tmp

# 性能計測付き
strace -c ./your_program

# 出力統計の読み方:
# % time    : システムコール実行時間
# seconds   : 総実行時間
# usecs/call: 平均実行時間
```

---

## 11. セキュリティ監査との連携

### 11.1 auditd ロギング

```bash
# auditd インストール
apt-get install auditd audispd-plugins

# ルール例：ファイルシステム監視
auditctl -w /etc/passwd -p wa -k passwd_changes

# ユーザーアクション監視
auditctl -a exit,always -F arch=b64 -S execve -F key=exec

# 確認
ausearch -k passwd_changes
```

### 11.2 SELinux/AppArmor ログ

```bash
# SELinux (RHEL系)
ausearch -m AVC | head

# AppArmor (Debian系)
grep apparmor /var/log/syslog
```

---

## 12. ベストプラクティスチェックリスト

### 監視運用チェックリスト

- [ ] ログローテーション設定確認 (logrotate が正常に動作)
- [ ] ログ一元収集構築 (リモートログサーバーまたはELK)
- [ ] ディスク容量監視 (警告閾値70%, 危機80%)
- [ ] メモリ圧力監視 (OOMKiller発生検知)
- [ ] CPU使用率監視 (トレンド分析で異常検知)
- [ ] I/O遅延監視 (r_await, w_await)
- [ ] zombie プロセス検知 (定期スクリプト)
- [ ] クリティカルサービス availability確保
- [ ] 定期的なパフォーマンステスト (fioベンチマーク)
- [ ] ログローテーション後アプリ再起動自動化

### セキュリティモニタリングチェックリスト

- [ ] 認証失敗ログ監視 (brute force 検知)
- [ ] sudo 実行ログ監視
- [ ] sshd アクセス ログ監視
- [ ] ファイル改ざん検知 (auditd)
- [ ] 定期的なログレビュー実施
- [ ] ウイルススキャンログ監視
- [ ] SELinux/AppArmor Policy violation監視

---

## 参考資料

1. LPIC-1 認定教科書（英語版 & 日本語翻訳版）
2. LPIC-2 認定教科書 - Linux システム管理
3. Linux Kernel Documentation
   - `/proc` ファイルシステム
   - `/sys` デバイスツリー
4. Red Hat: System Administrator's Guide
5. Ubuntu Server Guide
6. The Linux Performance: Tools & Techniques
   (Brendan Gregg)

---

## まとめ

Linux システム管理と監視の成功には以下が重要です：

1. **予防的監視**: 問題が発生する前の早期検知
2. **層状戦略**: ローカル監視 + 一元集約の組み合わせ
3. **自動化**: cron/systemd timer による定期タスク自動実行
4. **ドキュメント化**: アラート条件・対応手順の明文化
5. **継続的改善**: パフォーマンス測定に基づくチューニング

これらの実践により、安定で高性能なLinuxシステム運用が実現できます。

---

**最終更新:** 2024年2月
**対応資格:** LPIC-1 (101/102), LPIC-2 (201/202)
