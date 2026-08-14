import os
import ssl
import socket
import re
import urllib.request
import xml.etree.ElementTree as ET
import dns.resolver
from fastapi import FastAPI, HTTPException, BackgroundTasks, Response, Form
from fastapi.responses import HTMLResponse, FileResponse

# استيراد الدوال الأساسية
from blacklist_checker import generate_audit_report, get_live_dashboard_stats
from pdf_generator import generate_radar_pdf

app = FastAPI(
    title="BlacklistMail Radar API",
    description="Enterprise Domain Intelligence, Email Security & Automated Monetized SaaS",
    version="3.0.0",
)

PDF_DIR = "./generated_reports"
os.makedirs(PDF_DIR, exist_ok=True)

# CSS موحد واحترافي لجميع الصفحات الفرعية
COMMON_CSS = """
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
.container { max-width: 850px; margin: 30px auto; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid #334155; }
h1 { color: #fff; font-size: 26px; margin-bottom: 10px; }
p { color: #94a3b8; line-height: 1.6; }
input[type="text"], textarea, select { padding: 12px 15px; width: 95%; border: 1px solid #475569; border-radius: 6px; font-size: 15px; background: #0f172a; color: #fff; margin-bottom: 15px; }
textarea { height: 120px; font-family: inherit; }
button { padding: 12px 22px; background: #38bdf8; color: #0f172a; border: none; border-radius: 6px; font-size: 15px; cursor: pointer; font-weight: bold; transition: all 0.2s; }
button:hover { background: #0284c7; color: #fff; }
a { color: #38bdf8; text-decoration: none; }
.res-box { background: #064e3b; border: 1px solid #10b981; padding: 15px; border-radius: 6px; margin-top: 20px; color: #ecfdf5; }
.err-box { background: #7f1d1d; border: 1px solid #ef4444; padding: 15px; border-radius: 6px; margin-top: 20px; color: #fef2f2; }
code { background: #0f172a; padding: 12px; display: block; border-radius: 6px; font-weight: bold; word-break: break-all; margin-top: 8px; color: #38bdf8; border: 1px solid #334155; }

/* Affiliate Comparison Section */
.affiliate-section { background: #0f172a; border: 1px solid #334155; padding: 20px; border-radius: 10px; margin: 30px 0; }
.affiliate-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; }
@media (max-width: 600px) { .affiliate-grid { grid-template-columns: 1fr; } }
.aff-card { background: #1e293b; border: 1px solid #475569; padding: 18px; border-radius: 8px; text-align: center; }
.aff-card h3 { margin: 0 0 8px 0; color: #38bdf8; font-size: 18px; }
.aff-card p { font-size: 13px; color: #94a3b8; margin-bottom: 15px; }
.aff-btn { display: inline-block; padding: 10px 18px; background: #6366f1; color: #fff; border-radius: 6px; font-weight: bold; font-size: 13px; text-decoration: none; transition: background 0.2s; }
.aff-btn:hover { background: #4f46e5; }
.aff-btn.google { background: #ea4335; }
.aff-btn.google:hover { background: #d93025; }

.news-card { background: #0f172a; border: 1px solid #334155; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
.news-card h3 { margin: 0 0 5px 0; font-size: 16px; }
.news-card p { margin: 0; font-size: 13px; color: #94a3b8; }
"""

# جدول مقارنة الأرباح عالي التحويل
MONETIZATION_HTML = """
<div class="affiliate-section">
    <h3 style="margin:0; text-align:center; color:#f8fafc;">⚡ Need Professional & Secure Email Hosting?</h3>
    <p style="text-align:center; margin-top:5px;">Compare top-rated business email providers with maximum inbox deliverability & built-in SPF/DMARC security:</p>
    <div class="affiliate-grid">
        <div class="aff-card">
            <h3>Hostinger Business Email</h3>
            <p>Best value option! Get custom domain email, 99.9% uptime, and free SSL certificate.</p>
            <a href="https://hostinger.com/?referral=blacklistmail" target="_blank" class="aff-btn">Get Hostinger (75% Off) &rarr;</a>
        </div>
        <div class="aff-card">
            <h3>Google Workspace</h3>
            <p>Enterprise standard! Includes Gmail for Business, Google Drive, Meet & Calendar integration.</p>
            <a href="https://workspace.google.com/intl/en/landing/signup/referral/" target="_blank" class="aff-btn google">Get Google Workspace &rarr;</a>
        </div>
    </div>
</div>
"""

