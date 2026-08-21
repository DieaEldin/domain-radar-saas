# routers/bimi.py
import dns.resolver
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from utils import build_head_tags, clean_domain_name, MONETIZATION_HTML

router = APIRouter()

# ==========================================
# 1. أداة توليد السجل (BIMI Generator)
# ==========================================
@router.get("/bimi-generator", response_class=HTMLResponse)
@router.post("/bimi-generator", response_class=HTMLResponse)
async def bimi_generator(
    logo_url: str = Form(default=""),
    vmc_url: str = Form(default="")
):
    clean_logo = logo_url.strip()
    clean_vmc = vmc_url.strip()

    vmc_str = f" a={clean_vmc};" if clean_vmc else ""
    generated_record = f"v=BIMI1; l={clean_logo};{vmc_str}" if clean_logo else "v=BIMI1; l=;"

    head = build_head_tags(
        title="Free BIMI Record Generator | BlacklistMail",
        description="Generate a valid BIMI DNS record with your SVG logo and VMC certificate to show your brand logo in inboxes.",
        canonical_url="https://blacklistmail.com/bimi-generator"
    )

    html = f'''<!DOCTYPE html><html lang="en">{head}
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>🎨 Free BIMI Record Generator</h1><p>Create a BIMI DNS record to display your logo next to emails in Gmail, Yahoo, and Outlook.</p>
    <form method="POST" action="/bimi-generator">
        <label>SVG Logo URL (Must be HTTPS & SVG Tiny PS format):</label><br>
        <input type="text" name="logo_url" placeholder="https://example.com/logo.svg" value="{clean_logo}" required><br>
        <label>VMC Certificate URL (Optional):</label><br>
        <input type="text" name="vmc_url" placeholder="https://example.com/cert.pem" value="{clean_vmc}"><br><br>
        <button type="submit">Generate BIMI Record</button>
    </form>
    <div class="res-box"><h3 style="margin:0;">Generated BIMI Record:</h3><code>{generated_record}</code></div>
    {MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)


# ==========================================
# 2. أداة فحص السجل (BIMI Inspector)
# ==========================================
@router.get("/bimi-inspector", response_class=HTMLResponse)
@router.post("/bimi-inspector", response_class=HTMLResponse)
async def bimi_inspector(domain: str = Form(default="")):
    bimi_record, error = None, None
    clean_dom = clean_domain_name(domain)
    
    if clean_dom:
        bimi_target = f"default._bimi.{clean_dom}"
        try:
            answers = dns.resolver.resolve(bimi_target, 'TXT')
            for rdata in answers:
                txt_string = rdata.to_text().strip('"')
                if txt_string.startswith('v=BIMI1'):
                    bimi_record = txt_string
                    break
            if not bimi_record:
                error = f"No BIMI record found at {bimi_target}."
        except Exception:
            error = f"Unable to resolve BIMI DNS record for {clean_dom}."

    res_box = f'<div class="res-box"><h3 style="margin:0;">✅ Valid BIMI Record Found:</h3><code>{bimi_record}</code></div>' if bimi_record else ""
    if error and clean_dom:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    head = build_head_tags(
        title="Free BIMI Inspector & Checker Tool | BlacklistMail",
        description="Inspect and validate your domain's Brand Indicators for Message Identification (BIMI) DNS record.",
        canonical_url="https://blacklistmail.com/bimi-inspector"
    )

    html = f'''<!DOCTYPE html><html lang="en">{head}
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>🔍 Free BIMI Inspector</h1><p>Verify if your domain has a valid BIMI DNS record and logo configuration.</p>
    <form method="POST" action="/bimi-inspector">
        <input type="text" name="domain" placeholder="example.com" value="{clean_dom}" required><br>
        <button type="submit">Inspect BIMI</button>
    </form>
    {res_box}{MONETIZATION_HTML}
    </div></body></html>'''
    
    return HTMLResponse(content=html)