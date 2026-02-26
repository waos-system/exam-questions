# Linux Storage Management & System Administration Exam Research Summary

## Overview
Comprehensive exam question sets for Linux storage management and system administration, based on LPIC-1 (101/102) and LPIC-2 (201/202) certification standards (2019-2024).

---

## Set 1: Storage Management (linux_storage_001 to linux_storage_050)
Genre: ストレージ管理 (Storage Management)
Exam: Linux

### Topics Covered

#### 1. **Disk Partitioning (Questions 001-010)**
- **fdisk Usage**: Basic MBR partitioning, partition management
- **parted Tool**: GPT partitioning for 2TB+ disks
- **gdisk**: Specialized GPT tool
- **MBR Limitations**: 2TB maximum size restriction
- **Partition Management**: Creating, deleting, modifying partitions

**Common Challenge**: Administrators often overlook MBR's 2TB limitation when initially provisioning large storage systems. Migration to GPT is necessary but requires careful planning.

#### 2. **Logical Volume Manager (LVM) (Questions 011-015)**
- **Architecture**: Physical Volumes (PV) → Volume Groups (VG) → Logical Volumes (LV)
- **Commands**:
  - `pvcreate`: Initialize physical volumes
  - `vgcreate`: Create volume groups
  - `lvcreate`: Create logical volumes
  - `pvdisplay/vgdisplay/lvdisplay`: View resources
- **Advantages**: Online capacity expansion, flexible storage allocation

**Common Challenge**: LVM adds abstraction layer complexity. Understanding the three-tier hierarchy is critical for troubleshooting. Many issues stem from improper PV/VG/LV planning during initial setup.

#### 3. **File Systems (Questions 016-022)**
- **ext4**: Journaling, 16TB file size support, widespread compatibility
- **XFS**: High throughput, optimal for large files (100GB+), COW-based snapshots, RAID optimized
- **Btrfs**: Advanced features (snapshots, multi-device, RAID built-in), relatively newer, potential stability concerns in production

**Common Challenge**: File system selection decisions often come too late in the project. XFS shows superior performance on large sequential I/O, but ext4's ubiquity makes it the default choice. Btrfs promises much but needs careful monitoring in production environments.

#### 4. **Mount Operations (Questions 023-025)**
- **mount/umount**: Device attachment and detachment
- **fstab Configuration**: Persistent mount configuration
- **Mount Options**: Performance tuning (noatime, relatime), permissions (ro, rw)
- **Busy Device Handling**: Using `fuser` and `lsof` for process identification

**Common Challenge**: "device is busy" errors are common after system updates or during maintenance windows. Understanding process-to-filesystem binding is essential.

#### 5. **File System Checking & Repair (Questions 026-030)**
- **fsck**: Consistency checking, repair operations
- **xfs_repair**: XFS specific repairs (must be unmounted)
- **e2fsck**: ext4 checks with various fix levels (-y, -f, -p)
- **Danger of Mounted FS**: Running fsck on mounted filesystems risks data corruption

**Common Challenge**: Administrators frequently attempt fsck on mounted filesystems during production hours, not realizing the requirement for unmount. This is a critical operational mistake.

#### 6. **Disk Quotas (Questions 031-033)**
- **usrquota/grpquota**: User and group limits
- **Soft vs Hard Limits**: Warning vs enforcement thresholds
- **edquota/repquota/quota**: Configuration and reporting
- **fstab Integration**: `usrquota,grpquota` options

**Common Challenge**: Quota implementation is often overlooked until storage costs spike. Soft limits provide warnings that users frequently ignore; hard limits cause application failures.

#### 7. **Backup and Restoration (Questions 034-038)**
- **tar**: Archive creation with compression options (-czf)
- **dd**: Block-level disk/partition copying with status monitoring
- **rsync**: Efficient file synchronization with deletion support (--delete flag)
- **Data Preservation**: Selection between full and incremental strategies

**Common Challenge**: The `--delete` flag in rsync is simultaneously powerful and dangerous. Accidental synchronization in wrong direction can wipe source data. Version control and dry-runs are critical pre-conditions.

#### 8. **RAID Concepts (Questions 039-041)**
- **RAID 0 (Striping)**: High speed, zero fault tolerance
- **RAID 1 (Mirroring)**: 50% capacity overhead, single fault tolerance
- **RAID 5 (Striped+Parity)**: Minimum 3 disks, 1-disk fault tolerance, (n-1)/n capacity
- **RAID 6**: Dual-parity, 2-disk fault tolerance
- **Rebuild Time**: Exponential risk during recovery windows

