# routers/dns.py
import dns.resolver
import socket
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from utils import build_head_tags, clean_domain_name, MONETIZATION_HTML

router = APIRouter()

# ==========================================
# 1. أداة فحص سجلات البريد (MX Lookup)
# ==========================================
@router.get("/mx-lookup", response_class=HTMLResponse)
@router.post("/mx-lookup", response_class=HTMLResponse)
async def mx_lookup(domain: str = Form(default="")):
    mx_records = []
    error = None
    clean_dom = clean_domain_name(domain)

    if clean_dom:
        try:
            answers = dns.resolver.resolve(clean_dom, 'MX')
            for rdata in answers:
                mx_records.append({
                    "preference": rdata.preference,
                    "exchange": str(rdata.exchange).rstrip('.')
                })
            mx_records.sort(key=lambda x: x["preference"])
            if not mx_records:
                error = f"No MX records found for '{clean_dom}'."
        except Exception:
            error = f"Unable to resolve MX records for '{clean_dom}'."

    res_box = ""
    if mx_records:
        rows = "".join([f"<li><strong>Priority {item['preference']}:</strong> {item['exchange']}</li>" for item in mx_records])
        res_box = f'''
        <div class="res-box">
            <h3 style="margin:0 0 10px 0;">📫 MX Records Found ({len(mx_records)}):</h3>
            <ul style="margin:5px 0; padding-left:20px; line-height:1.6;">{rows}</ul>
        </div>'''
    elif error and clean_dom:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    head = build_head_tags(
        title="Free MX Record Lookup Tool | BlacklistMail",
        description="Perform a fast MX record lookup to verify mail server configurations for any domain.",
        canonical_url="https://blacklistmail.com/mx-lookup"
    )

    html = f'''<!DOCTYPE html><html lang="en">{head}
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>📫 Free MX Record Lookup</h1><p>Check the Mail Exchange (MX) DNS records and server priorities for your domain.</p>
    <form method="POST" action="/mx-lookup">
        <input type="text" name="domain" placeholder="example.com" value="{clean_dom}" required><br>
        <button type="submit">Lookup MX Records</button>
    </form>
    {res_box}{MONETIZATION_HTML}
    </div></body></html>'''

    return HTMLResponse(content=html)


# ==========================================
# 2. أداة البحث العكسي (PTR / Reverse DNS Lookup)
# ==========================================
@router.get("/ptr-lookup", response_class=HTMLResponse)
@router.post("/ptr-lookup", response_class=HTMLResponse)
async def ptr_lookup(ip_address: str = Form(default="")):
    hostname = None
    error = None
    clean_ip = ip_address.strip()

    if clean_ip:
        try:
            host, _, _ = socket.gethostbyaddr(clean_ip)
            hostname = host
        except Exception:
            error = f"No PTR record found or invalid IP address '{clean_ip}'."

    res_box = ""
    if hostname:
        res_box = f'''
        <div class="res-box">
            <h3 style="margin:0 0 5px 0;">🔄 Reverse DNS (PTR) Result:</h3>
            <p style="margin:0;"><strong>IP Address:</strong> {clean_ip}</p>
            <p style="margin:5px 0 0 0;"><strong>Resolved Hostname:</strong> <code>{hostname}</code></p>
        </div>'''
    elif error and clean_ip:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    head = build_head_tags(
        title="Free PTR Record / Reverse DNS Lookup | BlacklistMail",
        description="Perform a Reverse DNS (PTR) lookup on any IP address to find its mapped domain name.",
        canonical_url="https://blacklistmail.com/ptr-lookup"
    )

    html = f'''<!DOCTYPE html><html lang="en">{head}
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>🔄 Free Reverse DNS (PTR) Lookup</h1><p>Find the primary hostname associated with an IP address.</p>
    <form method="POST" action="/ptr-lookup">
        <input type="text" name="ip_address" placeholder="8.8.8.8" value="{clean_ip}" required><br>
        <button type="submit">Lookup PTR Record</button>
    </form>
    {res_box}{MONETIZATION_HTML}
    </div></body></html>'''

    return HTMLResponse(content=html)