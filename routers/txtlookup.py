import dns.resolver
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()

def get_txt_records(domain: str) -> list:
    """جلب سجلات TXT الفعلية للدومين"""
    try:
        clean_domain = domain.strip().lower().replace("http://", "").replace("https://", "").split("/")[0]
        answers = dns.resolver.resolve(clean_domain, 'TXT')
        records = []
        for rdata in answers:
            for txt_string in rdata.strings:
                records.append(txt_string.decode('utf-8'))
        return records
    except Exception as e:
        return [f"No TXT records found or resolution error: {str(e)}"]

@router.get("/txt-lookup", response_class=HTMLResponse)
async def txt_lookup_page(request: Request, domain: str = None):
    # إعداد وسوم SEO
    page_title = f"DNS TXT Record Lookup for {domain} | BlacklistMail" if domain else "Free DNS TXT Record Lookup Tool | BlacklistMail"
    meta_desc = f"Inspect and analyze live DNS TXT records for {domain}. Verify SPF, DMARC, DKIM, and site ownership." if domain else "Instantly query and analyze DNS TXT records for any domain to inspect SPF, DMARC, site verification, and security policies."
    
    # فحص وحساب النتائج عند البحث
    results_html = ""
    if domain:
        records = get_txt_records(domain)
        items_html = "".join([f"<li style='background: #1e293b; padding: 12px; margin-bottom: 8px; border-radius: 6px; word-break: break-all; font-family: monospace;'>{rec}</li>" for rec in records])
        results_html = f"""
        <div style="margin-top: 30px; text-align: left;">
            <h3>TXT Records for: <span style="color: #38bdf8;">{domain}</span></h3>
            <ul style="list-style: none; padding: 0;">
                {items_html}
            </ul>
        </div>
        """

    # بناء كود الـ HTML الكامل للصفحة
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <meta name="description" content="{meta_desc}">
    <link rel="canonical" href="https://blacklistmail.com/txt-lookup" />
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 40px 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }}
        a {{ color: #38bdf8; text-decoration: none; }}
        h1 {{ margin-top: 10px; color: #ffffff; }}
        input[type="text"] {{ width: 70%; padding: 12px; border-radius: 6px; border: 1px solid #334155; background: #0f172a; color: #fff; font-size: 16px; }}
        button {{ padding: 12px 24px; border-radius: 6px; border: none; background: #2563eb; color: #fff; font-size: 16px; cursor: pointer; font-weight: bold; }}
        button:hover {{ background: #1d4ed8; }}
    </style>
</head>
<body>
    <div class="container">
        <p><a href="/">&larr; Back to Dashboard</a></p>
        <h1>🔎 Free DNS TXT Record Lookup</h1>
        <p>Inspect all active TXT records published on your domain for SPF, DMARC, DKIM, and Domain Verification.</p>
        
        <form action="/txt-lookup" method="get" style="margin-top:20px;">
            <input type="text" name="domain" value="{domain if domain else ''}" placeholder="Enter domain name (e.g. workplaceemail.com)" required />
            <button type="submit">Lookup TXT</button>
        </form>

        {results_html}
    </div>
</body>
</html>"""

    return HTMLResponse(content=html_content)