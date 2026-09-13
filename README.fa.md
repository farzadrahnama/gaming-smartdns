<div align="center" style="text-align: center;">
  <p><a href="README.md"><strong>English</strong></a> &nbsp;|&nbsp; <a href="README.fa.md"><strong>فارسی</strong></a></p>
  <h1 align="center" style="text-align: center;">🎮 سامانه هوشمند SmartDNS و SNI Proxy گیمینگ</h1>
  <p align="center" style="text-align: center;">
    <strong>پینگ صفر و بدون تاخیر &bull; بدون افت سرعت در بازی &bull; پنل مدیریت چندکاربره و نمایندگی &bull; فایروال پویا با ipset &bull; سازگار با کلودفلر</strong><br>
    <em>سامانه فوق‌سریع و امن SmartDNS و پروکسی SNI طراحی‌شده برای دور زدن تحریم‌های گیمینگ و پلتفرم‌های هوش مصنوعی.</em>
  </p>
  <p align="center" style="text-align: center;">
    <a href="https://github.com/farzadrahnama/gaming-smartdns/releases/latest"><img alt="Latest Release v2.5.0" src="https://img.shields.io/badge/Release-v2.5.0-0078D4?style=flat-square&logo=github&logoColor=white"></a>&nbsp;<a href="https://github.com/farzadrahnama/gaming-smartdns"><img alt="GitHub Stars" src="https://img.shields.io/github/stars/farzadrahnama/gaming-smartdns?style=flat-square&color=yellow&logo=github"></a>&nbsp;<a href="https://opensource.org/licenses/MIT"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green?style=flat-square"></a><br><a href="#-نیازمندیهای-سیستم"><img alt="Ubuntu 22.04 / 24.04" src="https://img.shields.io/badge/Ubuntu-22.04%20%2F%2024.04-E95420?style=flat-square&logo=ubuntu&logoColor=white"></a>&nbsp;<a href="#-نیازمندیهای-سیستم"><img alt="Docker Engine Ready" src="https://img.shields.io/badge/Docker-Engine%20Ready-2496ED?style=flat-square&logo=docker&logoColor=white"></a>&nbsp;<a href="#-نیازمندیهای-سیستم"><img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white"></a>&nbsp;<a href="#-امنیت-سختازاری-و-حریم-خصوصی"><img alt="Firewall: ipset hardened" src="https://img.shields.io/badge/Firewall-ipset%20hardened-success?style=flat-square"></a>
  </p>
  <p align="center" style="text-align: center;">
    <sub><strong>بدون افزایش پینگ در بازی</strong> &bull; فقط هدایت ترافیک لایسنس و احراز هویت &bull; اتصال مستقیم UDP در مسابقات &bull; کنسول‌های PS5 / Xbox و کامپیوتر</sub>
  </p>
</div>

---

<div dir="rtl" align="right">

## 🚀 معرفی و هدف پروژه

گیمرهای رقابتی و کاربران ایرانی همواره با چالش‌های تحریم‌های خارجی، خطاهای اتصال (Matchmaking Errors) و مسدودیت‌های اعمال‌شده روی پلتفرم‌های اصلی بازی نظیر **Call of Duty (Warzone, MW3, BO6)**، **EA Sports FC / Apex Legends**، **PlayStation Network (PSN)**، **Xbox Live**، **Blizzard Battle.net** و **Epic Games** روبه‌رو هستند. از سوی دیگر، دسترسی به سرویس‌های هوش مصنوعی پیشرفته نظیر **ChatGPT, Claude, Gemini, Antigravity** نیازمند دور زدن محدودیت‌های منطقه‌ای است.

استفاده از وی‌پی‌ان‌های معمولی (VPN) باعث عبور **تمام** بسته‌های اینترنت (شامل ترافیک سنگین چت صوتی و داده‌های UDP گیم‌پلی) از تونل رمزنگاری می‌شود که حاصل آن **افزایش شدید پینگ (+۵۰ تا +۱۵۰ میلی‌ثانیه)، پکت لاست (Packet Loss)، نوسان جیتر و خطر مسدود شدن اکانت توسط سیستم‌های آنتی‌چیت (Anti-Cheat)** است.