**Common Challenge**: RAID 6 adoption lag despite clear advantages. Many systems still operate RAID 5 with large disks where dual-disk failures are statistically likely. Rebuild windows (10-48 hours) create vulnerability windows.

#### 9. **Space and Inode Management (Questions 042-049)**
- **df**: Block-level disk usage (df -k, df -h, df -i)
- **du**: Directory-level usage aggregation (du -sh for summaries)
- **Inode Exhaustion**: Small files deplete inodes before disk capacity
- **Cache Effects**: Discrepancies between df and actual available space
- **Monitoring Tools**: blkid, lsblk, partprobe, smartctl

**Common Challenge**: Inode exhaustion is frequently misdiagnosed. Systems report "Disk full" with 50% capacity available due to inode depletion from temporary files or cache accumulation. Understanding `df -i` is essential.

#### 10. **Advanced Features (Question 050)**
- **LVM Snapshots**: Copy-on-Write for backup windows
- **ACL Support**: Beyond traditional unix permissions
- **SELinux Integration**: Security context management
- **Incremental Backups**: Timestamp-based change detection
- **RAID Rebuild Penalties**: I/O contention during recovery

**Common Challenge**: RAID rebuild performance degradation is predictable but often underestimated in capacity planning. 1-2MB sequential I/O reads across entire disk during rebuild causes 50%+ performance reduction for concurrent workloads.

---

## Set 2: System Administration and Monitoring (linux_sysadmin_001 to linux_sysadmin_050)
Genre: システム管理と監視 (System Administration and Monitoring)
Exam: Linux

### Topics Covered

#### 1. **Log Management (Questions 001-014)**
- **Log Locations**:
  - `/var/log/auth.log`: Authentication events
  - `/var/log/syslog` or `/var/log/messages`: General system messages
  - `/var/log/kern.log`: Kernel messages
  - `/var/log/dmesg`: Boot-time kernel messages
- **Viewing Tools**:
  - `dmesg`: Kernel ring buffer
  - `journalctl`: systemd journal with time/service filtering
  - `grep cron /var/log/syslog`: Task scheduler logs
- **rsyslog Configuration**: `/etc/rsyslog.conf` with template directives
- **Log Rotation**: `logrotate` with retention policies (rotate N)
- **Log Compression**: `compresscmd` for custom compression

**Common Challenge**: Log management decisions are often deferred until disk space crises. rsyslog configuration complexity means most systems use defaults, leading to excessive storage consumption. Log4j-style vulnerability scanning requires cross-log analysis skills.

#### 2. **Performance Monitoring Tools (Questions 015-025)**
- **top**: Real-time process monitoring
  - VIRT (virtual memory), RES (physical), SHR (shared)
  - PRI/NI (priority/niceness)
  - Load Average interpretation
- **htop**: Enhanced top with color and graphs
- **iostat -x**: Disk I/O statistics
  - avgqu-sz: Queue length (indicates saturation)
  - r_await/w_await: Read/write latency
- **vmstat**: Memory and process statistics
  - r (run queue): CPU-bound wait count
  - b (blocked): I/O-bound wait count
- **sar**: System Activity Reporter across time windows
  - `-u`: CPU breakdown (user%, nice%, system%, iowait%, idle%)
  - `-d`: Disk I/O metrics
- **mpstat**: Per-CPU statistics (NUMA/hyperthreading analysis)

**Common Challenge**: Most operators monitor CPU% and Memory% without understanding that high CPU% with low iowait% is completely different from high CPU% with high iowait%. This distinction determines whether the bottleneck is CPU-bound (add CPU) or I/O-bound (add storage or network).

#### 3. **Process Management Beyond Basics (Questions 026-037)**
- **nice/renice**: Priority adjustment (-20 to +19, lower = higher priority)
- **CPU Affinity**: `taskset` to bind processes to specific cores
- **Process States**: S(sleep), R(running), D(disk sleep), Z(zombie)
- **Zombie Process**: Child process exit not waited by parent (indicates parent process issue)
- **lsof -p PID**: File descriptor inspection
- **ps -o ppid**: Parent process ID tracking
- **Debugging Tools**:
  - `valgrind`: Memory leak detection
  - `strace`: System call tracing (file opens, network access)
- **Realtime Scheduling**: SCHED_FIFO for deterministic latency

**Common Challenge**: Zombie processes accumulate in long-running services with improper signal handling. They become noticeable only when file descriptor tables fill up (ulimit -n). Strace overhead (10-100x slowdown) makes production debugging risky.

#### 4. **Cron and systemd Scheduling (Questions 047-050)**
- **crontab Format**: minute hour day month weekday command
  - `0 3 1 * *`: Monthly 1st at 3am
  - `0 18 * * 5`: Friday at 6pm
