# Linux Firewall and Communication Control - Research Summary

## Exam Standard
- **Exam**: Linux
- **Category**: ファイアウォールと通信制御 (Firewall and Communication Control)
- **Question IDs**: linux_firewall_001 to linux_firewall_050
- **Alignment**: LPIC-1 (102.4) and LPIC-2 (201.4, 205.3) 2019-2024 Standards

## Overview
Linux firewall and communication control covers the implementation and management of firewalls using various tools and technologies. This includes iptables fundamentals, firewalld, ufw, NAT configuration, and stateful inspection.

## Key Topics Covered

### 1. iptables Fundamentals (Questions 001-020)

#### Tables Structure
- **filter table**: Default table for packet filtering (INPUT, OUTPUT, FORWARD chains)
- **nat table**: Network Address Translation (PREROUTING, OUTPUT, POSTROUTING chains)
- **mangle table**: Packet modification (TTL, ToS, marking)
- **raw table**: Connection tracking exclusion (processed first)

#### Chains and Flow
- **INPUT**: Incoming packets to local system
- **OUTPUT**: Outgoing packets from local system
- **FORWARD**: Packets passing through system (router)
- **PREROUTING**: Before routing decision (NAT)
- **POSTROUTING**: After routing decision (NAT)

#### Basic Operations
- `-A` (Append): Add rule to end of chain
- `-I` (Insert): Add rule to beginning of chain
- `-D` (Delete): Remove specific rule
- `-F` (Flush): Remove all rules from chain
- `-P` (Policy): Set default policy for chain
- `-L` (List): Display rules (with `-v` for verbose, `-n` for numeric)
- `-S` (Save): Display rules in iptables-save format

#### Matching Criteria
- `-p` (protocol): tcp, udp, icmp, all
- `-s` (source): IP address or CIDR notation
- `-d` (destination): IP address or CIDR notation
- `-i` (input interface): eth0, eth1, etc.
- `-o` (output interface): eth0, eth1, etc.
- `--dport` (destination port): Single port or range
- `--sport` (source port): Single port or range
- `-m` (match extension): state, multiport, mac, tcp, limit, etc.

#### Jump Targets
- `ACCEPT`: Allow packet
- `DROP`: Discard packet silently
- `REJECT`: Discard packet with ICMP error response
- `LOG`: Log packet to syslog/kernel log
- `RETURN`: Stop processing current chain
- `DNAT`: Destination NAT
- `SNAT`: Source NAT
- `MASQUERADE`: Dynamic SNAT

### 2. Connection Tracking (Questions 015-017, 030)

#### Stateful Inspection
- `nf_conntrack` module enables connection tracking
- `-m state --state` module for connection state matching
- Connection states:
  - **NEW**: New connection attempt
  - **ESTABLISHED**: Existing connection with bidirectional communication
  - **RELATED**: Associated with existing connection
  - **INVALID**: Does not belong to tracked connection

#### Best Practice Rules
1. Allow loopback (127.0.0.1)
2. Allow established/related connections
3. Allow new connections on specific ports
4. Drop invalid/remaining packets

### 3. Network Address Translation (Questions 011-013, 039-040)

#### Source NAT (SNAT)
- Implemented in POSTROUTING chain
- Changes source IP address of outgoing packets
- Common for internal network access to external network
- Command: `iptables -t nat -A POSTROUTING -o eth0 -j SNAT --to-source IP`

#### Destination NAT (DNAT)
- Implemented in PREROUTING chain
- Changes destination IP/port of incoming packets
- Used for port forwarding and load balancing
- Command: `iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 8080 -j DNAT --to-destination 192.168.1.10:80`

#### Masquerading
- Special case of SNAT for dynamic IP addresses
- Automatically uses interface's current IP
- Command: `iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE`

### 4. Advanced Matching (Questions 034-044)

#### MAC Address Matching
- `-m mac --mac-source` for source MAC filtering
- Useful for LAN device control

