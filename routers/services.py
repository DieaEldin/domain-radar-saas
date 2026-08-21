from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from utils import build_head_tags, MONETIZATION_HTML

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
    }
}

# 1. الصفحة الرئيسية للأخبار (/news)
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


# 2. صفحة الخبر المنفصل (/news/{slug})
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

        <!-- Internal Linking Box -->
        <div class="cta-box">
            <h4 style="margin: 0 0 10px 0; color: #fff; font-size: 16px;">🔍 Verify Your Domain Security Compliance</h4>
            <p style="margin: 0; font-size: 14px; color: #94a3b8; line-height: 1.6;">Ensure your email setup meets provider mandates. Perform a instant live audit using our <a href="/dmarc-checker">DMARC Inspector</a>, <a href="/txt-lookup">DNS TXT Lookup</a>, or <a href="/spf-checker">SPF Checker</a> tools.</p>
        </div>
    </div>
</body>
</html>'''
    return HTMLResponse(content=html)