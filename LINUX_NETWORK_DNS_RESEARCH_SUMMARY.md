# Linux Network Settings and DNS - Research Summary

## Exam Standard
- **Exam**: Linux
- **Category**: ネットワーク設定とDNS (Network Settings and DNS)
- **Question IDs**: linux_network_dns_001 to linux_network_dns_050
- **Alignment**: LPIC-1 (101.3, 102.1) and LPIC-2 (201.1) 2019-2024 Standards

## Overview
Linux network settings and DNS covers the configuration and management of network interfaces, DHCP clients, DNS resolution, and network tools. This includes both legacy and modern approaches to network configuration.

## Key Topics Covered

### 1. Network Interface Configuration (Questions 001-004, 010-011, 019-020, 042-043)

#### Traditional ifconfig (Legacy)
- `ifconfig` - Display/configure network interfaces
- `ifconfig eth0` - Show interface details
- `ifconfig eth0 up/down` - Enable/disable interface
- `ifconfig eth0 192.168.1.100 netmask 255.255.255.0` - Set static IP
- IPv4-only, deprecated in favor of `ip` command

#### Modern ip Command
- `ip addr show` - List all interfaces and addresses
- `ip addr add 192.168.1.100/24 dev eth0` - Add address
- `ip addr del 192.168.1.100/24 dev eth0` - Remove address
- `ip link show` - Show interface status
- `ip link set eth0 up/down` - Enable/disable interface
- `ip link set eth0 mtu 1500` - Change MTU
- `ip link set eth0 promisc on` - Promiscuous mode

#### Configuration Files

##### Debian/Ubuntu (/etc/network/interfaces)
```
auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8 8.8.4.4
```

##### RedHat/CentOS (/etc/sysconfig/network-scripts/ifcfg-eth0)
```
DEVICE=eth0
TYPE=Ethernet
BOOTPROTO=none
IPADDR=192.168.1.100
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
ONBOOT=yes
```