- **systemd timer**: Alternative with two-part configuration
  - `.service` file: What to execute
  - `.timer` file: When to execute
  - `OnCalendar=*-*-* HH:MM:SS` (ISO8601)
- **Advantages of systemd**: Logging integration, systemd dependency management

**Common Challenge**: Many systems operate with cron-based backup scripts from 1990s, resisting migration to systemd-timer despite better logging and dependency handling. Cron timezone issues affect globally distributed teams.

#### 5. **Memory and CPU Metrics (Questions 023-040)**
- **/proc/meminfo**: System memory breakdown
  - MemAvailable: Allocatable memory (includes cache reclaimable)
  - Dirty: Unwritten to disk (indicates write workload)
- **swappiness**: Preference for disk swap over page cache eviction
  - Default 60 (too aggressive on modern servers)
  - Lowering to 10-20 better for most workloads
- **Page Cache**: Memory page copy of disk blocks
  - High ratio indicates I/O for same data repeatedly
  - `drop_caches` (seq 3) useful for benchmarking
- **NUMA**: Multi-socket performance (numactl for binding)
- **CPU Cache Analysis**: `perf stat` for miss rates

**Common Challenge**: Swappiness defaults assume consumer laptops. Enterprise systems with 256GB RAM and swap still use default 60, causing strange performance cliffs when memory approaches 50% utilization. NUMA-related performance problems are mysterious to non-expert operators.

#### 6. **Disk and I/O Performance (Questions 019-045)**
- **I/O Wait (%iowait)**: CPU idle waiting for disk completion
  - High %iowait = storage bottleneck
  - Not memory pressure, not CPU limit
- **Queue Length (avgqu-sz)**: Running I/O commands
  - >1 per disk = saturation
  - Indicator of queue buildup behind slow disk
- **Latency Metrics**:
  - r_await/w_await: Physical disk response time
  - svctm: Service time (deprecated, but still seen)
- **Benchmarking Tools**:
  - `fio`: Flexible I/O tester (standard for testing)
  - `bonnie++`: Sequential and random I/O
  - `iozone`: Detailed I/O profiling
- **Read vs Write Asymmetry**: SSDs often have 10x read/write performance differences

**Common Challenge**: Operators often correlate disk usage % with performance. A disk at 90% usage with low queue length has different performance characteristics than one at 50% usage with queue length > 5. Understanding demand vs. capacity requires thought.

#### 7. **Log File Locations and Permissions (Questions 001-003)**
- `/var/log/syslog` or `/var/log/messages` (distribution-dependent)
- `/var/log/auth.log` (Linux) or `/var/log/secure` (RedHat-based)
- `/var/log/kern.log` for kernel-specific messages
- Log rotation via logrotate (daily, weekly, monthly, yearly)

**Common Challenge**: Log file paths vary significantly between Debian/Ubuntu (syslog) and RedHat/CentOS (messages). Automation scripts often hardcode paths, breaking across distributions.

---

## Key Research Findings

### Storage Management Critical Issues

1. **Partitioning Mistakes**
   - MBR 2TB limitation still surprises many admins
   - GPT adoption slow due to legacy tooling (fdisk vs parted)
   - Partition schema changes risk data loss without careful planning

2. **File System Selection Impacts**
   - ext4 as default choice often wins over better options (XFS, Btrfs)
   - Performance differences only matter at scale (>1TB datasets)
   - File system repair times vary wildly (ext4: minutes, Btrfs: hours)

3. **LVM Complexity**
   - Three-tier abstraction (PV→VG→LV) requires mental model
   - Snapshot management critical for backup windows
   - Capacity planning errors common (sizing VG too small initially)

4. **Disk Space Exhaustion**
   - Inode exhaustion often mistaken for block exhaustion
   - Cache pressure causes apparent "full disk" with available blocks
   - Log files accumulation in /var/log without logrotate

5. **RAID Operational Hazards**
   - Rebuild windows (10-48 hours) create dual-failure vulnerability
   - RAID 5 with large disks: 2-disk failures statistically likely
   - Rebuild performance impact underestimated in concurrent load

### System Administration Critical Issues

1. **Log Management Scale**
   - Daily log volume exceeds capacity planning (100GB+ possible)
   - Retention policies often miss critical compliance windows
   - rsyslog remote forwarding introduces network dependency

2. **Performance Debugging Challenges**
   - iowait% vs CPU% misinterpretation leads wrong remediation
   - Queue depth interpretation requires empirical baseline knowledge
   - Memory metrics (RSS vs VSZ vs MemAvailable) frequently confused