#### TCP Flag Matching
- `-m tcp --tcp-flags SYN,ACK SYN` for SYN packets only
- Prevents SYN flood attacks with rate limiting

#### Multiport Matching
- `-m multiport --dports 80,443,8080` for multiple ports
- More efficient than multiple rules

#### Rate Limiting
- `-m limit --limit 25/minute` to prevent DoS attacks
- `--limit-burst` for burst handling

#### ICMP Matching
- `-p icmp --icmp-type echo-request` for ping requests
- Other types: echo-reply, unreachable, time-exceeded

### 5. Logging (Questions 018-019, 050)

#### LOG Target
- `-j LOG` sends packets to kernel log
- `--log-prefix "string"` adds prefix to log entries
- Log appears in /var/log/kernel.log or /var/log/syslog

#### Best Logging Practice
- Place LOG rule before DROP rule
- Use meaningful prefixes for filtering
- Monitor logs with `tail -f /var/log/syslog`

### 6. Persistence (Questions 037-038)

#### iptables-persistent (Debian/Ubuntu)
- Package: `iptables-persistent`
- Saves rules in:
  - `/etc/iptables/rules.v4` (IPv4)
  - `/etc/iptables/rules.v6` (IPv6)
- Save command: `dpkg-reconfigure iptables-persistent`
- Restore command: `iptables-restore < /etc/iptables/rules.v4`

#### Manual Save/Restore
- Save: `iptables-save > /etc/iptables/rules.v4`
- Restore: `iptables-restore < /etc/iptables/rules.v4`

### 7. ufw - Uncomplicated Firewall (Questions 020-023)

#### Basic Commands
- `ufw enable/disable` - Enable or disable firewall
- `ufw allow 22` - Allow port/service
- `ufw deny 22` - Deny port/service
- `ufw delete allow 22` - Remove rule
- `ufw reset` - Reset all rules

#### Advanced Rules
- `ufw allow from 192.168.1.50 to any port 5432` - Limit source IP
- `ufw allow http` - Allow by service name
- `ufw status` - Show active rules
- `ufw status verbose` - Show detailed rules

#### Configuration
- Config: `/etc/ufw/ufw.conf`
- Rules: `/etc/ufw/rules.v4` and `rules.v6`
- Services: `/etc/ufw/applications.d/`

### 8. firewalld (Questions 024-029, 045-046)

#### Zones
- **drop**: Most restrictive, drop all incoming
- **block**: Reject incoming (with ICMP response)
- **public**: Default for untrusted networks
- **external**: Enables masquerading
- **dmz**: Limited access for DMZ
- **work**: For trusted work networks
- **home**: For trusted home networks
- **internal**: For internal networks
- **trusted**: Allows all traffic

#### Basic Commands
- `firewall-cmd --state` - Check firewall status
- `firewall-cmd --get-active-zones` - Show active zones
- `firewall-cmd --list-all` - Show all rules for active zone
- `firewall-cmd --permanent --add-service=http` - Add service permanently
- `firewall-cmd --add-port=8080/tcp` - Add port (temporary)
- `firewall-cmd --reload` - Reload configuration

#### Service Management
- Services defined in `/etc/firewalld/services/*.xml`
- Each service specifies ports and protocols
- Can create custom services

### 9. Rule Ordering and Performance (Questions 033, 041-042)

#### Rule Order Impact
1. More specific rules before general rules
2. Frequently matching rules first
3. Deny rules after allow rules (typically)
4. Order: Allow established → Allow new → Deny/Log

#### Performance Optimization
- `-n` flag avoids DNS lookups
- Group multiple ports with multiport
- Use port ranges for efficiency
- Connection tracking reduces rule matching overhead

### 10. netfilter Architecture (Questions 048-049)