def clean_domain_name(domain: str) -> str:
    return domain.strip().lower().replace("http://", "").replace("https://", "").split("/")[0]


# --- Dashboard ---
@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    html_file_path = "dashboard.html"
    if not os.path.exists(html_file_path):
        raise HTTPException(status_code=404, detail="dashboard.html file not found.")
    with open(html_file_path, "r", encoding="utf-8") as f:
        return f.read()


# --- 1. DKIM Checker (جديد 🌟) ---
@app.get("/dkim-checker", response_class=HTMLResponse)
@app.post("/dkim-checker", response_class=HTMLResponse)
async def dkim_checker(domain: str = Form(default=""), selector: str = Form(default="google")):
    dkim_record, error = None, None
    clean_dom = clean_domain_name(domain)
    clean_sel = selector.strip()
    if clean_dom and clean_sel:
        try:
            query_host = f"{clean_sel}._domainkey.{clean_dom}"
            answers = dns.resolver.resolve(query_host, 'TXT')
            for rdata in answers:
                txt_string = rdata.to_text().strip('"')
                if 'v=DKIM1' in txt_string or 'p=' in txt_string:
                    dkim_record = txt_string
                    break
            if not dkim_record:
                error = f"No DKIM record found for selector '{clean_sel}' on domain {clean_dom}."
        except Exception:
            error = f"Unable to resolve DKIM record for selector '{clean_sel}'."

    res_box = f'<div class="res-box"><h3 style="margin:0;">✅ Valid DKIM Record Found ({clean_sel}._domainkey.{clean_dom}):</h3><code>{dkim_record}</code></div>' if dkim_record else ""
    if error and clean_dom:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    html = f'''<!DOCTYPE html><html><head><title>Free DKIM Record Checker | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>🔑 Free DKIM Record Checker</h1><p>Validate your DomainKeys Identified Mail (DKIM) public key record instantly.</p>
    <form method="POST" action="/dkim-checker">
        <label>Domain Name:</label><br>
        <input type="text" name="domain" placeholder="example.com" value="{clean_dom}" required><br>
        <label>DKIM Selector (Default is often 'google', 'k1', or 's1'):</label><br>
        <input type="text" name="selector" placeholder="e.g. google" value="{clean_sel}" required><br>
        <button type="submit">Check DKIM</button>
    </form>
    {res_box}{MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)


# --- 2. SPF Checker ---
@app.get("/spf-checker", response_class=HTMLResponse)
@app.post("/spf-checker", response_class=HTMLResponse)
async def spf_checker(domain: str = Form(default="")):
    spf_record, error = None, None
    clean_dom = clean_domain_name(domain)
    if clean_dom:
        try:
            answers = dns.resolver.resolve(clean_dom, 'TXT')
            for rdata in answers:
                txt_string = rdata.to_text().strip('"')
                if txt_string.startswith('v=spf1'):
                    spf_record = txt_string
                    break
            if not spf_record:
                error = "No SPF record found for this domain."
        except Exception:
            error = "Unable to resolve DNS records. Please check the domain."

    res_box = f'<div class="res-box"><h3 style="margin:0;">✅ Valid SPF Record Found:</h3><code>{spf_record}</code></div>' if spf_record else ""
    if error and clean_dom:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    html = f'''<!DOCTYPE html><html><head><title>Free SPF Record Checker | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>🛡️ Free SPF Record Checker</h1><p>Validate your Sender Policy Framework (SPF) record in real-time.</p>
    <form method="POST" action="/spf-checker"><input type="text" name="domain" placeholder="example.com" value="{clean_dom}" required><br><button type="submit">Check SPF</button></form>
    {res_box}{MONETIZATION_HTML}<hr style="border:0; border-top:1px solid #334155; margin:30px 0;">
    <p>Don't have an SPF record? <a href="/spf-generator">Generate an SPF Record here &rarr;</a></p>
    </div></body></html>'''
    return HTMLResponse(content=html)


# --- 3. DMARC Checker ---
@app.get("/dmarc-checker", response_class=HTMLResponse)
@app.post("/dmarc-checker", response_class=HTMLResponse)
async def dmarc_checker(domain: str = Form(default="")):
    dmarc_record, error = None, None
    clean_dom = clean_domain_name(domain)
    if clean_dom:
        try:
            answers = dns.resolver.resolve(f"_dmarc.{clean_dom}", 'TXT')
            for rdata in answers:
                txt_string = rdata.to_text().strip('"')
                if txt_string.startswith('v=DMARC1'):
                    dmarc_record = txt_string
                    break
            if not dmarc_record:
                error = "No DMARC record found for this domain."
        except Exception:
            error = "Unable to resolve DMARC record."

    res_box = f'<div class="res-box"><h3 style="margin:0;">✅ Valid DMARC Record Found:</h3><code>{dmarc_record}</code></div>' if dmarc_record else ""
    if error and clean_dom:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    html = f'''<!DOCTYPE html><html><head><title>Free DMARC Record Checker | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>🔐 Free DMARC Record Checker</h1><p>Test and validate domain DMARC records to prevent spoofing.</p>
    <form method="POST" action="/dmarc-checker"><input type="text" name="domain" placeholder="example.com" value="{clean_dom}" required><br><button type="submit">Check DMARC</button></form>
    {res_box}{MONETIZATION_HTML}<hr style="border:0; border-top:1px solid #334155; margin:30px 0;">
    <p>Need to create a policy? <a href="/dmarc-generator">Generate a DMARC Record here &rarr;</a></p>
    </div></body></html>'''
    return HTMLResponse(content=html)


# --- 4. MX Lookup ---
@app.get("/mx-lookup", response_class=HTMLResponse)
@app.post("/mx-lookup", response_class=HTMLResponse)
async def mx_lookup(domain: str = Form(default="")):
    mx_records, error = [], None
    clean_dom = clean_domain_name(domain)
    if clean_dom:
        try:
            answers = dns.resolver.resolve(clean_dom, 'MX')
            for rdata in answers:
                mx_records.append(f"Priority: {rdata.preference} -> Host: {rdata.exchange.to_text()}")
            if not mx_records:
                error = "No MX records found."
        except Exception:
            error = "Unable to fetch MX records."

    records_html = "".join([f"<code>{r}</code>" for r in mx_records])
    res_box = f'<div class="res-box"><h3 style="margin:0;">📬 MX Records ({len(mx_records)}):</h3>{records_html}</div>' if mx_records else ""
    if error and clean_dom:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    html = f'''<!DOCTYPE html><html><head><title>Free MX Record Lookup | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>📬 Free MX Lookup Tool</h1><p>Identify active mail servers for any domain.</p>
    <form method="POST" action="/mx-lookup"><input type="text" name="domain" placeholder="example.com" value="{clean_dom}" required><br><button type="submit">Lookup MX</button></form>
    {res_box}{MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)