**سامانه Gaming SmartDNS & SNI Proxy** این مشکل را به شکل مهندسی‌شده و قطعی حل می‌کند:
1. **تفکیک هوشمند در لایه DNS:** تنها آدرس‌های لاگین، لایسنس و مچ‌میکینگ که تحریم هستند به پروکسی SNI هدایت می‌شوند.
2. **پینگ کاملاً طبیعی و بدون تغییر (0ms Added Ping):** کل بسته‌های UDP درون بازی و چت صوتی، **۱۰۰٪ به صورت مستقیم و بدون واسطه** میان کنسول/کامپیوتر شما و نزدیک‌ترین سرور بازی تبادل می‌شوند.
3. **مدیریت پیشرفته و خودکار:** دارای داشبورد تحت وب مدرن **FastAPI**، **سیستم نمایندگی و ساب‌ادمین**، **فایروال هسته لینوکس (`ipset`)** و **مانیتورینگ زنده ترافیک**.

---

## ✨ جدول مقایسه قابلیت‌ها در یک نگاه

| ویژگی | وی‌پی‌ان سنتی (VPN / V2Ray) | سامانه اختصاصی Gaming SmartDNS |
| :--- | :--- | :--- |
| **تاثیر بر پینگ داخل بازی** | افزایش پینگ بین ۴۰ تا ۱۲۰ میلی‌ثانیه | **دقیقاً صفر میلی‌ثانیه (بدون هیچ‌گونه تاخیر اضافی)** |
| **نوسان پکت (Jitter & Loss)** | بالا به دلیل سربار رمزنگاری تونل | **مشابه اینترنت مستقیم و بومی سرویس‌دهنده** |
| **مصرف ترافیک و هزینه سرور** | بسیار سنگین (۵۰ تا ۱۰۰ گیگابایت در ماه برای هر کاربر) | **بسیار ناچیز (کمتر از ۱ گیگابایت در ماه)**؛ دانلود بازی‌ها مستقیم است |
| **ریسک مسدودیت توسط آنتی‌چیت**| بالا (شناسایی آی‌پی دیتاسنتر توسط Ricochet/Vanguard) | **کاملاً صفر و امن** (اتصال مسابقه بازی مستقیماً با سرور اصلی است) |
| **پشتیبانی از کنسول‌ها (PS4/PS5/Xbox)** | نیازمند روتر پیشرفته، مودم OpenWrt یا اشتراک هات‌اسپات | **پشتیبانی بومی**؛ تنها با تنظیم ۲ عدد IP در منوی DNS کنسول |
| **سیستم نمایندگی (Resellers)** | ساخت دستی کانفیگ یا پنل‌های سنگین متفرقه | **پنل اختصاصی چندکاربره** با سهمیه مشخص برای هر نماینده |
| **امنیت در برابر اسکنرها و حملات**| پورت‌های باز در معرض حملات DDoS و اسکنرهای اینترنت | **فایروال لایه هسته با `ipset`**؛ دراپ خاموش بسته‌های ناشناس |
| **مدیریت IP داینامیک کاربران** | نیازمند اجرای نرم‌افزار دائمی روی دستگاه کاربر | **لینک اختصاصی فعال‌سازی با یک کلیک** (برای گوشی یا روتر) |
| **مشاهده لاگ‌های بازی** | بررسی ترافیک نیازمند ابزارهای پیشرفته کپچر است | **مانیتورینگ زنده لاگ‌ها** و کوئری‌های DNS در حال ارسال |
| **رابط کاربری وب** | محیط متنی یا پنل‌های شلوغ و کند | **داشبورد زیبا، ریسپانسیو و تاریک با FastAPI** |

---

## 🏗️ معماری و نحوه گردش ترافیک

