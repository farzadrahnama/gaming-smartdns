<div align="center" style="text-align: center;">
  <p><a href="README.md"><strong>English</strong></a> &nbsp;|&nbsp; <a href="README.fa.md"><strong>فارسی</strong></a></p>
  <h1 align="center" style="text-align: center;">🎮 Gaming SmartDNS & SNI Proxy Hub</h1>
  <p align="center" style="text-align: center;">
    <strong>Sub-1ms Overhead &bull; Zero In-Game Ping &bull; Multi-Tenant Reseller Panel &bull; Dynamic IP Whitelisting &bull; Cloudflare Ready</strong><br>
    <em>The high-performance, private SmartDNS & SNI Proxy suite engineered for competitive gaming and AI platforms.</em>
  </p>
  <p align="center" style="text-align: center;">
    <a href="https://github.com/farzadrahnama/gaming-smartdns/releases/latest"><img alt="Latest Release v2.5.0" src="https://img.shields.io/badge/Release-v2.5.0-0078D4?style=flat-square&logo=github&logoColor=white"></a>&nbsp;<a href="https://github.com/farzadrahnama/gaming-smartdns"><img alt="GitHub Stars" src="https://img.shields.io/github/stars/farzadrahnama/gaming-smartdns?style=flat-square&color=yellow&logo=github"></a>&nbsp;<a href="https://opensource.org/licenses/MIT"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green?style=flat-square"></a><br><a href="#-system-requirements"><img alt="Ubuntu 22.04 / 24.04" src="https://img.shields.io/badge/Ubuntu-22.04%20%2F%2024.04-E95420?style=flat-square&logo=ubuntu&logoColor=white"></a>&nbsp;<a href="#-system-requirements"><img alt="Docker Engine Ready" src="https://img.shields.io/badge/Docker-Engine%20Ready-2496ED?style=flat-square&logo=docker&logoColor=white"></a>&nbsp;<a href="#-system-requirements"><img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white"></a>&nbsp;<a href="#%EF%B8%8F-security-hardening--privacy"><img alt="Firewall: ipset hardened" src="https://img.shields.io/badge/Firewall-ipset%20hardened-success?style=flat-square"></a>
  </p>
  <p align="center" style="text-align: center;">
    <sub><strong>Zero In-Game Ping Overhead</strong> &bull; Only Auth & Licenses Proxied &bull; Direct P2P/UDP Match Traffic &bull; PS5 / Xbox / PC &bull; 100% Private</sub>
  </p>
</div>

---

## 🚀 Overview

Competitive gamers frequently face severe regional geo-blocks, international sanctions, high ping, and matchmaking errors across major platforms—including **Call of Duty (Warzone, MW3, BO6)**, **EA Sports FC / Apex Legends**, **PlayStation Network (PSN)**, **Xbox Live**, **Blizzard Battle.net**, and **Epic Games**. At the same time, professionals and developers face restrictions accessing advanced AI ecosystems (**ChatGPT, Claude, Gemini, Antigravity**).

Traditional VPNs or full-tunnel proxies route **all** device network packets (including heavy voice chat and live multiplayer UDP traffic) through distant encrypted tunnels. This results in **severe ping spikes (+50ms to +150ms), packet jitter, packet loss, and anti-cheat account suspensions**.

**Gaming SmartDNS & SNI Proxy Hub** solves this natively through precision split-routing:
1. **DNS Resolution Layer:** Routes only blocked authentication, licensing, and matchmaking domain endpoints to a lightweight SNI proxy.
2. **Untouched Gameplay (0ms Added Ping):** All in-game UDP match packets, multiplayer voice chat, and telemetry flow **100% directly** between the user's console or PC and the official game servers.
3. **Turnkey Management:** Features a modern, multi-tenant **FastAPI Web Dashboard**, **Reseller / Sub-Admin hierarchy**, **Kernel-level `ipset` firewall protection**, and **Real-Time Live Traffic Sniffing**.

---

## ✨ Key Capabilities at a Glance

