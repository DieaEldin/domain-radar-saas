# utils.py

COMMON_CSS = """
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
.container { max-width: 850px; margin: 30px auto; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid #334155; }
h1 { color: #fff; font-size: 26px; margin-bottom: 10px; }
p { color: #94a3b8; line-height: 1.6; }
input[type="text"], textarea, select { padding: 12px 15px; width: 95%; border: 1px solid #475569; border-radius: 6px; font-size: 15px; background: #0f172a; color: #fff; margin-bottom: 15px; }
button { padding: 12px 22px; background: #38bdf8; color: #0f172a; border: none; border-radius: 6px; font-size: 15px; cursor: pointer; font-weight: bold; }
button:hover { background: #0284c7; color: #fff; }
a { color: #38bdf8; text-decoration: none; }
.res-box { background: #064e3b; border: 1px solid #10b981; padding: 15px; border-radius: 6px; margin-top: 20px; color: #ecfdf5; }
.err-box { background: #7f1d1d; border: 1px solid #ef4444; padding: 15px; border-radius: 6px; margin-top: 20px; color: #fef2f2; }
code { background: #0f172a; padding: 12px; display: block; border-radius: 6px; font-weight: bold; word-break: break-all; margin-top: 8px; color: #38bdf8; border: 1px solid #334155; }
"""

MONETIZATION_HTML = """
<div class="affiliate-section">
    <h3 style="margin:0; text-align:center; color:#f8fafc;">⚡ Need Professional & Secure Email Hosting?</h3>
    <div class="affiliate-grid">
        <div class="aff-card">
            <h3>Hostinger Business Email</h3>
            <a href="https://hostinger.com/?referral=blacklistmail" target="_blank" class="aff-btn">Get Hostinger (75% Off) &rarr;</a>
        </div>
        <div class="aff-card">
            <h3>Google Workspace</h3>
            <a href="https://workspace.google.com/intl/en/landing/signup/referral/" target="_blank" class="aff-btn google">Get Google Workspace &rarr;</a>
        </div>
    </div>
</div>
"""

def clean_domain_name(domain: str) -> str:
    return domain.strip().lower().replace("http://", "").replace("https://", "").split("/")[0]

def build_head_tags(title: str, description: str, canonical_url: str) -> str:
    return f"""
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <style>{COMMON_CSS}</style>
</head>
"""