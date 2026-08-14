import os
import dns.resolver
from fastapi import FastAPI, HTTPException, BackgroundTasks, Response, Form
from fastapi.responses import HTMLResponse, FileResponse

# 1. استيراد دالة الفحص ودالة الإحصائيات ودالة الـ PDF
from blacklist_checker import generate_audit_report, get_live_dashboard_stats
from pdf_generator import generate_radar_pdf

# 2. إنشاء تطبيق FastAPI
app = FastAPI(
    title="BlacklistMail Radar API",
    description="Enterprise Domain Intelligence, Email Security & Blacklist Audit API",
    version="1.2.0",
)

# 3. إنشاء مجلد مؤقت لحفظ تقارير PDF
PDF_DIR = "./generated_reports"
os.makedirs(PDF_DIR, exist_ok=True)

# CSS موحد واحترافي لجميع الصفحات الفرعية
COMMON_CSS = """
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8f9fa; color: #333; margin: 0; padding: 20px; }
.container { max-width: 750px; margin: 40px auto; background: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
h1 { color: #111; font-size: 26px; margin-bottom: 10px; }
input[type="text"] { padding: 12px 15px; width: 68%; border: 1px solid #ccc; border-radius: 6px; font-size: 15px; }
button { padding: 12px 20px; background: #0066ff; color: white; border: none; border-radius: 6px; font-size: 15px; cursor: pointer; font-weight: bold; }
button:hover { background: #0052cc; }
a { color: #0066ff; text-decoration: none; }
.res-box { background: #e8f5e9; border: 1px solid #4caf50; padding: 15px; border-radius: 6px; margin-top: 20px; }
.err-box { background: #ffebee; border: 1px solid #ef5350; padding: 15px; border-radius: 6px; margin-top: 20px; color: #c62828; }
code { background: #fff; padding: 10px; display: block; border-radius: 4px; font-weight: bold; word-break: break-all; margin-top: 8px; }
"""

def clean_domain_name(domain: str) -> str:
    return domain.strip().lower().replace("http://", "").replace("https://", "").split("/")[0]


# --- 4. مسار عرض واجهة الـ Dashboard الرئيسية ---
@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    html_file_path = "dashboard.html"
    if not os.path.exists(html_file_path):
        raise HTTPException(
            status_code=404,
            detail="dashboard.html file not found. Please place it in the same directory.",
        )
    with open(html_file_path, "r", encoding="utf-8") as f:
        return f.read()


# --- 5. أداة فحص SPF ---
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
                error = "لم يتم العثور على سجل SPF لهذا الدومين."
        except Exception:
            error = "تعذر جلب البيانات، تأكد من صحة اسم الدومين."

    res_box = f'<div class="res-box"><h3 style="color:#2e7d32;margin:0;">✅ Valid SPF Record Found:</h3><code>{spf_record}</code></div>' if spf_record else ""
    if error and clean_dom:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    html = f'''<!DOCTYPE html><html><head><title>Free SPF Record Checker | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>🛡️ Free SPF Record Checker</h1><p>Enter your domain name to test and validate its SPF record in real-time.</p>
    <form method="POST" action="/spf-checker"><input type="text" name="domain" placeholder="example.com" value="{clean_dom}" required><button type="submit">Check SPF</button></form>
    {res_box}<hr style="margin:30px 0; border:0; border-top:1px solid #eee;">
    <h2>Why is SPF important?</h2><p>Sender Policy Framework (SPF) protects your domain against email spoofing and improves email deliverability.</p>
    </div></body></html>'''
    return HTMLResponse(content=html)


# --- 6. أداة فحص DMARC ---
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
                error = "لم يتم العثور على سجل DMARC لهذا الدومين."
        except Exception:
            error = "تعذر جلب البيانات، أو لا يوجد سجل DMARC لهذا الدومين."

    res_box = f'<div class="res-box"><h3 style="color:#2e7d32;margin:0;">✅ Valid DMARC Record Found:</h3><code>{dmarc_record}</code></div>' if dmarc_record else ""
    if error and clean_dom:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    html = f'''<!DOCTYPE html><html><head><title>Free DMARC Record Checker | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>🔐 Free DMARC Record Checker</h1><p>Analyze your domain's DMARC record to protect against email spoofing and phishing.</p>
    <form method="POST" action="/dmarc-checker"><input type="text" name="domain" placeholder="example.com" value="{clean_dom}" required><button type="submit">Check DMARC</button></form>
    {res_box}<hr style="margin:30px 0; border:0; border-top:1px solid #eee;">
    <h2>Why is DMARC important?</h2><p>DMARC ensures only authorized senders can send emails on behalf of your domain name.</p>
    </div></body></html>'''
    return HTMLResponse(content=html)


