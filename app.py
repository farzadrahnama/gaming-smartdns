import re
import os
import sqlite3
import secrets
import subprocess
import asyncio
import hashlib
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()
DB_FILE = "/opt/smartdns/users.db"

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# Authentication Dependency
def get_current_admin(request: Request):
    token = request.cookies.get("session_token")
    if not token:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT admins.id, admins.name, admins.username, admins.role 
        FROM sessions 
        JOIN admins ON sessions.admin_id = admins.id 
        WHERE sessions.token = ?
    """, (token,))
    admin = c.fetchone()
    conn.close()
    
    if not admin:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return dict(admin)

def get_active_ip_timeouts():
    active_ips = {}
    try:
        res = subprocess.run(["ipset", "list", "gamers"], capture_output=True, text=True, check=True)
        in_members = False
        for line in res.stdout.splitlines():
            if line.startswith("Members:"):
                in_members = True
                continue
            if in_members and line.strip():
                parts = line.strip().split()
                ip = parts[0]
                timeout_sec = 0
                if "timeout" in parts:
                    try:
                        timeout_sec = int(parts[parts.index("timeout") + 1])
                    except (ValueError, IndexError):
                        timeout_sec = 0
                active_ips[ip] = timeout_sec
    except Exception:
        pass
    return active_ips

def sync_accounting():
    try:
        res_in = subprocess.run(["iptables", "-nvx", "-L", "SMARTDNS_IN", "-Z"], capture_output=True, text=True)
        res_out = subprocess.run(["iptables", "-nvx", "-L", "SMARTDNS_OUT", "-Z"], capture_output=True, text=True)
        
        ip_bytes = {}
        for out in [res_in.stdout, res_out.stdout]:
            for line in out.splitlines():
                parts = line.strip().split()
                if len(parts) >= 9 and parts[1].isdigit():
                    bytes_cnt = int(parts[1])
                    src = parts[7]
                    dst = parts[8]
                    target_ip = src if src != "0.0.0.0/0" else dst
                    if bytes_cnt > 0 and target_ip != "0.0.0.0/0":
                        ip_bytes[target_ip] = ip_bytes.get(target_ip, 0) + bytes_cnt

        if ip_bytes:
            conn = get_db()
            c = conn.cursor()
            for ip, b_count in ip_bytes.items():
                c.execute("UPDATE users SET used_bytes = used_bytes + ? WHERE last_ip = ?", (b_count, ip))
            conn.commit()
            conn.close()
    except Exception:
        pass

def check_user_limits(user):
    if user['is_blocked']:
        return False, "Account suspended by administrator."
    if user['expire_date']:
        try:
            exp = datetime.strptime(user['expire_date'], "%Y-%m-%d")
            if datetime.now() > exp:
                return False, f"Subscription expired on {user['expire_date']}."
        except Exception:
            pass
    if user['max_gb'] and user['max_gb'] > 0:
        max_bytes = user['max_gb'] * (1024 ** 3)
        if (user['used_bytes'] or 0) >= max_bytes:
            return False, f"Traffic limit of {user['max_gb']} GB reached."
    return True, "Active"

def register_iptables_acct(ip):
    try:
        subprocess.run(f"iptables -C SMARTDNS_IN -s {ip} -j ACCEPT 2>/dev/null || iptables -A SMARTDNS_IN -s {ip} -j ACCEPT", shell=True)
        subprocess.run(f"iptables -C SMARTDNS_OUT -d {ip} -j ACCEPT 2>/dev/null || iptables -A SMARTDNS_OUT -d {ip} -j ACCEPT", shell=True)
    except Exception:
        pass

@app.on_event("startup")
async def start_background_tasks():
    async def periodic_accounting():
        while True:
            await asyncio.sleep(30)
            sync_accounting()
    asyncio.create_task(periodic_accounting())

# --- AUTH ROUTES ---

@app.get("/login", response_class=HTMLResponse)
async def login_page(error: str = ""):
    err_html = f'<div style="background:#450a0a;border:1px solid #dc2626;color:#fca5a5;padding:10px;border-radius:8px;margin-bottom:15px;font-size:0.9rem;">{error}</div>' if error else ""
    return f"""<!DOCTYPE html><html><head><title>Login - Gaming DNS</title><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background:#0b0f19; color:#f8fafc; display:flex; justify-content:center; align-items:center; height:100vh; margin:0; }}
        .card {{ background:#161f30; border:1px solid #1e293b; padding:35px 30px; border-radius:16px; width:340px; box-shadow:0 10px 30px rgba(0,0,0,0.5); text-align:center; }}
        input {{ width:100%; padding:12px; margin:8px 0 16px; border-radius:8px; border:1px solid #334155; background:#0b0f19; color:#fff; box-sizing:border-box; font-size:0.95rem; }}
        button {{ width:100%; padding:12px; border-radius:8px; border:none; background:#38bdf8; color:#0b0f19; font-weight:bold; font-size:1rem; cursor:pointer; }}
        button:hover {{ background:#7dd3fc; }}
    </style></head><body>
    <div class="card">
        <h2 style="color:#38bdf8;margin:0 0 10px;">🎮 Gaming DNS</h2>
        <p style="color:#94a3b8;font-size:0.85rem;margin-bottom:20px;">Control & Accounting Panel</p>
        {err_html}
        <form method="POST" action="/login">
            <div style="text-align:left;font-size:0.85rem;color:#94a3b8;">Username</div>
            <input type="text" name="username" required autofocus>
            <div style="text-align:left;font-size:0.85rem;color:#94a3b8;">Password</div>
            <input type="password" name="password" required>
            <button type="submit">Sign In</button>
        </form>
    </div></body></html>"""

@app.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    pw_h = hash_pw(password)
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id FROM admins WHERE username = ? AND password_hash = ?", (username, pw_h))
    admin = c.fetchone()
    if not admin:
        conn.close()
        return RedirectResponse(url="/login?error=Invalid+username+or+password", status_code=status.HTTP_303_SEE_OTHER)
    
    token = secrets.token_urlsafe(32)
    c.execute("INSERT INTO sessions (token, admin_id, created_at) VALUES (?, ?, ?)", 
              (token, admin['id'], datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

    res = RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    res.set_cookie(key="session_token", value=token, httponly=True, max_age=86400 * 30, samesite="lax")
    return res

@app.get("/logout")
async def logout(response: Response):
    res = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    res.delete_cookie("session_token")
    return res

# --- ADMIN DASHBOARD ---

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, current_admin: dict = Depends(get_current_admin)):
    sync_accounting()
    conn = get_db()
    c = conn.cursor()

    is_super = (current_admin['role'] == 'superadmin')

    # Fetch users
    if is_super:
        c.execute("""
            SELECT users.*, admins.name as admin_name 
            FROM users 
            LEFT JOIN admins ON users.admin_id = admins.id 
            ORDER BY users.id DESC
        """)
    else:
        c.execute("""
            SELECT users.*, admins.name as admin_name 
            FROM users 
            LEFT JOIN admins ON users.admin_id = admins.id 
            WHERE users.admin_id = ? 
            ORDER BY users.id DESC
        """, (current_admin['id'],))
    users = c.fetchall()

    # Fetch subadmins if superadmin
    subadmins = []
    if is_super:
        c.execute("SELECT id, name, username, created_at FROM admins WHERE role = 'subadmin' ORDER BY id DESC")
        subadmins = c.fetchall()

    conn.close()

    active_ip_map = get_active_ip_timeouts()
    proto = request.headers.get("x-forwarded-proto", "https")
    host_header = request.headers.get("host", "os.getenv("PANEL_DOMAIN", "localhost")")
    base_url = f"{proto}://{host_header}"

    rows = ""
    active_count = 0
    total_traffic_bytes = 0

    for u in users:
        total_traffic_bytes += (u['used_bytes'] or 0)
        link = f"{base_url}/activate?token={u['token']}"
        is_allowed, reason = check_user_limits(u)
        used_gb = round((u['used_bytes'] or 0) / (1024 ** 3), 2)
        
        # Traffic display
        if u['max_gb'] and u['max_gb'] > 0:
            pct = min(100, int((used_gb / u['max_gb']) * 100))
            traffic_html = f"""<div><span style="font-weight:bold;color:#38bdf8;">{used_gb} GB</span> / {u['max_gb']} GB
            <div style="background:#0f172a;border-radius:4px;height:6px;width:110px;margin-top:4px;overflow:hidden;">
                <div style="background:{'#ef4444' if pct > 90 else '#38bdf8'};width:{pct}%;height:100%;"></div>
            </div></div>"""
        else:
            traffic_html = f"<span style='color:#94a3b8;'>{used_gb} GB (Unlimited)</span>"

        # Expiry display
        if u['expire_date']:
            try:
                days_left = (datetime.strptime(u['expire_date'], "%Y-%m-%d") - datetime.now()).days
                exp_html = f"<span style='color:#ef4444;font-weight:bold;'>Expired</span>" if days_left < 0 else f"<span style='color:#4ade80;'>{days_left}d left</span>"
            except:
                exp_html = u['expire_date']
        else:
            exp_html = "<span style='color:#94a3b8;'>No Expiry</span>"

        # Status badge
        if not is_allowed:
            status_badge = f"<span style='color:#ef4444;background:#450a0a;padding:4px 8px;border-radius:6px;font-size:0.75rem;'>⛔ {reason}</span>"
            kick_btn = ""
        elif u['last_ip'] in active_ip_map:
            active_count += 1
            rem_sec = active_ip_map[u['last_ip']]
            status_badge = f"<span style='color:#4ade80;font-weight:bold;background:#052e16;padding:4px 8px;border-radius:6px;font-size:0.75rem;'>🟢 Online ({rem_sec//3600}h)</span>"
            kick_btn = f"""<form method="POST" action="/admin/kick" style="display:inline;margin-left:4px;"><input type="hidden" name="ip" value="{u['last_ip']}"><button type="submit" style="padding:3px 6px;background:#f59e0b;color:#000;border:none;border-radius:4px;cursor:pointer;font-size:0.7rem;">Kick</button></form>"""
        else:
            status_badge = "<span style='color:#94a3b8;background:#1e293b;padding:4px 8px;border-radius:6px;font-size:0.75rem;'>⚪ Offline</span>"
            kick_btn = ""

        creator_badge = f"<span style='color:#a855f7;font-size:0.75rem;background:#3b0764;padding:2px 6px;border-radius:4px;'>{u['admin_name'] or 'SuperAdmin'}</span>" if is_super else ""

        rows += f"""<tr>
            <td><strong>{u['name']}</strong> {creator_badge}</td>
            <td><code style="color:#38bdf8;background:#0b0f19;padding:3px 6px;border-radius:4px;">{u['last_ip']}</code></td>
            <td>{status_badge} {kick_btn}</td>
            <td>{traffic_html}</td>
            <td>{exp_html}</td>
            <td>
                <input type="text" value="{link}" id="l_{u['id']}" readonly style="width:160px;padding:4px 6px;background:#0b0f19;color:#fff;border:1px solid #334155;border-radius:6px;font-size:0.75rem;">
                <button onclick="navigator.clipboard.writeText(document.getElementById('l_{u['id']}').value);alert('Copied link!');" style="padding:4px 8px;background:#334155;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:0.75rem;">📋 Copy</button>
            </td>
            <td>
                <button onclick="openEditModal({u['id']}, '{u['name']}', {u['max_gb']}, '{u['expire_date']}')" style="padding:4px 8px;background:#0284c7;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:0.75rem;">✏️ Edit</button>
                <form method="POST" action="/admin/delete" style="display:inline;" onsubmit="return confirm('Delete user {u['name']}?');">
                    <input type="hidden" name="user_id" value="{u['id']}">
                    <button type="submit" style="padding:4px 8px;background:#ef4444;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:0.75rem;">🗑️</button>
                </form>
            </td>
        </tr>"""

    # Subadmin rows
    sub_rows = ""
    for s in subadmins:
        sub_rows += f"""<tr>
            <td><strong>{s['name']}</strong></td>
            <td><code>{s['username']}</code></td>
            <td>{s['created_at']}</td>
            <td>
                <form method="POST" action="/admin/delete_subadmin" style="display:inline;" onsubmit="return confirm('Delete subadmin {s['name']}?');">
                    <input type="hidden" name="subadmin_id" value="{s['id']}">
                    <button type="submit" style="padding:4px 8px;background:#ef4444;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:0.75rem;">Delete</button>
                </form>
            </td>
        </tr>"""

    subadmin_section = ""
    if is_super:
        subadmin_section = f"""
        <div class="card" style="margin-top:25px;">
            <h3 style="margin-top:0;color:#c084fc;">👔 Sub-Admin Management (Resellers)</h3>
            <form method="POST" action="/admin/add_subadmin" style="display:flex;gap:10px;margin-bottom:15px;flex-wrap:wrap;">
                <input type="text" name="name" placeholder="Sub-Admin Name (e.g. Reza Agent)" required style="flex:2;">
                <input type="text" name="username" placeholder="Login Username" required style="flex:1;">
                <input type="password" name="password" placeholder="Password" required style="flex:1;">
                <button type="submit" style="background:#a855f7;color:#fff;">+ Create Sub-Admin</button>
            </form>
            <table>
                <thead><tr><th>Name</th><th>Username</th><th>Created Date</th><th>Action</th></tr></thead>
                <tbody>{sub_rows if sub_rows else '<tr><td colspan="4" style="text-align:center;color:#64748b;padding:15px;">No sub-admins created yet.</td></tr>'}</tbody>
            </table>
        </div>
        """

    total_gb = round(total_traffic_bytes / (1024 ** 3), 2)
    role_badge = "👑 Super Admin" if is_super else "👔 Sub-Admin"

    return f"""<!DOCTYPE html><html><head><title>Gaming DNS Dashboard</title><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background:#0b0f19; color:#e2e8f0; margin:0; padding:25px; }}
        .c {{ max-width:1180px; margin:0 auto; }}
        .card {{ background:#161f30; border:1px solid #1e293b; border-radius:12px; padding:20px; margin-bottom:22px; box-shadow:0 4px 10px rgba(0,0,0,0.3); }}
        input[type="text"], input[type="password"], input[type="number"], input[type="date"] {{ padding:10px 12px; border-radius:8px; border:1px solid #334155; background:#0b0f19; color:#fff; font-size:0.95rem; }}
        button {{ padding:10px 18px; border-radius:8px; border:none; font-weight:bold; cursor:pointer; }}
        .btn-add {{ background:#38bdf8; color:#0b0f19; }}
        table {{ width:100%; border-collapse:collapse; margin-top:10px; }}
        th, td {{ padding:12px 10px; text-align:left; border-bottom:1px solid #1e293b; font-size:0.88rem; }}
        th {{ color:#94a3b8; font-weight:600; }}
        .stats-bar {{ display:flex; gap:15px; margin-bottom:20px; flex-wrap:wrap; }}
        .stat-box {{ background:#161f30; border:1px solid #1e293b; padding:15px 20px; border-radius:10px; flex:1; min-width:160px; }}
        .stat-val {{ font-size:1.5rem; font-weight:bold; color:#38bdf8; margin-top:5px; }}
        .modal {{ display:none; position:fixed; z-index:99; left:0; top:0; width:100%; height:100%; background:rgba(0,0,0,0.7); justify-content:center; align-items:center; }}
        .nav-btn {{ background:#1e293b; color:#e2e8f0; text-decoration:none; padding:8px 14px; border-radius:8px; font-size:0.85rem; font-weight:600; display:inline-flex; align-items:center; gap:6px; }}
        .nav-btn:hover {{ background:#334155; }}
    </style>
    <script>
        function openEditModal(id, name, max_gb, expire_date) {{
            document.getElementById('edit_uid').value = id;
            document.getElementById('edit_name').innerText = name;
            document.getElementById('edit_max_gb').value = max_gb;
            document.getElementById('edit_expire_date').value = expire_date;
            document.getElementById('editModal').style.display = 'flex';
        }}
        function closeEditModal() {{
            document.getElementById('editModal').style.display = 'none';
        }}
    </script>
    </head><body><div class="c">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:10px;">
            <div>
                <h1 style="color:#38bdf8;margin:0;font-size:1.6rem;">🎮 Gaming DNS & Reseller Hub</h1>
                <span style="font-size:0.85rem;color:#94a3b8;">Logged in as: <strong>{current_admin['name']}</strong> ({role_badge})</span>
            </div>
            <div style="display:flex;gap:10px;">
                <a href="/admin/logs" class="nav-btn" style="background:#0284c7;color:#fff;">📜 Live Game Logs</a>
                <a href="/admin/change-password" class="nav-btn" style="background:#334155;color:#fff;">🔑 Change Password</a>
                <a href="/logout" class="nav-btn" style="background:#450a0a;color:#fca5a5;">🚪 Logout</a>
            </div>
        </div>

        <div class="stats-bar">
            <div class="stat-box">
                <div style="color:#94a3b8;font-size:0.8rem;">SERVER IP</div>
                <div class="stat-val" style="color:#f8fafc;font-size:1.2rem;">os.getenv("SERVER_IP", "127.0.0.1")</div>
            </div>
            <div class="stat-box">
                <div style="color:#94a3b8;font-size:0.8rem;">MANAGED CLIENTS</div>
                <div class="stat-val">{len(users)}</div>
            </div>
            <div class="stat-box">
                <div style="color:#94a3b8;font-size:0.8rem;">ONLINE NOW</div>
                <div class="stat-val" style="color:#4ade80;">{active_count}</div>
            </div>
            <div class="stat-box">
                <div style="color:#94a3b8;font-size:0.8rem;">TOTAL CONSUMED TRAFFIC</div>
                <div class="stat-val" style="color:#a855f7;">{total_gb} GB</div>
            </div>
        </div>

        <div class="card">
            <h3 style="margin-top:0;">➕ Add Client</h3>
            <form method="POST" action="/admin/add" style="display:flex;gap:10px;flex-wrap:wrap;">
                <input type="text" name="name" placeholder="Client Name (e.g. Farzad)" required style="flex:2;min-width:180px;">
                <input type="number" step="0.5" name="max_gb" placeholder="Traffic GB (0 = Unlimited)" value="20" style="flex:1;min-width:140px;">
                <input type="number" name="days" placeholder="Validity Days" value="30" style="flex:1;min-width:140px;">
                <button type="submit" class="btn-add">+ Generate Client Link</button>
            </form>
        </div>

        <div class="card">
            <h3 style="margin-top:0;">👥 Client Accounts List</h3>
            <table>
                <thead>
                    <tr>
                        <th>Client</th>
                        <th>Active IP</th>
                        <th>Status</th>
                        <th>Traffic Usage</th>
                        <th>Expiration</th>
                        <th>Client Portal Link</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {rows if rows else '<tr><td colspan="7" style="text-align:center;color:#64748b;padding:25px;">No clients in your workspace.</td></tr>'}
                </tbody>
            </table>
        </div>

        {subadmin_section}
    </div>

    <!-- Edit User Modal -->
    <div id="editModal" class="modal">
        <div style="background:#161f30;border:1px solid #1e293b;padding:25px;border-radius:12px;width:380px;box-shadow:0 10px 25px rgba(0,0,0,0.5);">
            <h3 style="margin-top:0;color:#38bdf8;">Edit Limits: <span id="edit_name"></span></h3>
            <form method="POST" action="/admin/update_limits">
                <input type="hidden" id="edit_uid" name="user_id">
                <div style="margin-bottom:12px;">
                    <label style="display:block;margin-bottom:4px;color:#94a3b8;font-size:0.85rem;">Traffic Quota (GB) [0 = Unlimited]:</label>
                    <input type="number" step="0.5" id="edit_max_gb" name="max_gb" style="width:100%;box-sizing:border-box;">
                </div>
                <div style="margin-bottom:15px;">
                    <label style="display:block;margin-bottom:4px;color:#94a3b8;font-size:0.85rem;">Expiration Date (YYYY-MM-DD):</label>
                    <input type="date" id="edit_expire_date" name="expire_date" style="width:100%;box-sizing:border-box;">
                </div>
                <div style="margin-bottom:15px;">
                    <label><input type="checkbox" name="reset_traffic" value="yes"> 🔄 Reset used traffic to 0 GB</label>
                </div>
                <div style="display:flex;gap:10px;justify-content:flex-end;">
                    <button type="button" onclick="closeEditModal()" style="background:#334155;color:#fff;">Cancel</button>
                    <button type="submit" style="background:#38bdf8;color:#0b0f19;">Save Changes</button>
                </div>
            </form>
        </div>
    </div>
    </body></html>"""

@app.post("/admin/add")
async def add_user(name: str = Form(...), max_gb: float = Form(0), days: int = Form(0), current_admin: dict = Depends(get_current_admin)):
    token = secrets.token_urlsafe(16)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    expire_date = ""
    if days and days > 0:
        expire_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO users (name, token, created_at, max_gb, used_bytes, expire_date, admin_id) VALUES (?, ?, ?, ?, 0, ?, ?)", 
              (name, token, created_at, max_gb, expire_date, current_admin['id']))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/update_limits")
async def update_limits(user_id: int = Form(...), max_gb: float = Form(0), expire_date: str = Form(""), reset_traffic: str = Form(None), current_admin: dict = Depends(get_current_admin)):
    conn = get_db()
    c = conn.cursor()
    
    # Subadmins can only edit their own clients
    if current_admin['role'] != 'superadmin':
        c.execute("SELECT id FROM users WHERE id = ? AND admin_id = ?", (user_id, current_admin['id']))
        if not c.fetchone():
            conn.close()
            raise HTTPException(status_code=403, detail="Forbidden")

    if reset_traffic == "yes":
        c.execute("UPDATE users SET max_gb = ?, expire_date = ?, used_bytes = 0 WHERE id = ?", (max_gb, expire_date, user_id))
    else:
        c.execute("UPDATE users SET max_gb = ?, expire_date = ? WHERE id = ?", (max_gb, expire_date, user_id))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/delete")
async def delete_user(user_id: int = Form(...), current_admin: dict = Depends(get_current_admin)):
    conn = get_db()
    c = conn.cursor()
    
    if current_admin['role'] != 'superadmin':
        c.execute("SELECT last_ip FROM users WHERE id = ? AND admin_id = ?", (user_id, current_admin['id']))
        row = c.fetchone()
        if not row:
            conn.close()
            raise HTTPException(status_code=403, detail="Forbidden")
    else:
        c.execute("SELECT last_ip FROM users WHERE id = ?", (user_id,))
        row = c.fetchone()

    if row and row['last_ip'] and row['last_ip'] != "None":
        subprocess.run(f"ipset del gamers {row['last_ip']}", shell=True, check=False)
    
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/kick")
async def kick_user(ip: str = Form(...), current_admin: dict = Depends(get_current_admin)):
    if ip and ip != "None":
        subprocess.run(f"ipset del gamers {ip}", shell=True, check=False)
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/add_subadmin")
async def add_subadmin(name: str = Form(...), username: str = Form(...), password: str = Form(...), current_admin: dict = Depends(get_current_admin)):
    if current_admin['role'] != 'superadmin':
        raise HTTPException(status_code=403, detail="Only Super Admin can create Sub-Admins")
    
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO admins (name, username, password_hash, role, created_at) VALUES (?, ?, ?, 'subadmin', ?)",
                  (name, username, hash_pw(password), datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return RedirectResponse(url="/admin?error=Username+already+exists", status_code=status.HTTP_303_SEE_OTHER)
    conn.close()
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/delete_subadmin")
async def delete_subadmin(subadmin_id: int = Form(...), current_admin: dict = Depends(get_current_admin)):
    if current_admin['role'] != 'superadmin':
        raise HTTPException(status_code=403, detail="Forbidden")
    
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM admins WHERE id = ? AND role = 'subadmin'", (subadmin_id,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

# --- DEDICATED LIVE GAME CONNECTION LOGS ---

@app.get("/admin/logs", response_class=HTMLResponse)
async def view_game_logs(request: Request):
    import os
    import re
    import sqlite3
    import subprocess
    
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT last_ip, name FROM users WHERE last_ip IS NOT NULL AND last_ip != 'None'")
        ip_to_name = {row['last_ip']: row['name'] for row in c.fetchall()}
        conn.close()

        server_ip = "os.getenv("SERVER_IP", "127.0.0.1")"
        all_entries = []

        # 1. Parse Live DNS Queries from smartdns_queries.log
        dns_log_path = "/var/log/smartdns_queries.log"
        if os.path.exists(dns_log_path):
            try:
                res_dns = subprocess.run(["tail", "-n", "120", dns_log_path], capture_output=True, text=True)
                for line in res_dns.stdout.splitlines():
                    line_str = line.strip()
                    if not line_str:
                        continue
                    m = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*? IP ([0-9.]+)\.\d+ > [0-9.]+\.53:.*?(?:A\?|AAAA\?|HTTPS\?|\?)\s*([a-zA-Z0-9.-]+)\.', line_str)
                    if not m:
                        m = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*? IP ([0-9.]+)\.\d+ > [0-9.]+\.53:.*? ([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\.', line_str)
                    if m:
                        time_str, client_ip, domain = m.groups()
                        if client_ip == server_ip:
                            continue
                        domain = domain.rstrip('.')
                        user_name = ip_to_name.get(client_ip)

                        lower = domain.lower()
                        tag = "🌐 General"
                        tag_color = "#64748b"

                        if any(k in lower for k in ['antigravity', 'cloudcode', 'run.app']):
                            tag = "🤖 Antigravity"
                            tag_color = "#38bdf8"
                        elif any(k in lower for k in ['chatgpt', 'openai', 'oaistatic', 'oaiusercontent']):
                            tag = "🤖 ChatGPT"
                            tag_color = "#10b981"
                        elif any(k in lower for k in ['gemini', 'bard', 'generativelanguage', 'aistudio', 'makersuite', 'deepmind']):
                            tag = "🤖 Gemini"
                            tag_color = "#06b6d4"
                        elif any(k in lower for k in ['claude', 'anthropic']):
                            tag = "🤖 Claude"
                            tag_color = "#d97706"
                        elif any(k in lower for k in ['activision', 'callofduty', 'demonware', 'atvi']):
                            tag = "🎯 Call of Duty"
                            tag_color = "#22c55e"
                        elif any(k in lower for k in ['ea.com', 'origin.com', 'electronicarts']):
                            tag = "⚡ EA / Apex"
                            tag_color = "#f97316"
                        elif any(k in lower for k in ['riotgames', 'pvp.net', 'leagueoflegends']):
                            tag = "🛡️ Riot / Valorant"
                            tag_color = "#ef4444"
                        elif any(k in lower for k in ['battle.net', 'blizzard', 'battlenet']):
                            tag = "⚔️ Blizzard"
                            tag_color = "#0ea5e9"
                        elif any(k in lower for k in ['epicgames', 'unrealengine']):
                            tag = "🎮 Epic / Fortnite"
                            tag_color = "#a855f7"
                        elif 'discord' in lower:
                            tag = "🎧 Discord"
                            tag_color = "#6366f1"
                        elif 'playstation' in lower:
                            tag = "🎮 PlayStation"
                            tag_color = "#0284c7"

                        all_entries.append({
                            'time': time_str,
                            'user': user_name,
                            'ip': client_ip,
                            'domain': domain,
                            'proto': 'DNS',
                            'tag': tag,
                            'color': tag_color
                        })
            except Exception:
                pass

        # 2. Parse Live HTTPS / SNI from sniproxy docker container
        try:
            res_sni = subprocess.run(["docker", "logs", "--tail", "80", "sniproxy"], capture_output=True, text=True)
            raw_logs = (res_sni.stdout or "") + (res_sni.stderr or "")
            for line in raw_logs.splitlines():
                line_str = line.strip()
                if not line_str:
                    continue
                try:
                    clean = re.sub(r'\[[0-9;]*[a-zA-Z]', '', line_str).strip()
                    src_ip = None
                    ip_m = re.search(r'(?:srcip|src|client|client_ip|from)[=:"]+([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', clean)
                    if ip_m and ip_m.group(1) not in [server_ip, '127.0.0.1', '1.1.1.1', '0.0.0.0']:
                        src_ip = ip_m.group(1)
                    if not src_ip:
                        continue

                    domain = ""
                    m = re.search(r'(?:sni|domain|question|host|qname|fqdn)[=:"]+([a-zA-Z0-9.-]+)', clean)
                    if m:
                        domain = m.group(1).rstrip('".')
                    else:
                        dm = re.search(r'([a-zA-Z0-9-]+\.(?:com|org|net|goog|app|io|ai|ir|de)[a-zA-Z0-9.-]*)', clean)
                        if dm:
                            domain = dm.group(1).rstrip('".')
                    if not domain:
                        continue

                    user_name = ip_to_name.get(src_ip)
                    lower = (domain + ' ' + clean).lower()
                    tag = "🌐 General"
                    tag_color = "#64748b"

                    if any(k in lower for k in ['antigravity', 'cloudcode', 'run.app']):
                        tag = "🤖 Antigravity"
                        tag_color = "#38bdf8"
                    elif any(k in lower for k in ['chatgpt', 'openai', 'oaistatic', 'oaiusercontent']):
                        tag = "🤖 ChatGPT"
                        tag_color = "#10b981"
                    elif any(k in lower for k in ['gemini', 'bard', 'generativelanguage', 'aistudio', 'makersuite', 'deepmind']):
                        tag = "🤖 Gemini"
                        tag_color = "#06b6d4"
                    elif any(k in lower for k in ['claude', 'anthropic']):
                        tag = "🤖 Claude"
                        tag_color = "#d97706"
                    elif any(k in lower for k in ['activision', 'callofduty', 'demonware', 'atvi']):
                        tag = "🎯 Call of Duty"
                        tag_color = "#22c55e"
                    elif any(k in lower for k in ['ea.com', 'origin.com', 'electronicarts']):
                        tag = "⚡ EA / Apex"
                        tag_color = "#f97316"
                    elif any(k in lower for k in ['riotgames', 'pvp.net', 'leagueoflegends']):
                        tag = "🛡️ Riot / Valorant"
                        tag_color = "#ef4444"
                    elif any(k in lower for k in ['battle.net', 'blizzard', 'battlenet']):
                        tag = "⚔️ Blizzard"
                        tag_color = "#0ea5e9"
                    elif any(k in lower for k in ['epicgames', 'unrealengine']):
                        tag = "🎮 Epic / Fortnite"
                        tag_color = "#a855f7"
                    elif 'discord' in lower:
                        tag = "🎧 Discord"
                        tag_color = "#6366f1"
                    elif 'playstation' in lower:
                        tag = "🎮 PlayStation"
                        tag_color = "#0284c7"

                    time_str = clean[:19].replace('T', ' ')
                    all_entries.append({
                        'time': time_str,
                        'user': user_name,
                        'ip': src_ip,
                        'domain': domain,
                        'proto': 'HTTPS',
                        'tag': tag,
                        'color': tag_color
                    })
                except Exception:
                    continue
        except Exception:
            pass

        all_entries.sort(key=lambda x: x['time'], reverse=True)

        log_rows = ""
        for entry in all_entries[:120]:
            col = entry['color']
            tag_text = entry['tag']
            badge = f"<span style='background:{col}22;color:{col};border:1px solid {col}55;padding:3px 8px;border-radius:6px;font-weight:bold;font-size:0.75rem;'>{tag_text}</span>"
            proto_badge = f"<span style='background:#1e293b;color:#94a3b8;padding:2px 6px;border-radius:4px;font-size:0.7rem;font-weight:600;'>{entry['proto']}</span>"

            if entry['user']:
                user_html = f"<strong style='color:#38bdf8;font-size:0.95rem;'>{entry['user']}</strong><div style='font-size:0.72rem;color:#64748b;font-family:monospace;'>{entry['ip']}</div>"
            elif entry['ip']:
                user_html = f"<span style='color:#f59e0b;font-weight:600;font-size:0.85rem;'>Guest / IP</span><div style='font-size:0.72rem;color:#64748b;font-family:monospace;'>{entry['ip']}</div>"
            else:
                user_html = "<span style='color:#64748b;font-size:0.85rem;'>System</span>"

            log_rows += f"""<tr>
                <td style="color:#94a3b8;font-family:monospace;font-size:0.8rem;">{entry['time']}</td>
                <td>{user_html}</td>
                <td>{proto_badge}</td>
                <td>{badge}</td>
                <td><code style="color:#f8fafc;font-size:0.85rem;word-break:break-all;">{entry['domain']}</code></td>
            </tr>"""

        return f"""<!DOCTYPE html><html><head><title>Live Traffic Monitor</title><meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background:#0b0f19; color:#e2e8f0; margin:0; padding:25px; }}
            .c {{ max-width:1200px; margin:0 auto; }}
            .card {{ background:#161f30; border:1px solid #1e293b; border-radius:12px; padding:20px; box-shadow:0 4px 10px rgba(0,0,0,0.3); }}
            table {{ width:100%; border-collapse:collapse; margin-top:15px; }}
            th, td {{ padding:12px 10px; text-align:left; border-bottom:1px solid #1e293b; font-size:0.88rem; }}
            th {{ color:#94a3b8; font-weight:600; }}
            .nav-btn {{ background:#1e293b; color:#e2e8f0; text-decoration:none; padding:8px 14px; border-radius:8px; font-size:0.85rem; font-weight:600; display:inline-flex; align-items:center; }}
            .nav-btn:hover {{ background:#334155; }}
            #searchBox {{ padding:8px 12px; border-radius:8px; border:1px solid #334155; background:#0b0f19; color:#fff; font-size:0.85rem; width:260px; }}
        </style>
        <script>
            function filterTable() {{
                var query = document.getElementById('searchBox').value.toLowerCase();
                var rows = document.querySelectorAll('#logsTable tbody tr');
                rows.forEach(function(r) {{
                    r.style.display = r.innerText.toLowerCase().includes(query) ? '' : 'none';
                }});
            }}
            let autoRef = true;
            function toggleAuto(cb) {{ autoRef = cb.checked; }}
            setInterval(() => {{
                var q = document.getElementById('searchBox') ? document.getElementById('searchBox').value : '';
                if (autoRef && q === '') location.reload();
            }}, 5000);
        </script>
        </head><body><div class="c">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:10px;">
                <div>
                    <h1 style="color:#38bdf8;margin:0;font-size:1.6rem;">🎯 Live Traffic & AI Monitor</h1>
                    <span style="font-size:0.85rem;color:#94a3b8;">Real-time stream of users connecting to Games, Antigravity & Web</span>
                </div>
                <div style="display:flex;gap:10px;align-items:center;">
                    <input type="text" id="searchBox" onkeyup="filterTable()" placeholder="🔍 Filter user or domain...">
                    <label style="font-size:0.82rem;color:#94a3b8;display:flex;align-items:center;gap:4px;cursor:pointer;">
                        <input type="checkbox" checked onchange="toggleAuto(this)"> Auto (5s)
                    </label>
                    <a href="/admin" class="nav-btn">⬅ Back</a>
                    <a href="/logout" class="nav-btn" style="background:#450a0a;color:#fca5a5;">🚪 Logout</a>
                </div>
            </div>

            <div class="card">
                <table id="logsTable">
                    <thead>
                        <tr>
                            <th style="width:160px;">Timestamp</th>
                            <th style="width:180px;">Client Name & IP</th>
                            <th style="width:70px;">Type</th>
                            <th style="width:160px;">Category</th>
                            <th>Target Server / Domain</th>
                        </tr>
                    </thead>
                    <tbody>
                        {log_rows if log_rows else '<tr><td colspan="5" style="text-align:center;color:#64748b;padding:30px;">No activity recorded yet.</td></tr>'}
                    </tbody>
                </table>
            </div>
        </div></body></html>"""
    except Exception as e:
        import traceback
        err_msg = traceback.format_exc()
        return HTMLResponse(f"<html><body style='background:#0b0f19;color:#ef4444;padding:30px;font-family:monospace;'><div style='background:#161f30;border:1px solid #ef4444;border-radius:10px;padding:20px;'><h3>Error in Live Monitor:</h3><pre>{err_msg}</pre><a href='/admin' style='color:#38bdf8;'>Back to Dashboard</a></div></body></html>")


# --- CLIENT STATUS & ACTIVATION PORTAL ---

@app.get("/activate", response_class=HTMLResponse)
async def activate(request: Request, token: str = ""):
    if not token:
        return HTMLResponse("<h2>Error: Token is missing.</h2>", status_code=400)

    sync_accounting()
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE token = ?", (token,))
    user = c.fetchone()

    if not user:
        conn.close()
        return HTMLResponse("<h2 style='color:#ef4444;'>Invalid or revoked link.</h2>", status_code=403)

    is_allowed, reason = check_user_limits(user)
    
    # Ignore Telegram, WhatsApp, Discord, and other link-preview bots
    ua = request.headers.get("user-agent", "").lower()
    is_bot = any(bot in ua for bot in ["telegrambot", "whatsapp", "twitterbot", "facebookexternalhit", "discordbot", "slackbot", "googlebot", "bingbot", "spider", "crawler"])

    forwarded = request.headers.get("x-forwarded-for")
    client_ip = forwarded.split(",")[0].strip() if forwarded else request.client.host

    # Only whitelist if it is a real human, not a crawler
    if is_allowed and not is_bot:
        subprocess.run(f"ipset add gamers {client_ip} timeout 86400 -exist", shell=True, check=True)
        register_iptables_acct(client_ip)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        c.execute("UPDATE users SET last_ip = ?, last_active = ? WHERE id = ?", (client_ip, now_str, user['id']))
        conn.commit()
    else:
        if client_ip:
            subprocess.run(f"ipset del gamers {client_ip} 2>/dev/null || true", shell=True)

    conn.close()

    used_gb = round((user['used_bytes'] or 0) / (1024 ** 3), 2)
    max_gb = user['max_gb'] or 0
    
    if max_gb > 0:
        pct = min(100, int((used_gb / max_gb) * 100))
        traffic_display = f"{used_gb} GB / {max_gb} GB ({pct}% used)"
    else:
        pct = 0
        traffic_display = f"{used_gb} GB (Unlimited Quota)"

    expire_date = user['expire_date']
    if expire_date:
        try:
            days_left = (datetime.strptime(expire_date, "%Y-%m-%d") - datetime.now()).days
            exp_display = f"{max(0, days_left)} Days Remaining (Expires: {expire_date})"
        except:
            exp_display = expire_date
    else:
        exp_display = "Active (Unlimited Validity)"

    server_ip = "os.getenv("SERVER_IP", "127.0.0.1")"

    if is_allowed:
        status_banner = """<span style="background:#22c55e;color:#022c22;padding:6px 14px;border-radius:20px;font-weight:bold;font-size:0.85rem;">● ACCESS ACTIVATED</span>"""
        btn_html = """<button onclick="location.reload();" style="background:#38bdf8;color:#0b0f19;padding:12px;border:none;border-radius:8px;font-size:1rem;font-weight:bold;cursor:pointer;width:100%;">🔄 Refresh My IP</button>"""
        ip_banner = f"""<div style="background:#0b0f19;padding:14px;border-radius:8px;font-family:monospace;font-size:1.3rem;color:#38bdf8;margin:20px 0;border:1px dashed #334155;">{client_ip}</div>"""
    else:
        status_banner = f"""<span style="background:#ef4444;color:#fff;padding:6px 14px;border-radius:20px;font-weight:bold;font-size:0.85rem;">⛔ {reason}</span>"""
        btn_html = """<div style="color:#ef4444;margin-top:15px;font-size:0.9rem;">Please contact your provider to renew your plan.</div>"""
        ip_banner = f"""<div style="background:#450a0a;padding:14px;border-radius:8px;font-family:monospace;font-size:1.1rem;color:#fca5a5;margin:20px 0;">Access Suspended: {reason}</div>"""

    return f"""<!DOCTYPE html><html><head><title>{user['name']}'s Gaming Portal</title><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body{{font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;background:#0b0f19;color:#f8fafc;text-align:center;padding:40px 15px;margin:0;}}
        .card{{background:#161f30;max-width:440px;margin:0 auto;padding:30px;border-radius:16px;border:1px solid #1e293b;box-shadow:0 10px 25px rgba(0,0,0,0.5);}}
        .stat-row{{display:flex;justify-content:space-between;font-size:0.9rem;margin:10px 0;color:#cbd5e1;}}
        .stat-val{{font-weight:bold;color:#38bdf8;}}
    </style></head><body><div class="card">
        {status_banner}
        <h2 style="margin-top: 15px;">Welcome, {user['name']}!</h2>
        
        {ip_banner}
        
        <div style="background:#0f172a;border:1px solid #1e293b;border-radius:10px;padding:15px;text-align:left;margin-bottom:20px;">
            <div style="font-weight:600;margin-bottom:10px;color:#94a3b8;font-size:0.85rem;">📊 YOUR SUBSCRIPTION STATUS</div>
            <div class="stat-row">
                <span>Traffic Quota:</span>
                <span class="stat-val">{traffic_display}</span>
            </div>
            {"<div style='background:#1e293b;border-radius:4px;height:7px;width:100%;margin:6px 0 12px;overflow:hidden;'><div style='background:" + ('#ef4444' if pct > 90 else '#38bdf8') + ";width:" + str(pct) + "%;height:100%;'></div></div>" if max_gb > 0 else ""}
            <div class="stat-row">
                <span>Validity:</span>
                <span class="stat-val">{exp_display}</span>
            </div>
        </div>

        {btn_html}

        <div style="background:#0f172a;padding:16px;border-radius:10px;text-align:left;font-size:0.9rem;margin-top:25px;border:1px solid #1e293b;">
            <strong>⚙️ DNS Configuration:</strong>
            <p style="margin:6px 0;">• <strong>Primary DNS:</strong> <span style="color:#38bdf8;font-weight:bold;">{server_ip}</span></p>
            <p style="margin:6px 0;">• <strong>Secondary DNS:</strong> 1.1.1.1 (or leave blank)</p>
            <p style="color:#94a3b8;font-size:0.8rem;margin-top:10px;">* Bookmark this page on your phone or PC. Whenever your modem reboots, tap Refresh to keep playing.</p>
        </div>
    </div></body></html>"""




# --- CHANGE PASSWORD PAGE ---

@app.get("/admin/change-password", response_class=HTMLResponse)
async def change_password_page(request: Request, error: str = "", success: str = "", current_admin: dict = Depends(get_current_admin)):
    err_html = f'<div style="background:#450a0a;border:1px solid #dc2626;color:#fca5a5;padding:12px;border-radius:8px;margin-bottom:15px;font-size:0.9rem;">{error}</div>' if error else ''
    succ_html = f'<div style="background:#052e16;border:1px solid #16a34a;color:#86efac;padding:12px;border-radius:8px;margin-bottom:15px;font-size:0.9rem;">{success}</div>' if success else ''
    
    return f"""<!DOCTYPE html><html><head><title>Change Password - Gaming DNS</title><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background:#0b0f19; color:#f8fafc; display:flex; justify-content:center; align-items:center; min-height:100vh; margin:0; padding:20px; }}
        .card {{ background:#161f30; border:1px solid #1e293b; padding:35px 30px; border-radius:16px; width:360px; box-shadow:0 10px 30px rgba(0,0,0,0.5); text-align:center; }}
        input {{ width:100%; padding:12px; margin:6px 0 16px; border-radius:8px; border:1px solid #334155; background:#0b0f19; color:#fff; box-sizing:border-box; font-size:0.95rem; }}
        button {{ width:100%; padding:12px; border-radius:8px; border:none; background:#38bdf8; color:#0b0f19; font-weight:bold; font-size:1rem; cursor:pointer; margin-top:5px; }}
        button:hover {{ background:#7dd3fc; }}
        .back-link {{ display:inline-block; margin-top:15px; color:#94a3b8; text-decoration:none; font-size:0.85rem; }}
        .back-link:hover {{ color:#e2e8f0; }}
    </style></head><body>
    <div class="card">
        <h2 style="color:#38bdf8;margin:0 0 10px;">🔑 Change Password</h2>
        <p style="color:#94a3b8;font-size:0.85rem;margin-bottom:20px;">Update password for <strong>{current_admin['name']}</strong></p>
        {err_html}
        {succ_html}
        <form method="POST" action="/admin/change-password">
            <div style="text-align:left;font-size:0.85rem;color:#94a3b8;">Current Password</div>
            <input type="password" name="old_password" required autofocus>
            
            <div style="text-align:left;font-size:0.85rem;color:#94a3b8;">New Password</div>
            <input type="password" name="new_password" required minlength="6">
            
            <div style="text-align:left;font-size:0.85rem;color:#94a3b8;">Confirm New Password</div>
            <input type="password" name="confirm_password" required minlength="6">
            
            <button type="submit">Save New Password</button>
            <a href="/admin" class="back-link">⬅ Back to Dashboard</a>
        </form>
    </div></body></html>"""

@app.post("/admin/change-password")
async def process_change_password(
    old_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    current_admin: dict = Depends(get_current_admin)
):
    if new_password != confirm_password:
        return RedirectResponse(url="/admin/change-password?error=New+passwords+do+not+match", status_code=status.HTTP_303_SEE_OTHER)
    
    if len(new_password) < 6:
        return RedirectResponse(url="/admin/change-password?error=Password+must+be+at+least+6+characters", status_code=status.HTTP_303_SEE_OTHER)

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT password_hash FROM admins WHERE id = ?", (current_admin['id'],))
    row = c.fetchone()
    
    if not row or row['password_hash'] != hash_pw(old_password):
        conn.close()
        return RedirectResponse(url="/admin/change-password?error=Incorrect+current+password", status_code=status.HTTP_303_SEE_OTHER)

    new_hash = hash_pw(new_password)
    c.execute("UPDATE admins SET password_hash = ? WHERE id = ?", (new_hash, current_admin['id']))
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/admin/change-password?success=Password+successfully+updated!", status_code=status.HTTP_303_SEE_OTHER)