# --- 5. TXT Lookup ---
@app.get("/txt-lookup", response_class=HTMLResponse)
@app.post("/txt-lookup", response_class=HTMLResponse)
async def txt_lookup(domain: str = Form(default="")):
    txt_records, error = [], None
    clean_dom = clean_domain_name(domain)
    if clean_dom:
        try:
            answers = dns.resolver.resolve(clean_dom, 'TXT')
            for rdata in answers:
                txt_records.append(rdata.to_text().strip('"'))
            if not txt_records:
                error = "No TXT records found."
        except Exception:
            error = "Unable to fetch TXT records."

    records_html = "".join([f"<code>{r}</code>" for r in txt_records])
    res_box = f'<div class="res-box"><h3 style="margin:0;">📝 TXT Records ({len(txt_records)}):</h3>{records_html}</div>' if txt_records else ""
    if error and clean_dom:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    html = f'''<!DOCTYPE html><html><head><title>Free TXT Record Lookup | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>📝 Free TXT Record Lookup</h1><p>Inspect all active DNS TXT records.</p>
    <form method="POST" action="/txt-lookup"><input type="text" name="domain" placeholder="example.com" value="{clean_dom}" required><br><button type="submit">Lookup TXT</button></form>
    {res_box}{MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)


# --- 6. SPF Generator ---
@app.get("/spf-generator", response_class=HTMLResponse)
@app.post("/spf-generator", response_class=HTMLResponse)
async def spf_generator(include_google: str = Form(default="no"), include_outlook: str = Form(default="no"), strictness: str = Form(default="~all")):
    includes = []
    if include_google == "yes":
        includes.append("include:_spf.google.com")
    if include_outlook == "yes":
        includes.append("include:spf.protection.outlook.com")

    inc_str = " " + " ".join(includes) if includes else ""
    generated_record = f"v=spf1 mx a{inc_str} {strictness}"

    html = f'''<!DOCTYPE html><html><head><title>Free SPF Record Generator | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>⚙️ Free SPF Record Generator</h1><p>Generate a customized SPF record for your domain in seconds.</p>
    <form method="POST" action="/spf-generator">
        <label>Include Google Workspace?</label><br>
        <select name="include_google"><option value="no">No</option><option value="yes" {"selected" if include_google=="yes" else ""}>Yes</option></select><br>
        <label>Include Microsoft 365 / Outlook?</label><br>
        <select name="include_outlook"><option value="no">No</option><option value="yes" {"selected" if include_outlook=="yes" else ""}>Yes</option></select><br>
        <label>Policy Strictness:</label><br>
        <select name="strictness">
            <option value="~all" {"selected" if strictness=="~all" else ""}>Soft Fail (~all) - Recommended</option>
            <option value="-all" {"selected" if strictness=="-all" else ""}>Hard Fail (-all) - Strict</option>
        </select><br><br>
        <button type="submit">Generate SPF Record</button>
    </form>
    <div class="res-box"><h3 style="margin:0;">Generated SPF Record:</h3><code>{generated_record}</code></div>
    {MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)