```text
[دستگاه کاربر: کامپیوتر / PS5 / Xbox / موبایل]
       │
       ▼ (ارسال کوئری DNS روی پورت 53)
[فایروال هسته لینوکس: ipset (gamers)]
       ├── 🚫 آی‌پی ثبت‌نشده  ──► مسدودسازی کامل و خاموش (Zero DDoS footprint)
       └── ✅ آی‌پی تاییدشده ──► هدایت به موتور SmartDNS
                                            │
                             ┌──────────────┴──────────────┐
                             ▼                             ▼
                    [دامنه‌های تحریمی بازی/هوش مصنوعی]      [ترافیک عادی اینترنت]
                     پاسخ با IP سرور پروکسی                   پاسخ مستقیم از 1.1.1.1
                             │                             │
                             ▼                             ▼
                    [پروکسی SNI روی پورت 443]            [اتصال مستقیم به اینترنت]
                    عبور شفاف هدر TLS بدون دستکاری          (دانلود آپدیت و وبگردی)
                             │
                             ▼
               [سرور رسمی احراز هویت بازی / ناشر]
                             │
                             ▼ (پایان ورود و پیدا شدن بازی)
               [اتصال به سرور مچ بازی (بسته‌های UDP پورت 3074 / 27015 و...)]
               ═════════════════════════════════════════════════════════════► اتصال مستقیم با پینگ بومی (۰ میلی‌ثانیه تاخیر!)
```

---

## 🔍 بررسی بخش‌های فنی و ویژگی‌ها

### ۱. هسته سبک SmartDNS و SNI Proxy
* **بدون رمزگشایی و افت سرعت پردازنده:** پروکسی SNI فقط هدر ابتدایی درخواست TLS (ClientHello) را بررسی کرده و ترافیک را شفاف عبور می‌دهد. پردازنده سرور حتی با صدها کاربر هم‌زمان کمترین لود را تجربه می‌کند.
* **بانک دامنه‌های پیش‌تنظیم شده:** پیکربندی شده برای بازی‌های اکتیویژن، کالاف دیوتی، فیفا/ای‌ای اسپورتس، اپکس، بتل‌نت، اپیک‌گیمز، رایت گیمز، پلی‌استیشن نتورک، اکس‌باکس لایو و هوش‌مصنوعی‌های OpenAI، Claude و Google.
* **فوروارد هوشمند:** تمام دامنه‌های عمومی اینترنت مستقیماً از کلودفلر (`1.1.1.1`) بدون کوچک‌ترین تاخیر یا مصرف پهنای باند پاسخ داده می‌شوند.

### ۲. پنل مدیریت پیشرفته با FastAPI
* **مدیریت سطوح دسترسی (RBAC):** دارای دو لایه کاربری مدیر اصلی (Super-Admin) و نمایندگان فروش (Resellers).
* **سیستم سهمیه‌بندی نمایندگان:** ساب‌ادمین‌ها می‌توانند کاربران خود را با سهمیه معین ثبت، تمدید، غیرفعال یا حذف کنند بدون آنکه به تنظیمات اصلی سرور دسترسی داشته باشند.
* **طراحی مدرن در حالت شب (Dark Mode):** رابط کاربری تمیز و سریع سازگار با موبایل و دسکتاپ.
* **سیستم تغییر رمز عبور امن:** با ذخیره‌سازی هش bcrypt و فرم اختصاصی داخل پنل.

### ۳. سیستم احراز هویت داینامیک و فایروال ipset
* **حفاظت کامل پورت‌ها:** پورت‌های ۵۳ (DNS) و ۴۴۳ (SNI) روی اینترنت برای افراد ناشناس کاملاً مسدود هستند تا مانع از حملات منع سرویس (DDoS Amplification) شود.
* **لینک فعال‌سازی خودکار:** هر کاربر یک آدرس یکتا دارد (`https://your-domain.com/activate?token=...`). با باز کردن این آدرس روی هر موبایل یا سیستمی در شبکه خانگی، آی‌پی پابلیک وی به مدت ۳۰ روز در لیست مجاز فعال می‌شود.

### ۴. اسنیفر و مانیتورینگ زنده ترافیک
* **مشاهده کوئری‌های DNS در لحظه:** در صفحه لاگ‌ها (`/admin/logs`) می‌توانید دامنه‌هایی را که کنسول یا سیستم کاربر هنگام باز کردن بازی فراخوانی می‌کند به شکل زنده ببینید.
* **عیب‌یابی سریع:** اگر دامنه‌ای در بازی جدید تغییر کند، بلافاصله در لاگ مشخص شده و با یک خط کانفیگ به لیست اضافه می‌گردد.

---