| Feature | Traditional VPN / SOCKS5 | Gaming SmartDNS & SNI Proxy Hub |
| :--- | :--- | :--- |
| **In-Game Ping & Latency** | High ping penalty (+40ms to +120ms added) | **0ms added latency** (Direct client-to-server UDP) |
| **Match Packet Jitter** | High jitter due to VPN encryption overhead | **Identical to native ISP connection** |
| **Server Bandwidth Cost** | High (50–100 GB per gamer/month) | **Minimal (<1 GB per gamer/month)**; game files download direct |
| **Anti-Cheat & Ban Safety** | High risk (Datacenter IP flagged by Ricochet/Vanguard) | **100% Safe** (In-game multiplayer connects directly to official servers) |
| **Console Compatibility** | Requires expensive custom routers or PC hotspot | **Native support**; just enter 2 DNS IP numbers on PS5/Xbox |
| **Multi-Tenant / Resellers** | Manual key generation or complex setups | **Built-in Reseller System** with user quotas and custom links |
| **Unauthorized Abuse Defense**| Open DNS resolvers attract DDoS attacks | **Kernel `ipset` Firewall**; only whitelisted IPs can resolve |
| **Dynamic IP Handling** | Requires client apps or persistent VPN tunnels | **1-Click Dynamic IP Updater link** for mobile & home routers |
| **Live Traffic Inspection** | Difficult to monitor specific game queries | **Real-time DNS Query Sniffer** streaming live game events |
| **Web Management UI** | CLI only or third-party bloated panels | **Modern, responsive FastAPI Dashboard** with Dark Mode |

---

## 🏗️ Architecture & Traffic Flow

```text
[User Device: PC / PS5 / Xbox / Mobile]
       │
       ▼ (DNS Query on Port 53)
[Linux Kernel Firewall: ipset (gamers)]
       ├── 🚫 Unregistered IP  ──► Silent DROP (Zero DDoS footprint)
       └── ✅ Whitelisted IP   ──► Forward to SmartDNS Engine
                                            │
                             ┌──────────────┴──────────────┐
                             ▼                             ▼
                  [Sanctioned Game / AI Domains]      [Unrestricted Internet]
                  Spoofed to Server Public IP         Direct resolution via 1.1.1.1
                             │                             │
                             ▼                             ▼
                  [SNI Proxy Engine (Port 443)]       [Direct ISP Connection]
                  Transparent TLS Pass-Through        (Normal Browsing & Downloads)
                             │
                             ▼
         [Official Game Auth / Licensing Server]
                             │
                             ▼ (Matchmaking complete)
         [Official Multi-player Game Match (UDP Port 3074 / 27015 / etc.)]
         ═════════════════════════════════════════════════════════════════► DIRECT TO GAME SERVER (0ms Ping!)
```

---

## 🔍 Feature Tour

### 1. Ultra-Low Overhead SmartDNS & SNI Proxy
* **Zero Decryption / Zero Re-encryption:** The SNI proxy inspects only the TLS ClientHello Server Name Indication (SNI) header and transparently pipes packets through. CPU usage remains negligible even under thousands of concurrent connections.
* **Pre-configured Rule Sets:** Out-of-the-box optimized domain lists for Activision/Call of Duty, EA/Origin, Blizzard Battle.net, Epic Games, Riot Games, PSN, Xbox Live, OpenAI, Anthropic Claude, and Google Gemini.
* **Smart Upstream Forwarding:** Any domain not in the sanction list resolves directly via Cloudflare DNS (`1.1.1.1`), ensuring uninhibited local internet performance.

### 2. Multi-Tenant FastAPI Management Dashboard
* **Role-Based Access Control:** Dual-tier hierarchy supporting Super-Admins and Resellers (Sub-Admins).
* **Reseller Quota System:** Resellers can independently register, renew, expire, and monitor their assigned client quotas without accessing host system configuration.
* **Dark Mode UI:** Lightweight, responsive interface built with modern CSS and reactive JavaScript.
* **Integrated Password Manager:** Secure in-app password changes with bcrypt hashing.

### 3. Dynamic IP Whitelisting & Kernel-Level Firewall
* **Zero DDoS Footprint:** Port 53 (DNS) and Port 443 (SNI Proxy) are closed by default. The Linux kernel drops all packets from non-whitelisted IPs before they reach userspace.
* **Tokenized 1-Click IP Activator:** Users receive a personal URL (`https://your-domain.com/activate?token=...`). Opening this link from any mobile phone, browser, or PC on their home network instantly registers their dynamic public IP for 30 days.