#### Hook Points
- **NF_IP_PRE_ROUTING**: raw → mangle → nat (PREROUTING)
- **NF_IP_LOCAL_IN**: mangle → filter (INPUT)
- **NF_IP_FORWARD**: mangle → filter (FORWARD)
- **NF_IP_LOCAL_OUT**: raw → mangle → nat → filter (OUTPUT)
- **NF_IP_POST_ROUTING**: mangle → nat (POSTROUTING)

#### Table Processing Order
1. raw (connection tracking exclusion)
2. mangle (packet modification)
3. nat (address translation)
4. filter (packet filtering)

## LPIC Alignment

### LPIC-1 (102.4: Firewall Configuration)
- Basic iptables concepts
- Rules and chains
- Jump targets
- Simple NAT configuration
- Basic packet filtering

### LPIC-2 (201.4: Network Interface Configuration)
- Advanced iptables usage
- Complex NAT scenarios
- Stateful inspection
- Advanced connection tracking
- Performance optimization

### LPIC-2 (205.3: Cyrus IMAP and Postfix)
- Mail server firewall rules
- Service-specific port forwarding
- Stateful filtering for protocols

## Common Scenarios

### Scenario 1: Gateway with NAT
```bash
# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# SNAT for internal network (192.168.1.0/24)
iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o eth0 -j SNAT --to-source 203.0.113.10

# Allow forwarding
iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
iptables -A FORWARD -i eth0 -o eth1 -m state --state ESTABLISHED,RELATED -j ACCEPT
```

### Scenario 2: Web Server Protection
```bash
# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Default policy: DROP
iptables -P INPUT DROP
```

### Scenario 3: Port Forwarding
```bash
# Forward external port 8080 to internal web server 192.168.1.10:80
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 8080 -j DNAT --to-destination 192.168.1.10:80
iptables -A FORWARD -p tcp -d 192.168.1.10 --dport 80 -j ACCEPT
```

## Tools and Utilities

### Analysis Tools
- `iptables -L -n -v` - List rules with packet/byte counts
- `iptables -S` - Show rules in command format
- `iptables-save` - Export rules for backup
- `iptables-restore` - Import rules from file

### Monitoring
- `tail -f /var/log/syslog` - Watch firewall logs
- `dmesg | grep "UFW"` - View ufw messages (Ubuntu)
- `journalctl -u firewalld` - View firewalld logs (systemd)

## Security Best Practices

1. **Default Deny**: Set default policies to DROP
2. **Explicit Allow**: Only allow necessary traffic
3. **Logging**: Log dropped packets for monitoring
4. **Stateful**: Use connection tracking for efficiency
5. **Testing**: Test rules before applying permanently
6. **Documentation**: Comment rules for maintenance
7. **Minimal Rules**: Reduce rule count for performance

## Recent Changes (2019-2024)

### nftables Migration
- Modern replacement for iptables
- More consistent syntax
- Better performance
- Still maintains iptables compatibility layer

### systemd Integration
- firewalld as primary firewall management
- systemd-resolved for DNS
- Zone-based configuration
- Hot reload without service restart

### Cloud Considerations
- Security groups in cloud platforms
- Integration with container networking
- Dynamic rule management
- API-based firewall control

## References

### LPIC-2 Study Resources
- Topic 201.4: Firewall Configuration
- Topic 205.3: Network Services Configuration
- GNU Linux certification resources

### Standards
- netfilter documentation (https://www.netfilter.org/)
- Debian/Ubuntu AppArmor integration
- RHEL/CentOS SELinux integration with firewalld

## Questions Coverage

The 50 questions are structured as follows:

- **Questions 001-010**: iptables fundamentals and basic operations
- **Questions 011-017**: NAT configuration and stateful inspection
- **Questions 018-030**: Logging, ufw, and firewalld basics
- **Questions 031-044**: Advanced matching and optimization
- **Questions 045-050**: firewalld advanced topics and netfilter architecture

Each question focuses on practical scenarios and command syntax relevant to real-world firewall administration.