## 📦 راهنمای جامع نصب و راه‌اندازی

شما می‌توانید سامانه Gaming SmartDNS را به دو روش **نصب خودکار با ۱ کلیک** (پیشنهاد شده برای سرورهای عملیاتی) یا **نصب دستی گام‌به‌گام** مستقر نمایید.

---

### 📋 پیش‌نیازها و پورت‌های مورد نیاز سرور

قبل از شروع نصب، اطمینان حاصل کنید که فایروال ارائه‌دهنده سرور ابری شما (مانند Hetzner، DigitalOcean، یا کلود کلاودفلر) ترافیک پورت‌های زیر را مسدود نکرده باشد:

| پورت | پروتکل | کاربرد و سرویس | سیاست دسترسی امنیتی |
| :--- | :--- | :--- | :--- |
| **53** | `UDP` / `TCP` | سرور DNS هوشمند | فقط کاربران مجاز (کنترل‌شده با `ipset`) |
| **443** | `TCP` | پروکسی شفاف SNI | فقط کاربران مجاز (کنترل‌شده با `ipset`) |
| **8080** | `TCP` | پنل تحت وب مدیریت FastAPI | فقط آی‌پی‌های کلودفلر (از طریق Origin Rules) |
| **22** | `TCP` | مدیریت سرور از طریق SSH | پایش‌شده توسط سیستم محافظتی `fail2ban` |

> [!NOTE]
> سیستم‌عامل‌های پشتیبانی‌شده: **Ubuntu 22.04 LTS** یا **Ubuntu 24.04 LTS** (معماری x86_64 یا ARM64) با دسترسی کاربر `root`.

---

### ⚡ روش اول: نصب خودکار و سریع با ۱ کلیک (پیشنهادی)

با دسترسی `root` وارد سرور ابری خام خود شوید و دستورات زیر را اجرا کنید:

```bash
# ۱. کلون کردن ریپازیتوری در مسیر /opt/smartdns
git clone https://github.com/farzadrahnama/gaming-smartdns.git /opt/smartdns
cd /opt/smartdns

# ۲. اعطای مجوز اجرا و شروع اسکریپت نصب
chmod +x install.sh
bash install.sh
```

#### اسکریپت نصب خودکار چه اقداماتی انجام می‌دهد؟
۱. **آماده‌سازی پکیج‌های سیستم:** مخازن اوبونتو را به‌روز کرده و ابزارهای لازم (`curl`, `git`, `ipset`, `iptables-persistent`, `tcpdump`, `fail2ban`, `python3-pip`) را نصب می‌کند.
۲. **نصب محیط داکر:** موتور Docker و پلاگین داکر کامپوز را پیکربندی می‌کند.
۳. **سخت‌سازی فایروال هسته لینوکس:**
   * مجموعه آی‌پی `ipset create gamers hash:ip` را می‌سازد.
   * قوانین `iptables` را برای مسدودسازی خودکار افراد ناشناس روی پورت‌های ۵۳ و ۴۴۳ اعمال می‌کند.
   * ذخیره‌سازی همیشگی قوانین در زمان ریستارت سرور (`netfilter-persistent save`).
۴. **راه‌اندازی پروکسی SNI:** کانتینر پرسرعت `sniproxy` را روی پورت ۴۴۳ بالا می‌آورد.
۵. **موتور دی‌ان‌اس و اسنیفر زنده:** سرویس `smartdns-sniffer` را برای مانیتورینگ زنده ترافیک در `systemd` فعال می‌سازد.
۶. **پنل مدیریت تحت وب:** محیط مجازی پایتون را ایجاد، پیش‌نیازها را نصب، امنیت دیتابیس (`chmod 600 users.db`) را تامین و پنل را روی پورت ۸۰۸۰ اجرا می‌کند.
۷. **ساخت حساب مدیر اصلی:** نام کاربری و رمزعبور دلخواه شما برای ورود به پنل را تنظیم می‌کند.

---

### 🛠️ روش دوم: راهنمای نصب دستی و گام‌به‌گام

در صورتی که قصد شخصی‌سازی دستی تمام سرویس‌ها را دارید:

<details>
<summary><b>برای مشاهده دستورات نصب دستی کلیک کنید</b></summary>