### 4. Real-time Live Traffic Sniffer
* **Live Game Query Stream:** Stream incoming DNS queries in real-time (`/admin/logs`) to verify which domains a console or PC is accessing during game startup.
* **Instant Troubleshooting:** Identify missing game domain endpoints immediately without SSH debugging.

---

## 📦 Installation & Deployment Guide

You can deploy Gaming SmartDNS & SNI Proxy using either the **Automated 1-Click Installer** (recommended for production servers) or via **Step-by-Step Manual Setup**.

---

### 📋 Prerequisites & Port Requirements

Before starting installation, ensure your cloud provider firewall (e.g. Hetzner, DigitalOcean, AWS Security Groups) permits traffic on the following ports:

| Port | Protocol | Usage | Access Policy |
| :--- | :--- | :--- | :--- |
| **53** | `UDP` / `TCP` | SmartDNS Resolver | Whitelisted IPs only (Enforced via `ipset`) |
| **443** | `TCP` | SNI Proxy Pass-through | Whitelisted IPs only (Enforced via `ipset`) |
| **8080** | `TCP` | FastAPI Management Web Panel | Cloudflare IPs only (or Origin Rule proxy) |
| **22** | `TCP` | SSH Administration | Restricted / Protected by `fail2ban` |

> [!NOTE]
> Supported Operating Systems: **Ubuntu 22.04 LTS** or **Ubuntu 24.04 LTS** (x86_64 / ARM64). Root or sudo privileges required.

---

### ⚡ Method 1: Automated 1-Click Installation (Recommended)

Log in to your clean Ubuntu server as `root` and run:

```bash
# 1. Clone the repository into /opt/smartdns
git clone https://github.com/farzadrahnama/gaming-smartdns.git /opt/smartdns
cd /opt/smartdns

# 2. Make the installer executable and launch setup
chmod +x install.sh
bash install.sh
```

#### What the installer does automatically:
1. **System Preparation:** Updates apt packages and installs prerequisites (`curl`, `git`, `ipset`, `iptables-persistent`, `tcpdump`, `fail2ban`, `python3-pip`).
2. **Docker Environment:** Installs Docker Engine and Docker Compose if not already present.
3. **Kernel Firewall Hardening:**
   * Creates the kernel IP set: `ipset create gamers hash:ip`
   * Binds iptables rules to drop all unauthorized traffic on ports 53 and 443.
   * Enables persistence across system reboots (`netfilter-persistent save`).
4. **SNI Proxy Container:** Launches the high-performance `sniproxy` Docker container listening on port 443.
5. **DNS Engine & Query Sniffer:** Configures the DNS resolver with gaming/AI domain rewrites and starts the unbuffered `smartdns-sniffer` systemd service for real-time logging.
6. **FastAPI Web Panel:** Creates the Python virtual environment, installs dependencies, sets up SQLite database permissions (`chmod 600 users.db`), and starts the `smartdns-panel` systemd daemon on port 8080.
7. **Super-Admin Setup:** Prompts you to set a secure administrator username and password.

---

### 🛠️ Method 2: Manual Step-by-Step Deployment

If you prefer custom configurations or containerized deployment:

<details>
<summary><b>Click to expand manual step-by-step instructions</b></summary>

#### Step 1: Install System Packages
```bash
apt update && apt upgrade -y
apt install -y docker.io docker-compose-plugin python3 python3-pip python3-venv ipset iptables-persistent tcpdump fail2ban curl git
```

#### Step 2: Configure Kernel Firewall (`ipset`)
```bash
# Create the whitelisted gamers ipset
ipset create gamers hash:ip timeout 2592000

# Allow loopback and established connections
iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT

# Allow DNS (53) and SNI Proxy (443) ONLY for whitelisted IPs
iptables -A INPUT -p udp --dport 53 -m set --match-set gamers src -j ACCEPT
iptables -A INPUT -p tcp --dport 53 -m set --match-set gamers src -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -m set --match-set gamers src -j ACCEPT

# Drop all unauthorized DNS and SNI attempts
iptables -A INPUT -p udp --dport 53 -j DROP
iptables -A INPUT -p tcp --dport 53 -j DROP
iptables -A INPUT -p tcp --dport 443 -j DROP

# Save firewall rules
netfilter-persistent save
```