# --- 7. أداة فحص MX Records ---
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
                error = "لم يتم العثور على سجلات MX لهذا الدومين."
        except Exception:
            error = "تعذر جلب سجلات MX، تأكد من صحة اسم الدومين."

    records_html = "".join([f"<code>{r}</code>" for r in mx_records])
    res_box = f'<div class="res-box"><h3 style="color:#2e7d32;margin:0;">📬 MX Records Found ({len(mx_records)}):</h3>{records_html}</div>' if mx_records else ""
    if error and clean_dom:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    html = f'''<!DOCTYPE html><html><head><title>Free MX Lookup Tool | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>📬 Free MX Record Lookup</h1><p>Check the Mail Exchange (MX) servers for any domain name instantly.</p>
    <form method="POST" action="/mx-lookup"><input type="text" name="domain" placeholder="example.com" value="{clean_dom}" required><button type="submit">Lookup MX</button></form>
    {res_box}<hr style="margin:30px 0; border:0; border-top:1px solid #eee;">
    <h2>What is an MX record?</h2><p>MX records specify the mail servers responsible for accepting email messages on behalf of a domain.</p>
    </div></body></html>'''
    return HTMLResponse(content=html)


# --- 8. أداة فحص جميع سجلات TXT ---
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
                error = "لم يتم العثور على أي سجلات TXT لهذا الدومين."
        except Exception:
            error = "تعذر جلب سجلات TXT."

    records_html = "".join([f"<code>{r}</code>" for r in txt_records])
    res_box = f'<div class="res-box"><h3 style="color:#2e7d32;margin:0;">📝 TXT Records Found ({len(txt_records)}):</h3>{records_html}</div>' if txt_records else ""
    if error and clean_dom:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    html = f'''<!DOCTYPE html><html><head><title>Free TXT Record Lookup | BlacklistMail</title><style>{COMMON_CSS}</style></head>
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>📝 Free TXT Record Lookup</h1><p>Lookup and inspect all DNS TXT records for any domain.</p>
    <form method="POST" action="/txt-lookup"><input type="text" name="domain" placeholder="example.com" value="{clean_dom}" required><button type="submit">Lookup TXT</button></form>
    {res_box}<hr style="margin:30px 0; border:0; border-top:1px solid #eee;">
    <h2>What are TXT records?</h2><p>TXT records store text-based information for external sources, often used for domain verification and security policies.</p>
    </div></body></html>'''
    return HTMLResponse(content=html)


# --- 9. مسار خريطة الموقع المحدثة سحابياً sitemap.xml ---
@app.get("/sitemap.xml")
def get_sitemap():
    sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>https://blacklistmail.com/</loc><lastmod>2026-08-14</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>
    <url><loc>https://blacklistmail.com/dashboard</loc><lastmod>2026-08-14</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
    <url><loc>https://blacklistmail.com/spf-checker</loc><lastmod>2026-08-14</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
    <url><loc>https://blacklistmail.com/dmarc-checker</loc><lastmod>2026-08-14</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
    <url><loc>https://blacklistmail.com/mx-lookup</loc><lastmod>2026-08-14</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
    <url><loc>https://blacklistmail.com/txt-lookup</loc><lastmod>2026-08-14</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
</urlset>"""
    return Response(content=sitemap_xml, media_type="application/xml")


# --- 10. مسار robots.txt ---
@app.get("/robots.txt")
def get_robots():
    robots_text = """User-agent: *
Allow: /

Sitemap: https://blacklistmail.com/sitemap.xml"""
    return Response(content=robots_text, media_type="text/plain")


# --- 11. API endpoints الحالية للبيانات والإحصائيات وتنزيل ה-PDF ---
@app.get("/api/v1/stats")
def get_global_stats():
    try:
        stats = get_live_dashboard_stats()
        return {"success": True, "stats": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/audit/{domain}")
def audit_domain(domain: str):
    try:
        clean_dom = clean_domain_name(domain)
        report_data = generate_audit_report(clean_dom)
        return {"success": True, "data": report_data}
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

        return FileResponse(
            path=pdf_path,
            filename=f"BlacklistMail_Radar_{clean_dom}.pdf",
            media_type="application/pdf",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate PDF: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)