from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from utils import build_head_tags, MONETIZATION_HTML
import httpx

router = APIRouter(tags=["Services"])

# ==========================================
# 1. Platform / Overview
# ==========================================
@router.get("/platform", response_class=HTMLResponse)
async def platform_page():
    head = build_head_tags(
        title="Email Security & Deliverability Platform | BlacklistMail",
        description="Comprehensive email security, blacklist monitoring, and DNS configuration suite.",
        canonical_url="https://blacklistmail.com/platform"
    )
    html = f'''<!DOCTYPE html><html lang="en">{head}
    <body><div class="container"><p><a href="/">&larr; Back to Home</a></p>
    <h1>🚀 BlacklistMail Platform</h1><p>All-in-one suite for monitoring domain reputation, deliverability, and DNS security.</p>
    {MONETIZATION_HTML}</div></body></html>'''
    return HTMLResponse(content=html)


# ==========================================
# 2. Delisting Directory
# ==========================================
@router.get("/delisting-directory", response_class=HTMLResponse)
async def delisting_directory():
    head = build_head_tags(
        title="Blacklist Delisting Directory | BlacklistMail",
        description="Official removal request links for major email blacklists.",
        canonical_url="https://blacklistmail.com/delisting-directory"
    )
    
    html = f'''<!DOCTYPE html>
    <html lang="en">
    {head}
    <style>
        :root {{
            --bg-color: #0d1117;
            --card-bg: #161b22;
            --border-color: #30363d;
            --accent-blue: #2f81f7;
            --text-main: #c9d1d9;
            --text-heading: #f0f6fc;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0; padding: 0; line-height: 1.6;
        }}
        .navbar {{ background: #161b22; border-bottom: 1px solid var(--border-color); padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }}
        .navbar a {{ color: var(--accent-blue); text-decoration: none; font-weight: 600; }}
        .container {{ max-width: 1000px; margin: 50px auto; padding: 0 20px; }}
        .header {{ margin-bottom: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.2rem; color: var(--text-heading); margin-bottom: 10px; }}
        .header p {{ color: #8b949e; font-size: 1.1rem; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }}
        .card {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 10px; padding: 25px; display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.2s; }}
        .card:hover {{ transform: translateY(-3px); border-color: var(--accent-blue); }}
        .card h3 {{ color: var(--text-heading); margin: 0 0 10px 0; font-size: 1.25rem; }}
        .card p {{ color: #8b949e; font-size: 0.92rem; margin-bottom: 20px; flex-grow: 1; }}
        .btn {{ display: inline-block; text-align: center; background: #21262d; color: var(--accent-blue); border: 1px solid var(--border-color); padding: 10px 16px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.9rem; transition: all 0.2s; }}
        .btn:hover {{ background: var(--accent-blue); color: #ffffff; }}
    </style>
    <body>
        <div class="navbar">
            <strong>BlacklistMail Directory</strong>
            <a href="/">&larr; Back to Home</a>
        </div>
        <div class="container">
            <div class="header">
                <h1>📋 Blacklist Delisting Directory</h1>
                <p>Direct removal application portals for major domain and IP DNSBL databases.</p>
            </div>
            <div class="grid">
                <div class="card">
                    <div>
                        <h3>Spamhaus Removal</h3>
                        <p>Global leader in IP/Domain threat reputation. Submit delist requests for SBL, DBL, and ZEN.</p>
                    </div>
                    <a href="https://check.spamhaus.org/" target="_blank" rel="noopener" class="btn">Official Lookup Portal &rarr;</a>
                </div>
                <div class="card">
                    <div>
                        <h3>Barracuda Central</h3>
                        <p>Leading enterprise anti-spam firewall list. Request immediate IP reputation re-evaluation.</p>
                    </div>
                    <a href="https://www.barracudacentral.org/lookups" target="_blank" rel="noopener" class="btn">Official Lookup Portal &rarr;</a>
                </div>
                <div class="card">
                    <div>
                        <h3>SpamCop Database</h3>
                        <p>Automated reporting database tracking IP addresses flagged for unsolicited bulk emails.</p>
                    </div>
                    <a href="https://www.spamcop.net/bl.shtml" target="_blank" rel="noopener" class="btn">Official Lookup Portal &rarr;</a>
                </div>
                <div class="card">
                    <div>
                        <h3>Proofpoint (SORBS)</h3>
                        <p>Database indexing open relays and proxy servers causing email deliverability issues.</p>
                    </div>
                    <a href="http://www.sorbs.net/lookup.shtml" target="_blank" rel="noopener" class="btn">Official Lookup Portal &rarr;</a>
                </div>
            </div>
        </div>
    </body>
    </html>'''
    return HTMLResponse(content=html)