#### Step 3: Start the SNI Proxy Container
Create `docker-compose.yml` in `/opt/smartdns`:
```yaml
services:
  sniproxy:
    image: alpine/sniproxy:latest
    container_name: sniproxy
    restart: always
    network_mode: host
    volumes:
      - ./config/sniproxy.conf:/etc/sniproxy.conf:ro
```
Launch the container:
```bash
docker compose up -d
```

#### Step 4: Configure Live Query Sniffer Service
Create `/etc/systemd/system/smartdns-sniffer.service`:
```ini
[Unit]
Description=SmartDNS Client Query Sniffer
After=network.target

[Service]
Type=simple
User=root
ExecStart=/bin/sh -c 'exec /usr/bin/tcpdump -l -U -n -tttt -i any "udp dst port 53" >> /var/log/smartdns_queries.log'
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```
Enable and start the service:
```bash
touch /var/log/smartdns_queries.log
chmod 666 /var/log/smartdns_queries.log
systemctl daemon-reload
systemctl enable --now smartdns-sniffer
```

#### Step 5: Start the FastAPI Management Web Dashboard
```bash
cd /opt/smartdns
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run initial setup script
python3 setup_db.py

# Create systemd service for web panel
cat << 'EOF' > /etc/systemd/system/smartdns-panel.service
[Unit]
Description=SmartDNS FastAPI Management Panel
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/smartdns
ExecStart=/opt/smartdns/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8080
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now smartdns-panel
```
</details>

---

### 🔍 Verification & Health Check

After installation finishes, verify all services are running properly:

```bash
# 1. Check container and systemd status
docker ps --filter name=sniproxy
systemctl is-active smartdns-panel smartdns-sniffer

# 2. Check firewall whitelist
ipset list gamers

# 3. Test DNS resolution locally
dig @127.0.0.1 cod.activision.com +short
# Should return your server's public IP!
```

---

### 🔄 Upgrading to Newer Versions

To pull updates and apply schema migrations:

```bash
cd /opt/smartdns
git pull
systemctl restart smartdns-panel
```

## ☁️ Cloudflare Domain, DNS & SSL/TLS Configuration Guide

By integrating your SmartDNS server behind **Cloudflare**, you get **free automated SSL/TLS certificates**, **enterprise DDoS mitigation**, and a **clean domain URL without exposing ugly port numbers** (e.g., accessing `https://dns.yourdomain.com/admin` directly without `:8080`).

### 1. DNS Architecture: Web Panel vs. Game Clients

It is crucial to understand the separation between the **Web Management Panel** and the **Client DNS Engine**:

| Component | Target Address | Cloudflare Proxy Mode | Purpose |
| :--- | :--- | :--- | :--- |
| **Admin & Reseller Panel** | `dns.yourdomain.com` | **Proxied (Orange Cloud ☁️)** | Web browser access with HTTPS, SSL, and DDoS shielding |
| **Client Activation Link** | `dns.yourdomain.com/activate?...` | **Proxied (Orange Cloud ☁️)** | Users open on mobile/PC to auto-whitelist home IP |
| **Console / PC DNS Settings**| `YOUR_SERVER_PUBLIC_IP` | **Direct IP (No CDN)** | UDP Port 53 query engine; consoles require raw IPv4 |
| **SNI Proxy (Auth/Game)** | `YOUR_SERVER_PUBLIC_IP` | **Direct IP (No CDN)** | Port 443 TLS handshake spoofed for game auth servers |

---

### 2. Step-by-Step Cloudflare Setup

#### Step A: Add DNS A-Record
In your **Cloudflare Dashboard** ➡️ Select your domain ➡️ Go to **DNS** ➡️ **Records**:
1. Click **Add Record**.
2. **Type:** `A`
3. **Name:** `dns` (or `cod` or `@` for root domain)
4. **IPv4 Address:** Enter your server's public IP (`YOUR_SERVER_IP`)
5. **Proxy status:** Toggle to **Proxied (Orange Cloud ☁️)**
6. **TTL:** Set to **Auto**
7. Click **Save**.