# --- 7. DMARC Generator ---
@app.get("/dmarc-generator", response_class=HTMLResponse)
@app.post("/dmarc-generator", response_class=HTMLResponse)
async def dmarc_generator(policy: str = Form(default="none"), email: str = Form(default="admin@example.com")):
    generated_record = f"v=DMARC1; p={policy}; rua=mailto:{email};"

    html = f'''<!DOCTYPE html><html><head><title>Free DMARC Record Generator | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>🛠️ Free DMARC Record Generator</h1><p>Create a valid DMARC record to secure your email domain.</p>
    <form method="POST" action="/dmarc-generator">
        <label>Policy (p):</label><br>
        <select name="policy">
            <option value="none" {"selected" if policy=="none" else ""}>None (Monitoring only)</option>
            <option value="quarantine" {"selected" if policy=="quarantine" else ""}>Quarantine (Send to Spam)</option>
            <option value="reject" {"selected" if policy=="reject" else ""}>Reject (Block unauthenticated emails)</option>
        </select><br>
        <label>Aggregate Report Email (rua):</label><br>
        <input type="text" name="email" value="{email}" required><br>
        <button type="submit">Generate DMARC Record</button>
    </form>
    <div class="res-box"><h3 style="margin:0;">Generated DMARC Record:</h3><code>{generated_record}</code></div>
    {MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)


# --- 8. BIMI Generator ---
@app.get("/bimi-generator", response_class=HTMLResponse)
@app.post("/bimi-generator", response_class=HTMLResponse)
async def bimi_generator(svg_url: str = Form(default="https://example.com/logo.svg")):
    clean_url = svg_url.strip()
    generated_record = f"v=BIMI1; l={clean_url}; a=;"

    html = f'''<!DOCTYPE html><html><head><title>Free BIMI Record Generator | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>🎨 Free BIMI Record Generator</h1><p>Display your official brand logo inside Gmail and Yahoo inboxes.</p>
    <form method="POST" action="/bimi-generator">
        <label>HTTPS URL of your SVG Logo:</label><br>
        <input type="text" name="svg_url" value="{clean_url}" required><br>
        <button type="submit">Generate BIMI Record</button>
    </form>
    <div class="res-box"><h3 style="margin:0;">Generated BIMI Record (TXT for default._bimi):</h3><code>{generated_record}</code></div>
    {MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)


