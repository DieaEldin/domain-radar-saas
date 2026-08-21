# routers/security.py
import socket
import ssl
from datetime import datetime
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from utils import build_head_tags, clean_domain_name, MONETIZATION_HTML

router = APIRouter()

# ==========================================
# 1. أداة فحص شهادة الأمان (SSL/TLS Checker)
# ==========================================
@router.get("/ssl-checker", response_class=HTMLResponse)
@router.post("/ssl-checker", response_class=HTMLResponse)
async def ssl_checker(domain: str = Form(default="")):
    cert_info, error = None, None
    clean_dom = clean_domain_name(domain)

    if clean_dom:
        try:
            context = ssl.create_default_context()
            with socket.create_connection((clean_dom, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=clean_dom) as ssock:
                    cert = ssock.getpeercert()
                    
                    # استخراج تاريخ الانتهاء والجهة المصدرة
                    not_after = cert.get('notAfter')
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    issuer_name = issuer.get('organizationName', 'Unknown')
                    
                    expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                    days_left = (expiry_date - datetime.utcnow()).days
                    
                    cert_info = {
                        "issuer": issuer_name,
                        "expiry": expiry_date.strftime('%Y-%m-%d'),
                        "days_left": days_left,
                        "status": "Valid" if days_left > 0 else "Expired"
                    }
        except Exception as e:
            error = f"Unable to verify SSL certificate for '{clean_dom}'. Make sure HTTPS is enabled and port 443 is open."

    res_box = ""
    if cert_info:
        status_color = "#10b981" if cert_info["days_left"] > 15 else "#f59e0b"
        res_box = f'''
        <div class="res-box" style="border-color: {status_color};">
            <h3 style="margin:0 0 10px 0; color: {status_color};">🔒 SSL Certificate Details:</h3>
            <p style="margin: 5px 0;"><strong>Status:</strong> {cert_info["status"]}</p>
            <p style="margin: 5px 0;"><strong>Issuer:</strong> {cert_info["issuer"]}</p>
            <p style="margin: 5px 0;"><strong>Expiration Date:</strong> {cert_info["expiry"]}</p>
            <p style="margin: 5px 0;"><strong>Days Remaining:</strong> {cert_info["days_left"]} days</p>
        </div>'''
    elif error and clean_dom:
        res_box = f'<div class="err-box">⚠️ {error}</div>'

    head = build_head_tags(
        title="Free SSL Certificate Checker | BlacklistMail",
        description="Verify SSL/TLS certificate validity, expiration dates, and issuer security for any domain.",
        canonical_url="https://blacklistmail.com/ssl-checker"
    )

    html = f'''<!DOCTYPE html><html lang="en">{head}
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>🔐 Free SSL Certificate Checker</h1><p>Inspect SSL/TLS security certificate health and expiry dates in real time.</p>
    <form method="POST" action="/ssl-checker">
        <input type="text" name="domain" placeholder="example.com" value="{clean_dom}" required><br>
        <button type="submit">Check SSL</button>
    </form>
    {res_box}{MONETIZATION_HTML}
    </div></body></html>'''
    
    return HTMLResponse(content=html)


# ==========================================
# 2. أداة تحليل السبام والأمان (Spam Analyzer)
# ==========================================
@router.get("/spam-analyzer", response_class=HTMLResponse)
@router.post("/spam-analyzer", response_class=HTMLResponse)
async def spam_analyzer(content: str = Form(default="")):
    spam_score = 0
    flags = []
    text_content = content.strip().lower()

    if text_content:
        # كلمات واختبارات شائعة تعزز فرص التصنيف كسبام
        spam_keywords = [
            "buy now", "free money", "100% free", "click here", "guaranteed", 
            "earn $", "no credit card", "act now", "urgent response required",
            "congratulations", "winner"
        ]
        
        for word in spam_keywords:
            if word in text_content:
                spam_score += 15
                flags.append(f"Contains high-risk trigger phrase: '{word}'")
                
        if "http://" in text_content:
            spam_score += 20
            flags.append("Contains non-secure HTTP links")
            
        if text_content.isupper() and len(text_content) > 20:
            spam_score += 25
            flags.append("Excessive use of ALL CAPS text")

        spam_score = min(spam_score, 100)

    res_box = ""
    if text_content:
        score_color = "#10b981" if spam_score < 30 else ("#f59e0b" if spam_score < 60 else "#ef4444")
        flags_html = "".join([f"<li>⚠️ {flag}</li>" for flag in flags]) if flags else "<li>✅ No major spam trigger phrases detected.</li>"
        
        res_box = f'''
        <div class="res-box" style="border-color: {score_color};">
            <h3 style="margin:0 0 10px 0; color: {score_color};">📊 Spam Score Assessment: {spam_score}/100</h3>
            <ul style="margin: 5px 0; padding-left: 20px; line-height: 1.6;">
                {flags_html}
            </ul>
        </div>'''

    head = build_head_tags(
        title="Free Email Spam Analyzer | BlacklistMail",
        description="Analyze your email content and subject line for spam triggers before sending.",
        canonical_url="https://blacklistmail.com/spam-analyzer"
    )

    html = f'''<!DOCTYPE html><html lang="en">{head}
    <body><div class="container"><p><a href="/">&larr; Back to Dashboard</a></p>
    <h1>🛡️ Free Email Spam Analyzer</h1><p>Test email text and subject lines for high-risk spam keywords and elements.</p>
    <form method="POST" action="/spam-analyzer">
        <label>Email Body Content or Subject Line:</label><br>
        <textarea name="content" rows="6" placeholder="Paste your email copy here..." required>{content}</textarea><br>
        <button type="submit">Analyze Content</button>
    </form>
    {res_box}{MONETIZATION_HTML}
    </div></body></html>'''
    
    return HTMLResponse(content=html)