#### گام ۱: نصب بسته‌های سیستم‌عامل
```bash
apt update && apt upgrade -y
apt install -y docker.io docker-compose-plugin python3 python3-pip python3-venv ipset iptables-persistent tcpdump fail2ban curl git
```

#### گام ۲: تنظیم فایروال لایه هسته (`ipset`)
```bash
# ایجاد مجموعه آی‌پی‌های تاییدشده با انقضای ۳۰ روزه
ipset create gamers hash:ip timeout 2592000

# مجاز کردن لوپ‌بک و ارتباطات موجود
iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT

# مجاز کردن دی‌ان‌اس (۵۳) و اس‌ان‌آی (۴۴۳) فقط برای آی‌پی‌های موجود در لیست
iptables -A INPUT -p udp --dport 53 -m set --match-set gamers src -j ACCEPT
iptables -A INPUT -p tcp --dport 53 -m set --match-set gamers src -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -m set --match-set gamers src -j ACCEPT

# مسدودسازی کامل هرگونه درخواست متفرقه و اسکنرهای اینترنت
iptables -A INPUT -p udp --dport 53 -j DROP
iptables -A INPUT -p tcp --dport 53 -j DROP
iptables -A INPUT -p tcp --dport 443 -j DROP

# ذخیره دائمی قوانین فایروال
netfilter-persistent save
```

#### گام ۳: راه‌اندازی کانتینر SNI Proxy
فایل `docker-compose.yml` را در مسیر `/opt/smartdns` ایجاد کنید:
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
کانتینر را اجرا کنید:
```bash
docker compose up -d
```

#### گام ۴: راه‌اندازی سرویس مانیتورینگ زنده ترافیک
فایل `/etc/systemd/system/smartdns-sniffer.service` را بسازید:
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
فعال‌سازی سرویس:
```bash
touch /var/log/smartdns_queries.log
chmod 666 /var/log/smartdns_queries.log
systemctl daemon-reload
systemctl enable --now smartdns-sniffer
```

#### گام ۵: راه‌اندازی پنل وب با FastAPI
```bash
cd /opt/smartdns
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# ساخت دیتابیس اولیه
python3 setup_db.py

# ساخت سرویس systemd برای پنل وب
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

### 🔍 تست صحت عملکرد سرویس‌ها پس از نصب

برای اطمینان از بالا آمدن تمام بخش‌ها:

```bash
# ۱. بررسی وضعیت کانتینر و سرویس‌های لینوکس
docker ps --filter name=sniproxy
systemctl is-active smartdns-panel smartdns-sniffer

# ۲. مشاهده آی‌پی‌های تاییدشده در فایروال
ipset list gamers

# ۳. تست لوکال کوئری دی‌ان‌اس بازی
dig @127.0.0.1 cod.activision.com +short
# باید آی‌پی پابلیک سرور شما را بازگرداند!
```

---

### 🔄 به‌روزرسانی سیستم به نسخه‌های جدیدتر

برای دریافت آخرین تغییرات و به‌روزرسانی پنل:

```bash
cd /opt/smartdns
git pull
systemctl restart smartdns-panel
```

---

## ☁️ راهنمای جامع تنظیم دامنه، دی‌ان‌اس و گواهی SSL در کلودفلر (Cloudflare)

با قرار دادن سرور خود پشت **Cloudflare**، علاوه بر دریافت **گواهی امنیتی رایگان SSL/TLS** و **محافظت در برابر حملات DDoS**، می‌توانید پنل مدیریت را روی دامنه‌ای شیک و بدون نیاز به وارد کردن پورت ۸۰۸۰ باز کنید (مانند `https://dns.yourdomain.com/admin` به جای `:8080`).

### ۱. معماری DNS: پنل مدیریت تحت وب در برابر ترافیک بازی کنسول‌ها

درک تفکیک بین ترافیک وب پنل و ترافیک شبکه کنسول‌ها بسیار ضروری است:

| بخش | آدرس هدف | حالت پروکسی کلودفلر | هدف و کاربرد |
| :--- | :--- | :--- | :--- |
| **پنل مدیریت و نمایندگان** | `dns.yourdomain.com` | **روشن / ابری نارنجی (Proxied ☁️)** | باز کردن با مرورگر وب، گواهی SSL، و محافظت از IP اصلی سرور |
| **لینک فعال‌سازی کلاینت‌ها** | `dns.yourdomain.com/activate?...` | **روشن / ابری نارنجی (Proxied ☁️)** | کاربران روی گوشی یا سیستم باز کرده تا آی‌پی آن‌ها مجاز شود |
| **تنظیم DNS کنسول / ویندوز**| `YOUR_SERVER_PUBLIC_IP` | **آی‌پی مستقیم (بدون کلودفلر)** | پروتکل UDP پورت ۵۳؛ کنسول‌ها باید مستقیم به سرور متصل شوند |
| **پروکسی SNI بازی** | `YOUR_SERVER_PUBLIC_IP` | **آی‌پی مستقیم (بدون کلودفلر)** | هندشیک TLS پورت ۴۴۳ بازی‌ها که توسط SmartDNS جعل می‌شود |

---

### ۲. مراحل گام‌به‌گام تنظیمات کلودفلر

#### گام اول: ایجاد رکورد DNS نوع A
در **داشبورد کلودفلر** ➡️ دامنه خود را انتخاب کنید ➡️ بخش **DNS** ➡️ منوی **Records**:
۱. روی دکمه **Add Record** کلیک کنید.
۲. **Type:** نوع را `A` انتخاب کنید.
۳. **Name:** ساب‌دامنه دلخواه (مثلاً `dns` یا `cod` یا `@` برای دامنه اصلی).
۴. **IPv4 Address:** آدرس IP پابلیک سرور خود را وارد کنید (`YOUR_SERVER_IP`).
۵. **Proxy status:** حتماً **روشن / ابری نارنجی (Proxied ☁️)** باشد.
۶. **TTL:** روی حالت **Auto** باشد.
۷. دکمه **Save** را بزنید.

#### گام دوم: تنظیمات رمزنگاری SSL/TLS
در **داشبورد کلودفلر** ➡️ منوی **SSL/TLS**:
۱. در تب **Overview** حالت رمزنگاری را روی **Full** (یا **Flexible**) قرار دهید.
۲. در تب **Edge Certificates**:
   * گزینه **Always Use HTTPS** را روشن کنید (انتقال خودکار از HTTP به HTTPS).
   * گزینه **Automatic HTTPS Rewrites** را روشن کنید.
   * مقدار **Minimum TLS Version** را روی **TLS 1.2** بگذارید.

#### گام سوم: حذف پورت 8080 با قانون Origin Rules
پنل مدیریت FastAPI به صورت پیش‌فرض روی پورت `8080` اجرا می‌شود. به جای درگیر شدن با وب‌سرورهای سنگین Nginx یا باز گذاشتن پورت‌های غیراستاندارد در مرورگر، کلودفلر به صورت رایگان ترافیک ورودی را به پورت ۸۰۸۰ سرور ریرایت می‌کند:

۱. در **داشبورد کلودفلر** ➡️ منوی **Rules** ➡️ زیرمنوی **Origin Rules**.
۲. روی دکمه **Create Rule** کلیک کنید.
۳. فیلدها را به این صورت تکمیل کنید:
   * **Rule name:** نام دلخواه بنویسید (مثلاً `SmartDNS Admin Panel Port Rewrite`).
۴. در بخش **Incoming requests**:
   * گزینه **Custom filter expression** را تیک بزنید.
   * **Field:** مقدار `Hostname`
   * **Operator:** مقدار `equals`
   * **Value:** ساب‌دامنه خود را وارد کنید (مثلاً `dns.yourdomain.com`).
۵. در بخش **Destination Port**:
   * گزینه **Rewrite to...** را انتخاب کنید.
   * پورت را وارد کنید: **`8080`**
۶. روی دکمه **Deploy** کلیک کنید.

> **نتیجه:** از این پس پنل مدیریت و لینک‌های فعال‌سازی به زیباترین شکل با آدرس امن در دسترس هستند:
> - `https://dns.yourdomain.com/admin`
> - `https://dns.yourdomain.com/activate?token=...`
>
> کلودفلر تمام ارتباطات SSL را مدیریت کرده و پورت ۴۴۳ را در پس‌زمینه به پورت ۸۰۸۰ سرور شما هدایت می‌کند!