# --- 9. Spam Words Analyzer ---
@app.get("/spam-analyzer", response_class=HTMLResponse)
@app.post("/spam-analyzer", response_class=HTMLResponse)
async def spam_analyzer(email_body: str = Form(default="")):
    spam_words = ["free", "buy now", "guaranteed", "earn money", "no risk", "100%", "click here", "urgent", "winner", "cash"]
    found_triggers = []
    
    if email_body:
        lower_text = email_body.lower()
        for word in spam_words:
            if re.search(r'\b' + re.escape(word) + r'\b', lower_text):
                found_triggers.append(word)

    res_box = ""
    if email_body:
        if found_triggers:
            triggers_str = ", ".join([f"'{w}'" for w in found_triggers])
            res_box = f'<div class="err-box">⚠️ <strong>Spam Triggers Detected!</strong> Your message contains high-risk spam keywords: <code>{triggers_str}</code>. Consider removing them to improve inbox rate.</div>'
        else:
            res_box = '<div class="res-box">✅ <strong>Clean Email Content!</strong> No common spam trigger words were detected in your text.</div>'

    html = f'''<!DOCTYPE html><html><head><title>Email Spam Words & Content Analyzer | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>📧 Free Email Spam Content Analyzer</h1><p>Scan your email copy for trigger words that land messages in Spam folders.</p>
    <form method="POST" action="/spam-analyzer">
        <label>Paste your Email Subject or Body Text:</label><br>
        <textarea name="email_body" placeholder="Paste your message here..." required>{email_body}</textarea><br>
        <button type="submit">Analyze Content</button>
    </form>
    {res_box}{MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)


# --- 10. Automated Uptime Monitor ---
@app.get("/uptime-monitor", response_class=HTMLResponse)
def uptime_monitor():
    html = f'''<!DOCTYPE html><html><head><title>24/7 Automated Domain & Email Uptime Monitor | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>📡 Automated 24/7 Monitoring (Enterprise SaaS)</h1>
    <p>Get instant SMS & Telegram notifications if your domain gets blacklisted, SSL expires, or MX records fail.</p>
    
    <div style="background:#0f172a; padding:20px; border-radius:8px; border:1px solid #334155; margin:20px 0;">
        <h3 style="color:#38bdf8; margin-top:0;">Features Included:</h3>
        <ul style="color:#94a3b8; line-height:1.8;">
            <li>Continuous Blacklist Auditing (Over 100+ RBLs)</li>
            <li>SSL Certificate Expiration Reminders (7-day advance alert)</li>
            <li>DNS Drift & MX Record Change Tracking</li>
            <li>Weekly Automated PDF Security Reports to your Inbox</li>
        </ul>
    </div>
    {MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)


# --- 11. PTR Lookup & SSL Checker ---
@app.get("/ptr-lookup", response_class=HTMLResponse)
@app.post("/ptr-lookup", response_class=HTMLResponse)
async def ptr_lookup(ip: str = Form(default="")):
    ptr_record, error = None, None
    clean_ip = ip.strip()
    if clean_ip:
        try:
            reversed_dns = dns.reversename.from_address(clean_ip)
            answers = dns.resolver.resolve(reversed_dns, 'PTR')
            ptr_record = answers[0].to_text().rstrip('.')
        except Exception:
            error = "Could not resolve PTR record for this IP address."

    res_box = f'<div class="res-box"><h3 style="margin:0;">✅ PTR Record Found:</h3><code>{ptr_record}</code></div>' if ptr_record else ""
    if error and clean_ip:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    html = f'''<!DOCTYPE html><html><head><title>Free Reverse DNS PTR Lookup | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>🔄 Reverse DNS (PTR) Lookup</h1><p>Verify if an IP address resolves to a valid domain hostname.</p>
    <form method="POST" action="/ptr-lookup"><input type="text" name="ip" placeholder="e.g. 8.8.8.8" value="{clean_ip}" required><br><button type="submit">Lookup PTR</button></form>
    {res_box}{MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)


@app.get("/ssl-checker", response_class=HTMLResponse)
@app.post("/ssl-checker", response_class=HTMLResponse)
async def ssl_checker(domain: str = Form(default="")):
    ssl_info, error = None, None
    clean_dom = clean_domain_name(domain)
    if clean_dom:
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((clean_dom, 443), timeout=5) as sock:
                with ctx.wrap_socket(sock, server_hostname=clean_dom) as ssock:
                    cert = ssock.getpeercert()
                    issuer = dict(x[0] for x in cert['issuer'])
                    ssl_info = f"Issuer: {issuer.get('organizationName', 'N/A')} | Expires: {cert['notAfter']}"
        except Exception:
            error = "Could not verify SSL certificate for this domain."

    res_box = f'<div class="res-box"><h3 style="margin:0;">🔒 SSL Certificate Details:</h3><code>{ssl_info}</code></div>' if ssl_info else ""
    if error and clean_dom:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    html = f'''<!DOCTYPE html><html><head><title>Free SSL Certificate Checker | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>🔒 Free SSL Certificate Checker</h1><p>Inspect SSL expiration dates and issuer details instantly.</p>
    <form method="POST" action="/ssl-checker"><input type="text" name="domain" placeholder="example.com" value="{clean_dom}" required><br><button type="submit">Check SSL</button></form>
    {res_box}{MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)


