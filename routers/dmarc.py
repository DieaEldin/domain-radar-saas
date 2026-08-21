# routers/dmarc.py
import dns.resolver
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from utils import build_head_tags, clean_domain_name, MONETIZATION_HTML

router = APIRouter()

# ==========================================
# 1. أداة توليد السجل (DMARC Generator)
# ==========================================
@router.get("/dmarc-generator", response_class=HTMLResponse)
@router.post("/dmarc-generator", response_class=HTMLResponse)
async def dmarc_generator(
    domain: str = Form(default=""),
    policy: str = Form(default="none"),
    rua_email: str = Form(default=""),
    pct: str = Form(default="100")
):
    clean_dom = clean_domain_name(domain)
    rua_str = f" rua=mailto:{rua_email.strip()};" if rua_email.strip() else ""
    pct_str = f" pct={pct.strip()};" if pct.strip() and pct != "100" else ""
    
    generated_record = f"v=DMARC1; p={policy};{rua_str}{pct_str}"

    head = build_head_tags(
        title="Free DMARC Record Generator | BlacklistMail",
        description="Create a valid DMARC DNS record for your domain to protect against spoofing and phishing.",
        canonical_url="https://blacklistmail.com/dmarc-generator"
    )

    html = f'''<!DOCTYPE html><html lang="en">{head}
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>⚙️ Free DMARC Record Generator</h1><p>Generate a customized DMARC policy for your domain in seconds.</p>
    <form method="POST" action="/dmarc-generator">
        <label>Domain Name:</label><br>
        <input type="text" name="domain" placeholder="example.com" value="{clean_dom}"><br>
        <label>Policy (p=):</label><br>
        <select name="policy">
            <option value="none" {"selected" if policy=="none" else ""}>None (Monitoring Only - Safe Start)</option>
            <option value="quarantine" {"selected" if policy=="quarantine" else ""}>Quarantine (Send to Spam)</option>
            <option value="reject" {"selected" if policy=="reject" else ""}>Reject (Block Unauthenticated Mail)</option>
        </select><br>
        <label>Aggregate Reports Email (RUA - Optional):</label><br>
        <input type="text" name="rua_email" placeholder="dmarc-reports@example.com" value="{rua_email}"><br>
        <label>Percentage Applied (pct=):</label><br>
        <input type="text" name="pct" placeholder="100" value="{pct}"><br><br>
        <button type="submit">Generate DMARC Record</button>
    </form>
    <div class="res-box"><h3 style="margin:0;">Generated DMARC Record:</h3><code>{generated_record}</code></div>
    {MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)


# ==========================================
# 2. أداة فحص السجل (DMARC Checker)
# ==========================================
@router.get("/dmarc-checker", response_class=HTMLResponse)
@router.post("/dmarc-checker", response_class=HTMLResponse)
async def dmarc_checker(domain: str = Form(default="")):
    dmarc_record, error = None, None
    clean_dom = clean_domain_name(domain)
    
    if clean_dom:
        dmarc_target = f"_dmarc.{clean_dom}"
        try:
            answers = dns.resolver.resolve(dmarc_target, 'TXT')
            for rdata in answers:
                txt_string = rdata.to_text().strip('"')
                if txt_string.startswith('v=DMARC1'):
                    dmarc_record = txt_string
                    break
            if not dmarc_record:
                error = f"No DMARC record found at {dmarc_target}."
        except Exception:
            error = f"Unable to resolve DMARC DNS record for {clean_dom}."

    res_box = f'<div class="res-box"><h3 style="margin:0;">✅ Valid DMARC Record Found:</h3><code>{dmarc_record}</code></div>' if dmarc_record else ""
    if error and clean_dom:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    head = build_head_tags(
        title="Free DMARC Record Checker & Validation Tool | BlacklistMail",
        description="Check and validate your domain's DMARC DNS record in real-time.",
        canonical_url="https://blacklistmail.com/dmarc-checker"
    )

    html = f'''<!DOCTYPE html><html lang="en">{head}
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>🛡️ Free DMARC Record Checker</h1><p>Check if your domain has a valid DMARC record configured.</p>
    <form method="POST" action="/dmarc-checker">
        <input type="text" name="domain" placeholder="example.com" value="{clean_dom}" required><br>
        <button type="submit">Check DMARC</button>
    </form>
    {res_box}{MONETIZATION_HTML}
    </div></body></html>'''
    
    return HTMLResponse(content=html)