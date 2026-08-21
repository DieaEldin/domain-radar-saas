import os
import urllib.request
import xml.etree.ElementTree as ET
from fastapi import FastAPI, BackgroundTasks, HTTPException, Response
from fastapi.responses import HTMLResponse, FileResponse

# استيراد الدوال الأساسية للمحرك
from blacklist_checker import generate_audit_report, get_live_dashboard_stats
from pdf_generator import generate_radar_pdf

# استيراد الـ Routers الخاصة بالأدوات والصفحات
from routers import spf, dmarc, dkim, bimi, security, dns, company, services, txtlookup

app = FastAPI(
    title="BlacklistMail Radar API",
    description="Enterprise Domain Intelligence, Email Security & Automated Monetized SaaS",
    version="3.0.0",
)

# 1. ربط أدوات الفحص والأمان
app.include_router(spf.router)       # SPF Tools
app.include_router(dmarc.router)     # DMARC Tools
app.include_router(dkim.router)      # DKIM Checker
app.include_router(bimi.router)      # BIMI Tools
app.include_router(security.router)  # Security & SSL
app.include_router(dns.router)       # DNS Lookups (MX, PTR)
app.include_router(txtlookup.router) # TXT Lookup

# 2. ربط الخدمات والصفحات الإدارية
app.include_router(services.router)  # Delisting, Uptime, News, Platform
app.include_router(company.router)   # Pricing, About, Contact, Status, Sitemap

# إعداد مجلد حفظ ملفات الـ PDF المؤقتة
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

def build_head_tags(title: str, description: str, canonical_url: str) -> str:
    return f"""
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    
    <!-- Open Graph Tags -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="https://blacklistmail.com/static/og-image.png">
    
    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{canonical_url}">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="https://blacklistmail.com/static/og-image.png">

    <link rel="sitemap" type="application/xml" title="Sitemap" href="https://blacklistmail.com/sitemap.xml" />
    <style>{COMMON_CSS}</style>
</head>
"""

# --- Dashboard ---
@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    html_file_path = "dashboard.html"
    if not os.path.exists(html_file_path):
        raise HTTPException(status_code=404, detail="dashboard.html file not found.")
    with open(html_file_path, "r", encoding="utf-8") as f:
        return f.read()

# --- Automated Uptime Monitor ---
@app.get("/uptime-monitor", response_class=HTMLResponse)
def uptime_monitor():
    head = build_head_tags(
        title="Automated Domain & Email Uptime Monitor | BlacklistMail",
        description="Get instant 24/7 alerts for domain blacklist changes, SSL certificate expiry, and DNS MX record issues to protect reputation.",
        canonical_url="https://blacklistmail.com/uptime-monitor"
    )

    html = f'''<!DOCTYPE html><html lang="en">{head}
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

# --- Security News ---
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

    head = build_head_tags(
        title="Cybersecurity Threat Feed & News | BlacklistMail",
        description="Stay updated with real-time email security threats, vulnerabilities, phishing tactics, and cyber security news updated continuously.",
        canonical_url="https://blacklistmail.com/news"
    )

    html = f'''<!DOCTYPE html><html lang="en">{head}
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>📰 Live Cybersecurity Threat Feed</h1><p>Real-time security updates, phishing vulnerabilities, and email safety news.</p>
    {news_html}{MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)

# --- Sitemap & Robots ---
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
    <url><loc>https://blacklistmail.com/pricing</loc><priority>0.8</priority></url>
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

# ✅ تعديل وحل مشكلة تحميل الـ PDF مع تنظيف الملفات تلقائياً
@app.get("/api/v1/download-pdf/{domain}")
def download_pdf_report(domain: str, background_tasks: BackgroundTasks):
    clean_dom = clean_domain_name(domain)
    pdf_filename = f"report_{clean_dom}.pdf"
    pdf_path = os.path.join(PDF_DIR, pdf_filename)
    try:
        report_data = generate_audit_report(clean_dom)
        generate_radar_pdf(report_data, pdf_path)
        
        # إضافة مهمة خلفية لحذف الملف بعد انتهاء عملية التحميل للعميل
        background_tasks.add_task(os.remove, pdf_path)
        
        return FileResponse(
            path=pdf_path, 
            filename=f"BlacklistMail_Radar_{clean_dom}.pdf", 
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Pricing Page ---
@app.get("/pricing", response_class=HTMLResponse)
async def read_pricing():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pricing_path = os.path.join(base_dir, "templates", "pricing.html")
    
    if not os.path.exists(pricing_path):
        pricing_path = os.path.join(base_dir, "pricing.html")
        
    if not os.path.exists(pricing_path):
        raise HTTPException(status_code=404, detail="Pricing page template not found.")
        
    with open(pricing_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)