#### Step B: Configure SSL/TLS Encryption
In your **Cloudflare Dashboard** ➡️ Go to **SSL/TLS**:
1. Under **Overview**, set the encryption mode to **Full** (or **Flexible** if you have not configured local SSL certificates on the VPS).
2. Go to **SSL/TLS** ➡️ **Edge Certificates**:
   * Enable **Always Use HTTPS** (automatically redirects HTTP to HTTPS).
   * Enable **Automatic HTTPS Rewrites**.
   * Set **Minimum TLS Version** to **TLS 1.2** (or **TLS 1.3**).

#### Step C: Remove Port 8080 Using Cloudflare Origin Rules
By default, the FastAPI dashboard runs on port `8080`. Cloudflare's standard proxy listens on ports `80` and `443`. Rather than exposing port `:8080` in user links or configuring complex NGINX reverse proxies on your VPS, you can use **Cloudflare Origin Rules** to rewrite the destination port in the cloud for free:

1. In your **Cloudflare Dashboard**, navigate to **Rules** ➡️ **Origin Rules**.
2. Click **Create Rule**.
3. Fill in the rule details:
   * **Rule name:** `SmartDNS Admin Panel Port Rewrite`
4. In the **Incoming requests** section:
   * Select **Custom filter expression**
   * **Field:** `Hostname`
   * **Operator:** `equals`
   * **Value:** `dns.yourdomain.com` (your subdomain configured in Step A)
5. In the **Destination Port** section:
   * Select **Rewrite to...**
   * Select **Port** and enter: **`8080`**
6. Click **Deploy**.

> **Result:** Your FastAPI management panel and 1-click IP activation links can now be accessed cleanly at:
> - `https://dns.yourdomain.com/admin`
> - `https://dns.yourdomain.com/activate?token=...`
>
> Cloudflare automatically handles the SSL handshake at the edge, routes port 443 traffic directly to port 8080 on your VPS origin, and hides your backend infrastructure!

---

#### Step D (Optional): WAF Rate Limiting & Admin Security
To safeguard your admin panel against brute-force attacks from unauthorized countries:
1. In Cloudflare ➡️ **Security** ➡️ **WAF** ➡️ **Rate limiting rules**:
   * Create a rule for URI path containing `/admin/login`.
   * Set threshold to 5 requests per 10 seconds.
   * Action: **Block** for 1 hour.
2. In Cloudflare ➡️ **Security** ➡️ **WAF** ➡️ **Custom rules**:
   * Block requests to `/admin` that do not originate from your administrator's country.

---

## 🎮 Client Configuration Guide

Clients configure their device once by setting the Primary DNS to your server IP:

```text
Primary DNS:   YOUR_SERVER_IP
Secondary DNS: 1.1.1.1 (or 8.8.8.8)
```

<details>
<summary><b>🖥️ Windows 10 / 11 Setup</b></summary>

1. Press <kbd>Win</kbd> + <kbd>R</kbd>, type `ncpa.cpl`, and press **Enter**.
2. Right-click your active network adapter (Ethernet or Wi-Fi) ➡️ select **Properties**.
3. Double-click **Internet Protocol Version 4 (TCP/IPv4)**.
4. Select **Use the following DNS server addresses**:
   * **Preferred DNS server:** `YOUR_SERVER_IP`
   * **Alternate DNS server:** `1.1.1.1`
5. Click **OK** ➡️ **OK**.
6. Open your browser and visit your unique activation link to whitelist your public IP.
</details>

<details>
<summary><b>🎮 PlayStation 5 (PS5) & PlayStation 4 (PS4) Setup</b></summary>

1. Navigate to **Settings** ➡️ **Network** ➡️ **Settings** ➡️ **Set Up Internet Connection**.
2. Highlight your connected Wi-Fi or LAN connection and press the **Options button** (3 lines) on the controller.
3. Select **Advanced Settings**.
4. Set **DNS Settings** to **Manual**.
5. Enter:
   * **Primary DNS:** `YOUR_SERVER_IP`
   * **Secondary DNS:** `1.1.1.1`
6. Leave other settings on Automatic and select **OK**.
7. Test the connection. Ensure your home IP is activated via your personal link.
</details>

<details>
<summary><b>🟩 Xbox Series X / S & Xbox One Setup</b></summary>

1. Press the Xbox button on the controller ➡️ select **Profile & system** ➡️ **Settings**.
2. Go to **General** ➡️ **Network settings** ➡️ **Advanced settings**.
3. Select **DNS settings** ➡️ choose **Manual**.
4. Enter:
   * **Primary IPv4 DNS:** `YOUR_SERVER_IP`
   * **Secondary IPv4 DNS:** `1.1.1.1`
