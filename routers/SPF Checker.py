# routers/spf.py
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from utils import build_head_tags, clean_domain_name, MONETIZATION_HTML

router = APIRouter()

@router.get("/spf-generator", response_class=HTMLResponse)
@router.post("/spf-generator", response_class=HTMLResponse)
async def spf_generator(include_google: str = Form(default="no"), include_outlook: str = Form(default="no"), strictness: str = Form(default="~all")):
    includes = []
    if include_google == "yes":
        includes.append("include:_spf.google.com")
    if include_outlook == "yes":
        includes.append("include:spf.protection.outlook.com")

    inc_str = " " + " ".join(includes) if includes else ""
    generated_record = f"v=spf1 mx a{inc_str} {strictness}"

    head = build_head_tags(
        title="Free SPF Record Generator | BlacklistMail",
        description="Generate a custom, valid SPF DNS record for Google Workspace, Outlook, or custom servers to maximize inbox delivery and security.",
        canonical_url="https://blacklistmail.com/spf-generator"
    )

    html = f'''<!DOCTYPE html><html lang="en">{head}
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