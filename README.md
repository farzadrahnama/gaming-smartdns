# 🎮 SmartDNS & SNI Proxy Hub

[![GitHub stars](https://img.shields.io/github/stars/farzadrahnama/gaming-smartdns?style=social)](https://github.com/farzadrahnama/gaming-smartdns)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen)](https://www.python.org/)

A high-performance, private **SmartDNS and SNI Proxy** solution designed to bypass geo-restrictions, sanctions, and matchmaking blocks on gaming networks (**Call of Duty, PlayStation Network, EA/Apex, Blizzard, Epic Games**) and AI platforms (**ChatGPT, Claude, Gemini, Antigravity**).

Includes a modern **FastAPI Admin Dashboard**, **Reseller / Sub-Admin multi-tenant system**, **Firewall IP whitelisting (`ipset`)**, and **Live Traffic Monitoring**.

---

## 🏗️ Architecture

```text
[User Device (PC / PS5 / Xbox)]
       │ (Port 53 DNS Query)
       ▼
[Firewall: ipset (gamers)]
       ├── Unregistered IP  ──► ⛔ Silently DROPPED (No Response)
       └── Whitelisted IP   ──► ✅ Accepted
                                     │
                        ┌────────────┴────────────┐
                        ▼                         ▼
              [Sanctioned Game/AI]         [Normal Internet]
              Resolved to Proxy IP         Resolved via 1.1.1.1
                        │                         │
                        ▼                         ▼
                 [SNI Proxy: 443]          [Direct Connection]
