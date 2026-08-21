# routers/dkim.py
import dns.resolver
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from utils import build_head_tags, clean_domain_name, MONETIZATION_HTML

router = APIRouter()

@router.get("/dkim-checker", response_class=HTMLResponse)
@router.post("/dkim-checker", response_class=HTMLResponse)
async def dkim_checker(domain: str = Form(default=""), selector: str = Form(default="google")):
    dkim_record, error = None, None
    clean_dom = clean_domain_name(domain)
    clean_sel = selector.strip()
    
    if clean_dom and clean_sel:
        dkim_target = f"{clean_sel}._domainkey.{clean_dom}"
        try:
            answers = dns.resolver.resolve(dkim_target, 'TXT')
            for rdata in answers:
                txt_string = rdata.to_text().strip('"')
                if 'v=DKIM1' in txt_string or 'p=' in txt_string:
                    dkim_record = txt_string
                    break
            if not dkim_record:
                error = f"No DKIM record found at selector '{clean_sel}' for domain '{clean_dom}'."
        except Exception:
            error = f"Unable to resolve DKIM DNS record for {dkim_target}. Please check the selector and domain."

    res_box = f'<div class="res-box"><h3 style="margin:0;">✅ Valid DKIM Record Found:</h3><code>{dkim_record}</code></div>' if dkim_record else ""
    if error and clean_dom:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    head = build_head_tags(
        title="Free DKIM Record Checker & Validation Tool | BlacklistMail",
        description="Verify and check your domain's DKIM selector TXT record in real time.",
        canonical_url="https://blacklistmail.com/dkim-checker"
    )

    html = f'''<!DOCTYPE html><html lang="en">{head}
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>🔑 Free DKIM Record Checker</h1><p>Validate your DKIM DNS record using your specific domain selector.</p>
    <form method="POST" action="/dkim-checker">
        <label>Domain Name:</label><br>
        <input type="text" name="domain" placeholder="example.com" value="{clean_dom}" required><br>
        <label>DKIM Selector (e.g., google, default, k1):</label><br>
        <input type="text" name="selector" placeholder="google" value="{clean_sel}" required><br><br>
        <button type="submit">Check DKIM</button>
    </form>
    {res_box}{MONETIZATION_HTML}
    </div></body></html>'''
    
    return HTMLResponse(content=html)