---

#### گام چهارم (اختیاری): افزایش امنیت پنل ادمین با WAF
برای جلوگیری از حملات Brute-Force روی صفحه ورود:
۱. در کلودفلر ➡️ بخش **Security** ➡️ **WAF** ➡️ تب **Rate limiting rules**:
   * قانونی بسازید که مسیر `/admin/login` در صورت بیش از ۵ بار تلاش در ۱۰ ثانیه به مدت ۱ ساعت مسدود شود.
۲. در تب **Custom rules**:
   * می‌توانید دسترسی به مسیر `/admin` را فقط به کشورهای مشخص یا IPهای خاص محدود کنید.

---

## 🎮 راهنمای تنظیم کلاینت‌ها (کنسول و کامپیوتر)

کاربران کافی است یک‌بار DNS دستگاه خود را روی آی‌پی سرور شما تنظیم نمایند:

```text
Primary DNS (دی‌ان‌اس اول):    YOUR_SERVER_IP
Secondary DNS (دی‌ان‌اس دوم):  1.1.1.1 (یا 8.8.8.8)
```

<details>
<summary><b>🖥️ راهنمای ویندوز ۱۰ و ۱۱</b></summary>

۱. کلیدهای <kbd>Win</kbd> + <kbd>R</kbd> را بزنید، تایپ کنید `ncpa.cpl` و Enter بزنید.
۲. روی کارت شبکه فعال خود (Ethernet یا Wi-Fi) راست‌کلیک کرده و **Properties** را انتخاب کنید.
۳. روی گزینه **Internet Protocol Version 4 (TCP/IPv4)** دوبار کلیک کنید.
۴. گزینه **Use the following DNS server addresses** را فعال کرده و مقادیر بالا را وارد کنید.
۵. دکمه **OK** را بزنید.
۶. سپس لینک فعال‌سازی اختصاصی خود را در مرورگر باز کنید تا آی‌پی شما مجاز شود.
</details>

<details>
<summary><b>🎮 راهنمای پلی‌استیشن ۵ و ۴ (PS5 / PS4)</b></summary>

۱. به مسیر **Settings** ➡️ **Network** ➡️ **Settings** ➡️ **Set Up Internet Connection** بروید.
۲. روی شبکه فعال خود رفته و دکمه **Options** (سه خط روی دسته) را بزنید.
۳. گزینه **Advanced Settings** را انتخاب کنید.
۴. بخش **DNS Settings** را روی حالت **Manual** بگذارید.
۵. مقادیر را وارد کنید:
   * **Primary DNS:** آدرس IP سرور شما
   * **Secondary DNS:** `1.1.1.1`
۶. بقیه گزینه‌ها را روی اتوماتیک بگذارید و ذخیره کنید.
</details>

<details>
<summary><b>🟩 راهنمای ایکس‌باکس (Xbox Series X/S و Xbox One)</b></summary>

۱. دکمه Xbox روی دسته را بزنید ➡️ منوی **Profile & system** ➡️ گزینه **Settings**.
۲. وارد مسیر **General** ➡️ **Network settings** ➡️ **Advanced settings** شوید.
۳. گزینه **DNS settings** را زده و حالت **Manual** را برگزینید.
۴. مقادیر Primary و Secondary را وارد کرده و کنسول را یک‌بار Restart کنید.
</details>

<details>
<summary><b>🍎 راهنمای مک (macOS)</b></summary>

۱. به **System Settings** ➡️ **Network** بروید.
۲. روی شبکه متصل خود کلیک کرده و گزینه **Details...** را انتخاب کنید.
۳. از پنل سمت چپ روی تب **DNS** کلیک کنید.
۴. با زدن دکمه `+` در زیر بخش DNS Servers ابتدا آی‌پی سرور خود و سپس `1.1.1.1` را اضافه کنید و OK را بزنید.
</details>

<details>
<summary><b>📱 راهنمای اندروید و iOS</b></summary>