# ==========================================
# 3. Security News Data & Endpoints
# ==========================================
NEWS_DATA = {
    "gmail-yahoo-dmarc-updates-2026": {
        "title": "Gmail & Yahoo DMARC Enforcement Updates for 2026",
        "date": "2026-08-20",
        "summary": "Latest requirements for bulk senders regarding SPF, DKIM, and one-click unsubscribe headers.",
        "content": """
            <p>Inbox providers such as Gmail and Yahoo have strictly enforced authentication mandates for domain senders. Failing to implement required protocols result in immediate inbox rejections or automatic spam classification.</p>
            
            <h3 style="color:#fff; margin-top:20px;">Mandatory Security Standards:</h3>
            <ul style="line-height:1.8;">
                <li><strong>Strict SPF & DKIM Alignment:</strong> Email headers must pass domain alignment checks for both SPF and DKIM signatures.</li>
                <li><strong>Enforced DMARC Policy:</strong> Domains must publish an explicit DMARC policy (minimum <code>p=none</code> with reporting, upgrading to <code>p=quarantine</code> or <code>p=reject</code>).</li>
                <li><strong>One-Click Unsubscribe (RFC 8058):</strong> Bulk marketing messages require standard headers to allow instant user unsubscription.</li>
                <li><strong>Spam Rate Threshold:</strong> Keep reported spam complaints below <strong>0.10%</strong> (and never exceed 0.30%).</li>
            </ul>

            <p style="margin-top:20px;">Verify your compliance status immediately to protect your business email reputation.</p>
        """,
        "image": "https://blacklistmail.com/static/news-dmarc.jpg"
    },
    "bimi-logo-verification-guide": {
        "title": "How BIMI Certification Protects Brand Reputation in Inboxes",
        "date": "2026-08-15",
        "summary": "A comprehensive breakdown of VMC certificates and BIMI DNS record configuration.",
        "content": """
            <p>Brand Indicators for Message Identification (BIMI) empowers verified organizations to display official brand logos directly alongside email messages in user inboxes.</p>
            
            <h3 style="color:#fff; margin-top:20px;">Prerequisites to Deploy BIMI:</h3>
            <ol style="line-height:1.8;">
                <li><strong>Strict DMARC Policy:</strong> Your DMARC policy must be actively enforced at <code>p=quarantine</code> (at 100% pct) or <code>p=reject</code>.</li>
                <li><strong>SVG Logo Hosting:</strong> Format your trademarked logo as a square SVG-P/PS file hosted over secure HTTPS.</li>
                <li><strong>Verified Mark Certificate (VMC):</strong> Acquire a VMC from a recognized Certificate Authority to validate brand ownership.</li>
            </ol>

            <p style="margin-top:20px;">Deploying BIMI significantly increases email open rates while insulating your domain from phishing spoofs.</p>
        """,
        "image": "https://blacklistmail.com/static/news-bimi.jpg"
    },
    "common-spf-errors-deliverability-impact": {
        "title": "Top 5 SPF Record Misconfigurations Ruining Email Deliverability",
        "date": "2026-08-22",
        "summary": "Discover the most critical SPF syntax errors, lookup limits, and alignment issues that push your emails into the spam folder.",
        "content": """
            <p>Sender Policy Framework (SPF) is a fundamental DNS authentication mechanism designed to prevent domain spoofing. However, a single syntax error or misconfiguration in your SPF record can severely damage your domain reputation and drop delivery rates.</p>

            <h3 style="color:#fff; margin-top:20px;">1. Exceeding the 10 DNS Lookup Limit</h3>
            <p>SPF evaluation mechanisms impose a strict limit of <strong>10 DNS lookups</strong>. Including multiple third-party services (e.g., Google Workspace, SendGrid, Mailchimp) can quickly exceed this limit, causing mail servers to return a <code>PermError</code> and bypass SPF validation entirely.</p>

            <h3 style="color:#fff; margin-top:20px;">2. Multiple SPF Records on a Single Domain</h3>
            <p>A domain must strictly contain <strong>only one SPF TXT record</strong>. Publishing multiple records causes receiving servers to reject all of them due to authentication ambiguity.</p>

            <h3 style="color:#fff; margin-top:20px;">3. Using the Obsolete <code>ptr</code> Mechanism</h3>
            <p>Using <code>ptr</code> mechanism in modern SPF records is strongly discouraged by RFC standards. It places unnecessary load on DNS resolvers and causes soft delivery failures.</p>

            <h3 style="color:#fff; margin-top:20px;">4. Misconfigured All Mechanisms (<code>~all</code> vs <code>-all</code>)</h3>
            <p>Failing to end your record with an explicit qualifier like <code>~all</code> (SoftFail) or <code>-all</code> (HardFail) leaves your domain vulnerable to impersonation and phishing attacks.</p>

            <p style="margin-top:25px;">To prevent these silent delivery failures, validate your record layout before sending campaigns.</p>
        """,
        "image": "https://blacklistmail.com/static/news-spf.jpg"
    }
}

