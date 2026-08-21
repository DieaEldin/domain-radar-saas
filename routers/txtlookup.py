# --- TXT Lookup Tool ---
@app.get("/txt-lookup", response_class=HTMLResponse)
def txt_lookup_page():
    head = build_head_tags(
        title="Free DNS TXT Record Lookup Tool | BlacklistMail",
        description="Instantly query and analyze DNS TXT records for any domain to inspect SPF, DMARC, site verification, and security policies.",
        canonical_url="https://blacklistmail.com/txt-lookup"
    )

    html = f'''<!DOCTYPE html><html lang="en">{head}
    <body>
        <div class="container">
            <p><a href="/">&larr; Back to Dashboard</a></p>
            <h1>🔎 Free DNS TXT Record Lookup</h1>
            <p>Inspect all active TXT records published on your domain for SPF, DMARC, DKIM, and Domain Verification.</p>
            
            <form action="/txt-lookup" method="get" style="margin-top:20px;">
                <input type="text" name="domain" placeholder="Enter domain name (e.g. workplaceemail.com)" required />
                <button type="submit">Lookup TXT Records</button>
            </form>

            {MONETIZATION_HTML}
        </div>
    </body>
    </html>'''
    return HTMLResponse(content=html)