5. Save settings and restart the console.
</details>

<details>
<summary><b>🍎 macOS Setup</b></summary>

1. Open **System Settings** ➡️ **Network**.
2. Select your active Wi-Fi or Ethernet connection and click **Details...**.
3. Select the **DNS** tab on the left.
4. Click the `+` button under DNS Servers and add `YOUR_SERVER_IP` at the top, followed by `1.1.1.1`.
5. Click **OK** and **Apply**.
</details>

<details>
<summary><b>📱 iOS & Android Mobile Setup</b></summary>

* **iOS:** Open **Settings** ➡️ **Wi-Fi** ➡️ Tap the `(i)` icon next to your network ➡️ **Configure DNS** ➡️ Select **Manual** ➡️ Add `YOUR_SERVER_IP`.
* **Android:** Open **Settings** ➡️ **Network & internet** ➡️ **Wi-Fi** ➡️ Tap your network gear icon ➡️ **Advanced options** ➡️ Change IP settings to **Static** ➡️ Set DNS 1 to `YOUR_SERVER_IP`.
</details>

---

<h2 id="-system-requirements">💻 System Requirements</h2>

| Component | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **Operating System** | Ubuntu 22.04 LTS (x86_64) | Ubuntu 24.04 LTS (x86_64) |
| **CPU** | 1 vCPU Core | 2 vCPU Cores |
| **RAM** | 1 GB RAM | 2 GB+ RAM |
| **Disk Space** | 10 GB Free Storage | 20 GB SSD / NVMe |
| **Firewall Ports** | 53 (UDP/TCP), 443 (TCP), 8080 (TCP) | Same (Protected by `ipset` & Cloudflare) |

---

<h2 id="️-security-hardening--privacy">🛡️ Security, Hardening & Privacy</h2>

* **Kernel-Level `ipset` Filtering:** Only validated public IPs listed in the `gamers` IP set can communicate with DNS (53) and SNI (443). Arbitrary Internet scanners and Shodan probes receive silent packet drops.
* **Fail2ban Integration:** Automatic brute-force protection active on SSH and admin login endpoints.
* **Database Isolation:** SQLite database stored with strict file permissions (`chmod 600 users.db`).
* **Automated Daily Backups:** Automated daily snapshots of user lists, reseller quotas, and configuration files stored in `/opt/smartdns/backups/`.
* **DNS Query Rate Limiting:** Anti-flood rules enforce a maximum of 50 DNS queries/sec per client IP.
* **Zero Telemetry:** 100% self-contained. No external telemetry, phone-home beacons, or user activity tracking.

---

<div align="center" style="text-align: center;">
  <h2 align="center" style="text-align: center;">🌟 Support & Community</h2>

  <p align="center" style="text-align: center;">
    If Gaming SmartDNS helps you lower your ping or bypass sanctions, please star the repository!
  </p>

  <p align="center">
    <a href="https://github.com/farzadrahnama/gaming-smartdns">
      <img src="https://img.shields.io/github/stars/farzadrahnama/gaming-smartdns?style=for-the-badge&label=Star%20on%20GitHub&color=yellow&logo=github" alt="Star on GitHub">
    </a>
  </p>

  <hr>

  <p align="center" style="text-align: center;">
    <strong>Architected & Maintained by Farzad Rahnama</strong><br>
    <a href="https://github.com/farzadrahnama"><img alt="GitHub: farzadrahnama" src="https://img.shields.io/badge/GitHub-farzadrahnama-24292e?style=flat-square&logo=github"></a>&nbsp;<a href="https://www.linkedin.com/in/farzadrahnama/"><img alt="LinkedIn: farzadrahnama" src="https://img.shields.io/badge/LinkedIn-farzadrahnama-0A66C2?style=flat-square&logo=linkedin"></a>&nbsp;<a href="https://github.com/farzadrahnama/gaming-smartdns/issues"><img alt="Open Issues" src="https://img.shields.io/github/issues/farzadrahnama/gaming-smartdns?style=flat-square"></a><br>
    <sub>&copy; Farzad Rahnama. Released under the open-source MIT License.</sub>
  </p>
</div>