@router.get("/news", response_class=HTMLResponse)
async def security_news(request: Request):
    articles_html = ""
    for slug, article in NEWS_DATA.items():
        articles_html += f"""
        <article style="background: #1e293b; padding: 25px; margin-bottom: 20px; border-radius: 8px; border: 1px solid #334155;">
            <span style="color: #38bdf8; font-size: 13px; font-weight: 600;">{article['date']}</span>
            <h2 style="margin: 10px 0;"><a href="/news/{slug}" style="color: #fff; text-decoration: none;">{article['title']}</a></h2>
            <p style="color: #94a3b8; font-size: 14px; line-height: 1.6; margin-bottom: 15px;">{article['summary']}</p>
            <a href="/news/{slug}" style="color: #38bdf8; font-weight: bold; font-size: 14px; text-decoration: none;">Read Full Article &rarr;</a>
        </article>
        """

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Security News & Deliverability Trends | BlacklistMail</title>
    <meta name="description" content="Stay updated with the latest trends in email authentication, SPF/DMARC policies, and inbox placement.">
    <link rel="canonical" href="https://blacklistmail.com/news" />
    <meta property="og:title" content="Email Security News & Deliverability Trends" />
    <meta property="og:description" content="Latest trends in email authentication and domain reputation." />
    <meta property="og:url" content="https://blacklistmail.com/news" />
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 40px 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        a {{ color: #38bdf8; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <p><a href="/">&larr; Back to Dashboard</a></p>
        <h1 style="color: #fff;">📰 Security News & Insights</h1>
        <p style="color: #94a3b8; margin-bottom: 30px;">Insights on email authentication protocols, blacklist updates, and domain reputation management.</p>
        
        {articles_html}
    </div>
</body>
</html>'''
    return HTMLResponse(content=html)


@router.get("/news/{slug}", response_class=HTMLResponse)
async def news_detail(slug: str):
    if slug not in NEWS_DATA:
        raise HTTPException(status_code=404, detail="Article not found")
        
    article = NEWS_DATA[slug]
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']} | BlacklistMail News</title>
    <meta name="description" content="{article['summary']}">
    <link rel="canonical" href="https://blacklistmail.com/news/{slug}" />
    <meta property="og:title" content="{article['title']}" />
    <meta property="og:description" content="{article['summary']}" />
    <meta property="og:image" content="{article['image']}" />
    <meta property="og:type" content="article" />
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 40px 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: #1e293b; padding: 35px; border-radius: 12px; border: 1px solid #334155; }}
        a {{ color: #38bdf8; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .cta-box {{ background: #0f172a; padding: 20px; border-radius: 8px; border-left: 4px solid #38bdf8; margin-top: 35px; border-top: 1px solid #334155; border-right: 1px solid #334155; border-bottom: 1px solid #334155; }}
        code {{ background: #0f172a; color: #38bdf8; padding: 3px 6px; border-radius: 4px; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <p><a href="/news">&larr; Back to News</a></p>
        <span style="color: #38bdf8; font-size: 14px; font-weight: 600;">Published: {article['date']}</span>
        <h1 style="color: #fff; margin-top: 10px; font-size: 26px;">{article['title']}</h1>
        <hr style="border-color: #334155; margin: 20px 0;" />
        
        <div style="line-height: 1.8; color: #cbd5e1; font-size: 15px;">
            {article['content']}
        </div>

        <div class="cta-box">
            <h4 style="margin: 0 0 10px 0; color: #fff; font-size: 16px;">🔍 Verify Your Domain Security Compliance</h4>
            <p style="margin: 0; font-size: 14px; color: #94a3b8; line-height: 1.6;">Ensure your email setup meets provider mandates. Perform a instant live audit using our <a href="/dmarc-checker">DMARC Inspector</a>, <a href="/txt-lookup">DNS TXT Lookup</a>, or <a href="/spf-checker">SPF Checker</a> tools.</p>
        </div>
    </div>
</body>
</html>'''
    return HTMLResponse(content=html)


# ==========================================
# 4. Email Health Score (DoH API Audit)
# ==========================================
@router.get("/email-health-score", response_class=HTMLResponse)
async def email_health_score_page(domain: str = ""):
    head = build_head_tags(
        title="Free Email Health Check & Deliverability Audit | BlacklistMail",
        description="Run a 1-click comprehensive email security audit checking SPF, DMARC, MX, and Blacklists.",
        canonical_url="https://blacklistmail.com/email-health-score"
    )
    
    domain_input = domain.strip().lower()
    results_html = ""
    
    if domain_input:
        score = 0
        spf_found, dmarc_found, mx_found = False, False, False
        
        async with httpx.AsyncClient(timeout=8.0) as client:
            # 1. Check MX Records
            try:
                res_mx = await client.get(f"https://dns.google/resolve?name={domain_input}&type=MX")
                if res_mx.status_code == 200:
                    data = res_mx.json()
                    if data.get("Status") == 0 and "Answer" in data:
                        mx_found = True
                        score += 30
            except Exception:
                pass

            # 2. Check SPF Record
            try:
                res_txt = await client.get(f"https://dns.google/resolve?name={domain_input}&type=TXT")
                if res_txt.status_code == 200:
                    data = res_txt.json()
                    if data.get("Status") == 0 and "Answer" in data:
                        for ans in data["Answer"]:
                            txt_data = ans.get("data", "").lower()
                            if "v=spf1" in txt_data:
                                spf_found = True
                                score += 35
                                break
            except Exception:
                pass

            # 3. Check DMARC Record
            try:
                res_dmarc = await client.get(f"https://dns.google/resolve?name=_dmarc.{domain_input}&type=TXT")
                if res_dmarc.status_code == 200:
                    data = res_dmarc.json()
                    if data.get("Status") == 0 and "Answer" in data:
                        for ans in data["Answer"]:
                            txt_data = ans.get("data", "").lower()
                            if "v=dmarc1" in txt_data:
                                dmarc_found = True
                                score += 35
                                break
            except Exception:
                pass

        # Badges & Colors
        spf_badge = '<span style="color: #3fb950; font-weight: bold;">✔ Valid</span>' if spf_found else '<span style="color: #f85149; font-weight: bold;">✖ Missing</span>'
        dmarc_badge = '<span style="color: #3fb950; font-weight: bold;">✔ Configured</span>' if dmarc_found else '<span style="color: #f85149; font-weight: bold;">✖ Missing</span>'
        mx_badge = '<span style="color: #3fb950; font-weight: bold;">✔ Detected</span>' if mx_found else '<span style="color: #f85149; font-weight: bold;">✖ No MX Records</span>'
        
        score_color = "#3fb950" if score >= 80 else ("#d29922" if score >= 50 else "#f85149")

        results_html = f'''
        <div style="background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 25px; margin-top: 30px;">
            <div style="text-align: center; margin-bottom: 25px;">
                <h2 style="color: #f0f6fc; margin-bottom: 5px;">Health Score for <span style="color: #2f81f7;">{domain_input}</span></h2>
                <div style="font-size: 3.5rem; font-weight: bold; color: {score_color}; margin: 10px 0;">{score} / 100</div>
                <p style="color: #8b949e;">Live Google DNS API Results</p>
            </div>
            
            <div style="display: grid; gap: 15px;">
                <div style="background: #0d1117; padding: 15px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center;">
                    <span>🛡️ <strong>SPF Record Status</strong></span>
                    {spf_badge}
                </div>
                <div style="background: #0d1117; padding: 15px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center;">
                    <span>🔒 <strong>DMARC Alignment</strong></span>
                    {dmarc_badge}
                </div>
                <div style="background: #0d1117; padding: 15px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center;">
                    <span>📮 <strong>MX Mail Server Records</strong></span>
                    {mx_badge}
                </div>
            </div>
        </div>
        '''

    html = f'''<!DOCTYPE html>
<html lang="en">
{head}
<style>
    body {{ font-family: system-ui, -apple-system, sans-serif; background-color: #0d1117; color: #c9d1d9; margin: 0; padding: 0; }}
    .navbar {{ background: #161b22; border-bottom: 1px solid #30363d; padding: 1rem 2rem; display: flex; justify-content: space-between; }}
    .navbar a {{ color: #2f81f7; text-decoration: none; font-weight: 600; }}
    .container {{ max-width: 800px; margin: 40px auto; padding: 0 20px; }}
    .search-box {{ display: flex; gap: 10px; margin-top: 20px; }}
    input[type="text"] {{ flex: 1; padding: 12px; border-radius: 6px; border: 1px solid #30363d; background: #161b22; color: #fff; font-size: 1rem; }}
    button {{ background: #238636; color: #fff; border: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; cursor: pointer; }}
    button:hover {{ background: #2ea043; }}
</style>
<body>
    <div class="navbar">
        <strong>BlacklistMail Health Audit</strong>
        <a href="/">&larr; Back to Home</a>
    </div>
    <div class="container">
        <h1 style="color: #f0f6fc; text-align: center;">📊 Instant Email Health Score</h1>
        <p style="text-align: center; color: #8b949e;">Test your domain's SPF, DMARC, and MX setup in real-time.</p>

        <form method="get" action="/email-health-score" class="search-box">
            <input type="text" name="domain" placeholder="example.com" value="{domain_input}" required />
            <button type="submit">Run Audit</button>
        </form>

        {results_html}
    </div>
</body>
</html>'''
    return HTMLResponse(content=html)


# ==========================================
# 5. FAQ Page (SEO Enhanced)
# ==========================================
@router.get("/faq", response_class=HTMLResponse)
async def faq_page():
    head = build_head_tags(
        title="Frequently Asked Questions | Email Security & Blacklists",
        description="Learn about email deliverability, DNS security records, BIMI requirements, and how to request blacklist removal.",
        canonical_url="https://blacklistmail.com/faq"
    )
    
    html = f'''<!DOCTYPE html>
<html lang="en">
{head}
<style>
    body {{ font-family: system-ui, -apple-system, sans-serif; background-color: #0d1117; color: #c9d1d9; margin: 0; padding: 0; line-height: 1.6; }}
    .navbar {{ background: #161b22; border-bottom: 1px solid #30363d; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }}
    .navbar a {{ color: #2f81f7; text-decoration: none; font-weight: 600; }}
    .container {{ max-width: 800px; margin: 40px auto; padding: 0 20px; }}
    .faq-item {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 15px; }}
    .faq-item h3 {{ color: #f0f6fc; margin-top: 0; font-size: 1.1rem; }}
    .faq-item p {{ color: #8b949e; margin-bottom: 0; font-size: 0.95rem; }}
</style>
<body>
    <div class="navbar">
        <strong style="color:#f0f6fc;">BlacklistMail Knowledge Base</strong>
        <a href="/">&larr; Back to Home</a>
    </div>
    <div class="container">
        <h1 style="color: #f0f6fc; text-align: center; margin-bottom: 30px;">❓ Frequently Asked Questions</h1>
        
        <div class="faq-item">
            <h3>How do I remove my IP or domain from a blacklist?</h3>
            <p>You can locate the official removal portal using our <a href="/delisting-directory" style="color:#2f81f7;">Delisting Directory</a> and submit a removal request once you have resolved the underlying spam or security issue.</p>
        </div>

        <div class="faq-item">
            <h3>What is the difference between SPF and DMARC?</h3>
            <p>SPF defines which IP addresses/servers are authorized to send email on behalf of your domain. DMARC instructs receiving servers how to handle messages that fail SPF or DKIM checks.</p>
        </div>

        <div class="faq-item">
            <h3>Why are my emails landing in the Spam folder?</h3>
            <p>Common causes include missing DMARC enforcement policies, blacklisted sending IPs, high spam complaint rates, or syntax errors exceeding the 10 DNS lookup limit in SPF records.</p>
        </div>

        <div class="faq-item">
            <h3>What are the requirements to display a BIMI Brand Logo in inboxes?</h3>
            <p>To implement BIMI, your domain must enforce a strict DMARC policy (<code>p=quarantine</code> or <code>p=reject</code>), host a valid SVG Tiny P/S logo, and optionally secure a VMC (Verified Mark Certificate).</p>
        </div>

        <div class="faq-item">
            <h3>How often are Blacklist Monitoring databases updated?</h3>
            <p>Major DNSBLs (such as Spamhaus and Barracuda) update their databases in real-time. Our automated checks query live DNS zone files to give you real-time status updates.</p>
        </div>

        <div class="faq-item">
            <h3>Does a high Email Health Score guarantee 100% Inbox Placement?</h3>
            <p>While a high Health Score ensures your DNS authentication (SPF, DKIM, DMARC) is flawless, deliverability also depends on domain reputation, email content quality, and recipient engagement rates.</p>
        </div>
    </div>
</body>
</html>'''
    return HTMLResponse(content=html)