3. **Process Management Errors**
   - Zombie processes indicate parent process bugs (common)
   - File descriptor exhaustion causes cryptic "too many files" errors
   - Nice/priority changes ineffective without CPU understanding

4. **Backup Window Impacts**
   - Snapshot creation freezes filesystem briefly (transparent but impacts latency)
   - Incremental backups require careful timestamp tracking
   - Restore testing often neglected (70% failure rate in field studies)

5. **Monitoring Blind Spots**
   - Swappiness defaults cause unexpected behavior (NUMA systems especially)
   - CPU affinity misconfiguration on NUMA: 30-40% performance loss
   - Cache-heavy workloads invisible to traditional metrics

---

## LPIC Alignment

### LPIC-1 Coverage (101/102)
- Disk partitioning (fdisk, parted)
- File systems (ext2, ext3, ext4, XFS)
- File system mounting (/etc/fstab)
- Basic LVM operations
- User/group quotas
- Simple performance monitoring (top, free, df)
- Log file locations
- Basic cron/at scheduling

### LPIC-2 Coverage (201/202)
- Advanced partitioning (GPT, UEFI)
- Advanced LVM (snapshots, expansion)
- RAID management
- Advanced file system repairs
- rsyslog configuration
- Advanced monitoring (iostat, vmstat, sar)
- systemd unit/timer management
- Performance tuning parameters
- Advanced backup strategies (rsync, dd, tar)

---

## Practical Application Scenarios

### Scenario 1: Emergency Disk Capacity Extension
**Problem**: Production database system at 95% capacity, iowait 80%
**Skills Required**:
- Identify block vs inode exhaustion (df -i)
- LVM expansion (lvextend -r)
- File system resize (resize2fs)
- Priority ranking of cleanup candidates (du measurements)

### Scenario 2: Log Explosion Debugging
**Problem**: /var full, applications failing, root cause unknown
**Skills Required**:
- logrotate configuration (rotate retention)
- rsyslog filtering rules (severity levels)
- Find large files (du, find patterns)
- Journalctl storage management (disk parameter)

### Scenario 3: RAID Recovery Planning
**Problem**: RAID 5 array with one disk down, rebuild takes 36 hours
**Skills Required**:
- Understand rebuild risk (2-disk failure window)
- Monitor rebuild progress (iostat -x)
- Predict performance impact (queue analysis)
- Plan maintenance window (capacity/redundancy tradeoff)

### Scenario 4: Performance Baseline Establishment
**Problem**: System feels slow, but metrics appear normal
**Skills Required**:
- Establish baseline (sar historical data)
- CPU affinity analysis (taskset)
- Memory pressure vs iowait correlation
- Profile application I/O patterns (strace)

---

## Certification Tips

1. **fdisk vs parted**: Know when each is appropriate (MBR vs GPT)
2. **lvextend/resize2fs**: Order matters; always extend LV before filesystem
3. **fsck safety**: Never run on mounted filesystem (unless read-only rescue)
4. **dmesg vs journalctl**: Understand scope differences (kernel vs system)
5. **rsync --delete**: Know deletion direction; always use --dry-run first
6. **iowait interpretation**: Not a performance metric; indicates bottleneck existence
7. **zombie processes**: Understand parent-child relationship; kill parent, not zombie
8. **nice/renice bounds**: -20 to 19; lower = higher priority (inverted intuition)
9. **systemd timer**: Requires both .service and .timer files in /etc/systemd/system/
10. **quota terminology**: Hard limit stops access; soft limit warns only

---

## References & Standards

- LPIC-1 Exam 101 (System Architecture & Installation)
- LPIC-1 Exam 102 (Linux Installation & Package Management)
- LPIC-2 Exam 201 (Advanced Linux Administration)
- LPIC-2 Exam 202 (Linux Administration & Networking)
- Linux Foundation Education (2019-2024 standards)
- Storage and Performance Best Practices

---

## Question Distribution Summary

### Storage Management (50 questions)
- Partitioning: 10 questions
- LVM: 5 questions
- File Systems: 7 questions
- Mount Operations: 3 questions
- File System Repair: 5 questions
- Disk Quotas: 3 questions
- Backup/Restoration: 5 questions
- RAID Concepts: 3 questions
- Space/Inode Management: 8 questions
- Advanced Features: 1 question

### System Administration (50 questions)
- Log Management: 14 questions
- Performance Monitoring: 11 questions
- Process Management: 11 questions
- Cron/systemd Job Scheduling: 4 questions
- Memory/CPU Metrics: 10 questions

**Total**: 100 comprehensive exam questions covering LPIC-1 and LPIC-2 storage and system administration domains.
