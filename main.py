import os
import dns.resolver
from fastapi import FastAPI, HTTPException, BackgroundTasks, Response, Form, Request
from fastapi.responses import HTMLResponse, FileResponse

# 1. استيراد دالة الفحص ودالة الإحصائيات ودالة الـ PDF
from blacklist_checker import generate_audit_report, get_live_dashboard_stats
from pdf_generator import generate_radar_pdf

# 2. إنشاء تطبيق FastAPI
app = FastAPI(
    title="BlacklistMail Radar API",
    description="Enterprise Domain Intelligence, Email Security & Blacklist Audit API",
    version="1.1.0",
)

# 3. إنشاء مجلد مؤقت لحفظ تقارير PDF
PDF_DIR = "./generated_reports"
os.makedirs(PDF_DIR, exist_ok=True)


# 4. مسار عرض واجهة الـ Dashboard الرسمية
@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    """عرض لوحة التحكم الرئيسية من ملف dashboard.html"""
    html_file_path = "dashboard.html"
    if not os.path.exists(html_file_path):
        raise HTTPException(
            status_code=404,
            detail="dashboard.html file not found. Please place it in the same directory.",
        )

    with open(html_file_path, "r", encoding="utf-8") as f:
        return f.read()


# 5. مسار أداة فحص الـ SPF (FastAPI Compatible)
@app.get("/spf-checker", response_class=HTMLResponse)
@app.post("/spf-checker", response_class=HTMLResponse)
async def spf_checker(domain: str = Form(default="")):
    spf_record = None
    error = None
    clean_domain = domain.strip().lower().replace("http://", "").replace("https://", "").split("/")[0]

    if clean_domain:
        try:
            answers = dns.resolver.resolve(clean_domain, 'TXT')
            for rdata in answers:
                txt_string = rdata.to_text().strip('"')
                if txt_string.startswith('v=spf1'):
                    spf_record = txt_string
                    break
            if not spf_record:
                error = "لم يتم العثور على سجل SPF لهذا الدومين."
        except Exception:
            error = "تعذر جلب البيانات، تأكد من صحة اسم الدومين."

    # تصميم الواجهة مباشرة
    result_box = ""
    if spf_record:
        result_box = f'''
        <div style="background: #e8f5e9; border: 1px solid #4caf50; padding: 15px; border-radius: 6px; margin-top: 20px;">
            <h3 style="color: #2e7d32; margin-top:0;">✅ Valid SPF Record Found:</h3>
            <code style="background: #fff; padding: 10px; display: block; border-radius: 4px; font-weight: bold; word-break: break-all;">{spf_record}</code>
        </div>'''
    elif error and clean_domain:
        result_box = f'''
        <div style="background: #ffebee; border: 1px solid #ef5350; padding: 15px; border-radius: 6px; margin-top: 20px; color: #c62828;">
            ⚠️ {error}
        </div>'''

    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Free SPF Record Checker & Lookup Tool | BlacklistMail</title>
        <meta name="description" content="Free online SPF Record Checker. Validate your SPF syntax, prevent email spoofing, and ensure proper email deliverability.">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8f9fa; color: #333; margin: 0; padding: 20px; }}
            .container {{ max-width: 750px; margin: 40px auto; background: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
            h1 {{ color: #111; font-size: 26px; margin-bottom: 10px; }}
            input[type="text"] {{ padding: 12px 15px; width: 68%; border: 1px solid #ccc; border-radius: 6px; font-size: 15px; }}
            button {{ padding: 12px 20px; background: #0066ff; color: white; border: none; border-radius: 6px; font-size: 15px; cursor: pointer; font-weight: bold; }}
            button:hover {{ background: #0052cc; }}
            a {{ color: #0066ff; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <p><a href="/">&larr; Back to Dashboard</a></p>
            <h1>🛡️ Free SPF Record Checker</h1>
            <p>Enter your domain name to test and validate its SPF (Sender Policy Framework) record in real-time.</p>
            
            <form method="POST" action="/spf-checker" style="margin: 25px 0;">
                <input type="text" name="domain" placeholder="example.com" value="{clean_domain}" required>
                <button type="submit">Check SPF</button>
            </form>

            {result_box}

            <hr style="margin: 35px 0; border: 0; border-top: 1px solid #eee;">
            <h2>Why is SPF validation important?</h2>
            <p>Sender Policy Framework (SPF) protects your domain against spoofing and helps your emails reach the inbox instead of spam folders.</p>
        </div>
    </body>
    </html>
    '''
    return HTMLResponse(content=html_content)


# 6. مسار خريطة الموقع sitemap.xml
@app.get("/sitemap.xml")
def get_sitemap():
    """إرجاع خريطة الموقع بتنسيق XML حقيقي"""
    sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://blacklistmail.com/</loc>
        <lastmod>2026-08-14</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://blacklistmail.com/dashboard</loc>
        <lastmod>2026-08-14</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://blacklistmail.com/spf-checker</loc>
        <lastmod>2026-08-14</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
</urlset>"""
    return Response(content=sitemap_xml, media_type="application/xml")


# 7. مسار ملف robots.txt
@app.get("/robots.txt")
def get_robots():
    robots_text = """User-agent: *
Allow: /

Sitemap: https://blacklistmail.com/sitemap.xml"""
    return Response(content=robots_text, media_type="text/plain")


# 8. API endpoint للإحصائيات العامة
@app.get("/api/v1/stats")
def get_global_stats():
    try:
        stats = get_live_dashboard_stats()
        return {"success": True, "stats": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 9. API endpoint لنتائج الفحص JSON
@app.get("/api/v1/audit/{domain}")
def audit_domain(domain: str):
    try:
        clean_domain = (
            domain.strip()
            .lower()
            .replace("http://", "")
            .replace("https://", "")
            .split("/")[0]
        )
        report_data = generate_audit_report(clean_domain)
        return {"success": True, "data": report_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 10. API endpoint لتحميل تقرير PDF
@app.get("/api/v1/download-pdf/{domain}")
def download_pdf_report(domain: str, background_tasks: BackgroundTasks):
    clean_domain = (
        domain.strip()
        .lower()
        .replace("http://", "")
        .replace("https://", "")
        .split("/")[0]
    )
    pdf_filename = f"report_{clean_domain}.pdf"
    pdf_path = os.path.join(PDF_DIR, pdf_filename)

    try:
        report_data = generate_audit_report(clean_domain)
        generate_radar_pdf(report_data, pdf_path)
        background_tasks.add_task(os.remove, pdf_path)

        return FileResponse(
            path=pdf_path,
            filename=f"BlacklistMail_Radar_{clean_domain}.pdf",
            media_type="application/pdf",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate PDF: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)