##### Modern netplan (/etc/netplan/00-installer-config.yaml)
```yaml
network:
  version: 2
  ethernets:
    eth0:
      addresses: [192.168.1.100/24]
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

### 2. DHCP Configuration (Questions 001, 017-021, 047)

#### DHCP Client (dhclient)
- `dhclient eth0` - Obtain IP via DHCP
- `dhclient -r eth0` - Release DHCP lease
- `dhclient -r eth0 && dhclient eth0` - Renew lease
- `cat /var/lib/dhclient/dhclient.leases` - View lease information

#### DHCP Configuration (/etc/dhcp/dhclient.conf)
- `request` statement: Specify which DHCP options to request
- `require` statement: Require certain options or fail
- `send` statement: Send custom DHCP options
- `ignore` statement: Ignore specific DHCP options

### 3. CIDR Notation (Question 005)

#### Classless Inter-Domain Routing
- /32: Single host
- /24: 254 usable hosts
- /16: 65,534 usable hosts
- /8: Class A network
- /30: Point-to-point link (2 usable addresses)

### 4. DNS Resolution (Questions 003, 006, 021, 024-027, 035, 041)

#### /etc/resolv.conf
- `nameserver` entries specify DNS servers
- `search` statement specifies domain search path
- `domain` statement for default domain

#### systemd-resolved
- `resolvectl status` - Show DNS resolver status
- `resolvectl query example.com` - Query DNS
- `resolvectl flush-caches` - Clear DNS cache

#### /etc/hosts File
- Format: `IP hostname [alias]`
- Local static hostname mapping
- Checked before DNS queries

### 5. DNS Lookup Tools (Questions 008, 025-027, 044)

#### nslookup
- `nslookup example.com` - Query DNS
- `nslookup example.com 8.8.8.8` - Query specific DNS server
- Shows A, AAAA, MX, NS records

#### dig (Domain Information Groper)
- `dig example.com` - Standard query
- `dig NS example.com` - Query NS records
- `dig MX example.com` - Query mail records
- `dig A example.com +short` - Short output
- `dig @8.8.8.8 example.com` - Specific DNS server
- `dig +trace example.com` - Trace DNS resolution path

#### host
- Simpler DNS lookup tool
- `host example.com` - Query DNS
- `host -t MX example.com` - Query specific record type

### 6. Hostname Configuration (Questions 007, 014)

#### hostnamectl Command (systemd)
- `hostnamectl` - Show hostname status
- `hostnamectl set-hostname newname` - Set hostname permanently
- `hostnamectl set-hostname --pretty "My Computer"` - Friendly name

#### /etc/hostname File
- Single-line file containing hostname
- Persistent across reboots

### 7. Routing Configuration (Questions 009, 029, 037, 040)

#### route Command (Legacy)
- `route -n` - Display routing table (numeric)
- `route add default gw 192.168.1.1` - Add default gateway
- `route del default gw 192.168.1.1` - Remove route

#### ip route Command (Modern)
- `ip route show` - Display routing table
- `ip route add 192.168.2.0/24 via 192.168.1.1` - Add route
- `ip route add default via 192.168.1.1 dev eth0` - Add default gateway

### 8. Network Status and Monitoring (Questions 011-013, 028, 032, 034, 036, 038, 045-046)

#### ping Command
- `ping -c 4 hostname` - Send 4 echo requests
- Measures latency and packet loss
- 100% loss indicates host unreachable

#### traceroute/mtr Commands
- `traceroute hostname` - Show path to host
- `mtr hostname` - Real-time hop monitoring

#### netstat Command (Legacy)
- `netstat -r` - Show routing table
- `netstat -tulnp` - Show listening ports
- `netstat -an | grep LISTEN` - Show listening services

#### ss Command (Modern)
- `ss -tulnp` - Show listening ports (preferred)
- `ss -tanp` - Show all TCP connections
- Faster than netstat

### 9. Network Interface Information (Question 010, 032, 048)

#### Interface Status Flags
- **UP**: Interface is active
- **DOWN**: Interface is inactive
- **BROADCAST**: Supports broadcast
- **MULTICAST**: Supports multicast
- **LOOPBACK**: Loopback interface
- **PROMISC**: Promiscuous mode enabled

## LPIC Alignment

### LPIC-1 101.3: GNU and Unix Commands
- Network tools and commands
- Basic network troubleshooting

### LPIC-1 102.1: Devices, Linux Filesystems, FHS
- Device configuration files
- /etc directory structure for network config

### LPIC-2 201.1: Network Device Configuration
- Complex network interface setup
- Advanced DNS configuration
- Routing and gateway setup
- Network troubleshooting techniques

## Common Scenarios

### Scenario 1: Static IP Configuration (Debian)
```bash
# Edit /etc/network/interfaces
sudo nano /etc/network/interfaces

# Add:
auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8 8.8.4.4

# Apply
sudo systemctl restart networking
```

### Scenario 2: DHCP Configuration
```bash
# Use dhclient for configuration
sudo dhclient eth0

# View lease
cat /var/lib/dhclient/dhclient.leases

# Release and renew
sudo dhclient -r eth0
sudo dhclient eth0
```

### Scenario 3: DNS Troubleshooting
```bash
# Check DNS configuration
resolvectl status

# Flush DNS cache
resolvectl flush-caches

# Test DNS resolution
dig example.com
nslookup example.com
```

## Questions Coverage

The 50 questions are structured as follows:

- **Questions 001-010**: DHCP, IP configuration, interface management
- **Questions 011-015**: Network tools and interface status
- **Questions 016-025**: DNS configuration and tools
- **Questions 026-035**: Hostname, routing, and network status
- **Questions 036-045**: DNS tools and network configuration
- **Questions 046-050**: Advanced configuration and modern tools

Each question focuses on practical scenarios and command syntax relevant to system administrators managing Linux network infrastructure.