* **آیفون (iOS):** به تنظیمات ➡️ وای‌فای ➡️ علامت `(i)` کنار شبکه ➡️ بخش **Configure DNS** ➡️ انتخاب **Manual** ➡️ اضافه کردن آی‌پی سرور.
* **اندروید:** به تنظیمات ➡️ شبکه و اینترنت ➡️ وای‌فای ➡️ چرخ‌دنده کنار شبکه ➡️ در تنظیمات پیشرفته بخش IP Settings را روی **Static** قرار داده و DNS 1 را تنظیم کنید.
</details>

---

<h2 id="-نیازمندیهای-سیستم">💻 نیازمندی‌های سیستم</h2>

| قطعه / منبع | حداقل مشخصات | مشخصات پیشنهادی |
| :--- | :--- | :--- |
| **سیستم‌عامل** | Ubuntu 22.04 LTS (x86_64) | Ubuntu 24.04 LTS (x86_64) |
| **پردازنده (CPU)** | ۱ هسته مجازی | ۲ هسته مجازی |
| **حافظه رم (RAM)** | ۱ گیگابایت | ۲ گیگابایت یا بالاتر |
| **فضای دیسک** | ۱۰ گیگابایت فضای خالی | ۲۰ گیگابایت SSD / NVMe |
| **پورت‌های باز** | ۵۳ (UDP/TCP)، ۴۴۳ (TCP)، ۸۰۸۰ (TCP) | یکسان (محافظت‌شده با ipset و Cloudflare) |

---

<h2 id="-امنیت-سختازاری-و-حریم-خصوصی">🛡️ امنیت، سخت‌سازی و حریم خصوصی</h2>

* **فیلترینگ لایه هسته لینوکس با `ipset`:** تنها آی‌پی‌های تایید شده در مجموعه `gamers` امکان ارتباط با سرویس DNS و SNI را دارند و پویش‌های اینترنتی و اسکنرها بلافاصله دراپ می‌شوند.
* **محافظت خودکار Fail2ban:** پایش مداوم حملات Brute-force روی پورت‌های مدیریتی.
* **امنیت پایگاه داده:** پایگاه داده با مجوزهای محدود فایل (`chmod 600 users.db`) ایزوله شده است.
* **پشتیبان‌گیری روزانه:** اسکریپت خودکار روزانه از دیتابیس و تنظیمات در `/opt/smartdns/backups/` فایل پشتیبان تهیه می‌کند.
* **محدودیت نرخ درخواست (Rate Limit):** قوانین ضد سیلاب DNS ترافیک را به حداکثر ۵۰ درخواست در ثانیه برای هر کلاینت کنترل می‌کنند.
* **حفظ حریم خصوصی:** هیچ‌گونه داده شخصی، فعالیت کاربر یا آمار ترافیکی به سرورهای خارجی ارسال نمی‌شود.

---

</div>

<div align="center" style="text-align: center;">
  <h2 align="center" style="text-align: center;">🌟 حمایت و توسعه</h2>

  <p align="center" style="text-align: center;">
    اگر این پروژه به بهبود تجربه بازی و رفع تحریم‌های شما کمک کرده است، لطفاً با ثبت ستاره (Star) در گیت‌هاب از آن حمایت کنید!
  </p>

  <p align="center">
    <a href="https://github.com/farzadrahnama/gaming-smartdns">
      <img src="https://img.shields.io/github/stars/farzadrahnama/gaming-smartdns?style=for-the-badge&label=Star%20on%20GitHub&color=yellow&logo=github" alt="Star on GitHub">
    </a>
  </p>

  <hr>

  <p align="center" style="text-align: center;">
    <strong>طراحی و پیاده‌سازی توسط فرزاد رهنما</strong><br>
    <a href="https://github.com/farzadrahnama"><img alt="GitHub: farzadrahnama" src="https://img.shields.io/badge/GitHub-farzadrahnama-24292e?style=flat-square&logo=github"></a>&nbsp;<a href="https://github.com/farzadrahnama/gaming-smartdns/issues"><img alt="Open Issues" src="https://img.shields.io/github/issues/farzadrahnama/gaming-smartdns?style=flat-square"></a><br>
    <sub>&copy; Farzad Rahnama. تحت لایسنس متن‌باز MIT منتشر شده است.</sub>
  </p>
</div>