# --- 12. Security News ---
@app.get("/news", response_class=HTMLResponse)
def get_security_news():
    news_items = []
    try:
        req = urllib.request.Request("https://feeds.feedburner.com/TheHackersNews", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            xml_data = resp.read()
            root = ET.fromstring(xml_data)
            for item in root.findall('./channel/item')[:6]:
                title = item.find('title').text if item.find('title') is not None else "Cybersecurity Update"
                link = item.find('link').text if item.find('link') is not None else "#"
                desc = item.find('description').text if item.find('description') is not None else ""
                clean_desc = desc.split('<')[0][:140] + "..."
                news_items.append(f'<div class="news-card"><h3><a href="{link}" target="_blank">{title} &rarr;</a></h3><p>{clean_desc}</p></div>')
    except Exception:
        news_items.append('<div class="news-card"><p>Automated Feed Loading... Check back in a few minutes.</p></div>')

    news_html = "".join(news_items)
    html = f'''<!DOCTYPE html><html><head><title>Cybersecurity & Email Threat Intelligence | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>📰 Live Cybersecurity Threat Feed</h1><p>Real-time security updates, phishing vulnerabilities, and email safety news.</p>
    {news_html}{MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)


# --- 13. Sitemap.xml المحدث لـ 13 أداة صفحة ---
@app.get("/sitemap.xml")
def get_sitemap():
    sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>https://blacklistmail.com/</loc><priority>1.0</priority></url>
    <url><loc>https://blacklistmail.com/spf-checker</loc><priority>0.8</priority></url>
    <url><loc>https://blacklistmail.com/dmarc-checker</loc><priority>0.8</priority></url>
    <url><loc>https://blacklistmail.com/dkim-checker</loc><priority>0.8</priority></url>
    <url><loc>https://blacklistmail.com/mx-lookup</loc><priority>0.8</priority></url>
    <url><loc>https://blacklistmail.com/txt-lookup</loc><priority>0.8</priority></url>
    <url><loc>https://blacklistmail.com/spf-generator</loc><priority>0.8</priority></url>
    <url><loc>https://blacklistmail.com/dmarc-generator</loc><priority>0.8</priority></url>
    <url><loc>https://blacklistmail.com/bimi-generator</loc><priority>0.8</priority></url>
    <url><loc>https://blacklistmail.com/spam-analyzer</loc><priority>0.8</priority></url>
    <url><loc>https://blacklistmail.com/uptime-monitor</loc><priority>0.8</priority></url>
    <url><loc>https://blacklistmail.com/ptr-lookup</loc><priority>0.8</priority></url>
    <url><loc>https://blacklistmail.com/ssl-checker</loc><priority>0.8</priority></url>
    <url><loc>https://blacklistmail.com/news</loc><priority>0.8</priority></url>
</urlset>"""
    return Response(content=sitemap_xml, media_type="application/xml")


@app.get("/robots.txt")
def get_robots():
    return Response(content="User-agent: *\nAllow: /\nSitemap: https://blacklistmail.com/sitemap.xml", media_type="text/plain")


# --- APIs ---
@app.get("/api/v1/stats")
def get_global_stats():
    try:
        return {"success": True, "stats": get_live_dashboard_stats()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/audit/{domain}")
def audit_domain(domain: str):
    try:
        return {"success": True, "data": generate_audit_report(clean_domain_name(domain))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/download-pdf/{domain}")
def download_pdf_report(domain: str, background_tasks: BackgroundTasks):
    clean_dom = clean_domain_name(domain)
    pdf_filename = f"report_{clean_dom}.pdf"
    pdf_path = os.path.join(PDF_DIR, pdf_filename)
    try:
        report_data = generate_audit_report(clean_dom)
        generate_radar_pdf(report_data, pdf_path)
        background_tasks.add_task(os.remove, pdf_path)
        return FileResponse(path=pdf_path, filename=f"BlacklistMail_Radar_{clean_dom}.pdf", media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)