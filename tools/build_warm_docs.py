# -*- coding: utf-8 -*-
"""
Rebuilds docs/index.html with the Warm Terracotta, Espresso Obsidian,
and Warm Linen editorial design system.
Replaces the clunky pitch-dark template with a Stripe/Mintlify-caliber documentation studio.
"""

# Read existing docs/index.html to extract the ENDPOINTS array exactly
with open("/tmp/beyond-likes-git/docs/index.html", "r", encoding="utf-8") as f:
    orig = f.read()

# Extract endpoints array from orig
start_marker = "const ENDPOINTS = ["
end_marker = "];\n\n    function renderNav()"
if end_marker not in orig:
    end_marker = "];\n\n    // Render Nav"
if end_marker not in orig:
    # Find the end of array
    idx_start = orig.find(start_marker)
    idx_end = orig.find("];", idx_start)
    endpoints_str = orig[idx_start + len(start_marker) - 1: idx_end + 1]
else:
    idx_start = orig.find(start_marker)
    idx_end = orig.find(end_marker)
    endpoints_str = orig[idx_start + len(start_marker) - 1: idx_end + 1]

NEW_DOCS_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Normative Intelligence API Reference &amp; Interactive Studio</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #faf8f5;
      --sidebar-bg: #ffffff;
      --card-bg: #ffffff;
      --card-border: #e8e3d8;
      --border-subtle: #f4f0e8;

      --text: #18181b;
      --text-muted: #52525b;
      --text-subtle: #71717a;

      --accent: #c8441b;
      --accent-hover: #b13712;
      --accent-subtle: #fdf2ee;
      --accent-border: #f8c9bc;

      --juniper: #0d5c4e;
      --juniper-subtle: #edf7f4;
      --juniper-border: #bce3db;

      --amber: #b45309;
      --amber-subtle: #fffbeb;
      --amber-border: #fde68a;

      --rose: #be123c;
      --rose-subtle: #fff1f2;
      --rose-border: #fecdd3;

      --code-bg: #18181b;
      --code-text: #f4f4f5;

      --method-post: #c8441b;
      --method-get: #0d5c4e;
      --method-delete: #be123c;
      --border-focus: #c8441b;

      --shadow-sm: 0 1px 3px rgba(39, 30, 20, 0.05);
      --shadow-md: 0 4px 14px -2px rgba(39, 30, 20, 0.08);
      --shadow-lg: 0 12px 28px -6px rgba(39, 30, 20, 0.09);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      display: flex;
      min-height: 100vh;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }}

    /* Sidebar Navigation */
    #sidebar {{
      width: 320px;
      background: var(--sidebar-bg);
      border-right: 1px solid var(--card-border);
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
      padding: 24px 20px;
      flex-shrink: 0;
      display: flex;
      flex-direction: column;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 22px;
      padding-bottom: 18px;
      border-bottom: 1px solid var(--card-border);
      text-decoration: none;
      color: var(--text);
    }}

    .brand-title {{
      font-size: 1.05rem;
      font-weight: 800;
      letter-spacing: -0.02em;
    }}
    .brand-title span {{ color: var(--accent); }}

    .brand-version {{
      font-size: 0.7rem;
      background: var(--accent-subtle);
      border: 1px solid var(--accent-border);
      color: var(--accent);
      padding: 2px 7px;
      border-radius: 4px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      margin-left: 6px;
    }}

    .search-box {{
      margin-bottom: 22px;
    }}
    .search-input {{
      width: 100%;
      background: var(--bg);
      border: 1px solid var(--card-border);
      color: var(--text);
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 0.86rem;
      font-family: inherit;
      outline: none;
      transition: all 0.15s;
    }}
    .search-input:focus {{
      border-color: var(--accent);
      background: #ffffff;
      box-shadow: 0 0 0 3px rgba(200, 68, 27, 0.12);
    }}

    .nav-group-title {{
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-subtle);
      font-weight: 800;
      margin: 20px 0 8px 6px;
    }}

    .nav-item {{
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 10px;
      border-radius: 6px;
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.84rem;
      font-weight: 600;
      margin-bottom: 2px;
      transition: all 0.15s;
    }}
    .nav-item:hover {{
      background: var(--accent-subtle);
      color: var(--accent);
    }}
    .nav-item.active {{
      background: var(--accent-subtle);
      color: var(--accent);
      font-weight: 700;
    }}

    .badge-method {{
      font-size: 0.65rem;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: 0.04em;
    }}
    .badge-post {{
      background: var(--accent-subtle);
      color: var(--accent);
      border: 1px solid var(--accent-border);
    }}
    .badge-get {{
      background: var(--juniper-subtle);
      color: var(--juniper);
      border: 1px solid var(--juniper-border);
    }}
    .badge-delete {{
      background: var(--rose-subtle);
      color: var(--rose);
      border: 1px solid var(--rose-border);
    }}

    .sidebar-footer {{
      margin-top: auto;
      padding-top: 18px;
      border-top: 1px solid var(--card-border);
      font-size: 0.78rem;
      color: var(--text-subtle);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .sidebar-footer a {{
      color: var(--accent);
      text-decoration: none;
      font-weight: 600;
    }}
    .sidebar-footer a:hover {{ text-decoration: underline; }}

    /* Main Content Area */
    #content {{
      flex: 1;
      padding: 40px 48px;
      max-width: 1140px;
      overflow-y: auto;
    }}

    .top-banner {{
      background: #ffffff;
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 26px 30px;
      margin-bottom: 36px;
      box-shadow: var(--shadow-sm);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 20px;
      flex-wrap: wrap;
    }}
    .banner-title {{
      font-size: 1.35rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--text);
      margin-bottom: 6px;
    }}
    .banner-desc {{
      font-size: 0.94rem;
      color: var(--text-muted);
      line-height: 1.6;
      max-width: 620px;
    }}
    .banner-links {{
      display: flex;
      gap: 10px;
    }}
    .btn-link {{
      background: var(--bg);
      color: var(--text);
      border: 1px solid var(--card-border);
      padding: 9px 16px;
      border-radius: 8px;
      font-size: 0.86rem;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.15s;
    }}
    .btn-link:hover {{
      background: var(--accent-subtle);
      color: var(--accent);
      border-color: var(--accent-border);
    }}

    /* Endpoint Card */
    .endpoint-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      margin-bottom: 40px;
      overflow: hidden;
      box-shadow: var(--shadow-sm);
      transition: box-shadow 0.2s;
    }}
    .endpoint-card:hover {{
      box-shadow: var(--shadow-md);
    }}

    .endpoint-header {{
      padding: 24px 28px;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 16px;
      background: #ffffff;
    }}
    .endpoint-route {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 8px;
    }}
    .endpoint-path {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text);
    }}
    .endpoint-summary {{
      font-size: 1.25rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--text);
      margin-bottom: 6px;
    }}
    .endpoint-desc {{
      font-size: 0.92rem;
      color: var(--text-muted);
      max-width: 760px;
      line-height: 1.6;
    }}

    .badge-perspective {{
      background: var(--juniper-subtle);
      color: var(--juniper);
      border: 1px solid var(--juniper-border);
      font-size: 0.72rem;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 5px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      white-space: nowrap;
    }}

    /* Interactive Live Studio Split */
    .endpoint-body {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      border-bottom: 1px solid var(--card-border);
    }}
    @media (max-width: 900px) {{
      .endpoint-body {{ grid-template-columns: 1fr; }}
    }}

    .panel-req {{
      padding: 24px;
      border-right: 1px solid var(--card-border);
      background: #ffffff;
    }}
    .panel-res {{
      padding: 24px;
      background: #fdfcf9;
    }}

    .panel-title {{
      font-size: 0.76rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-subtle);
      font-weight: 800;
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .code-editor {{
      width: 100%;
      height: 190px;
      background: #1c1917;
      border: 1px solid #383431;
      border-radius: 8px;
      padding: 14px;
      color: #fed7aa;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      outline: none;
      resize: vertical;
      line-height: 1.5;
    }}
    .code-editor:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 2px rgba(200, 68, 27, 0.25);
    }}

    .code-block {{
      background: #1c1917;
      border: 1px solid #383431;
      border-radius: 8px;
      padding: 14px;
      color: #bbf7d0;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      overflow-x: auto;
      max-height: 260px;
      overflow-y: auto;
      line-height: 1.5;
    }}

    .btn-send {{
      background: var(--accent);
      color: #ffffff;
      border: none;
      padding: 10px 20px;
      border-radius: 7px;
      font-weight: 700;
      font-size: 0.88rem;
      cursor: pointer;
      margin-top: 14px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 2px 6px rgba(200, 68, 27, 0.25);
      transition: all 0.15s;
    }}
    .btn-send:hover {{
      background: var(--accent-hover);
      transform: translateY(-1px);
    }}
    .btn-send:disabled {{
      background: #71717a;
      cursor: not-allowed;
      transform: none;
    }}

    .btn-copy {{
      background: #ffffff;
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      font-size: 0.72rem;
      font-weight: 600;
      padding: 3px 9px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .btn-copy:hover {{
      color: var(--accent);
      border-color: var(--accent-border);
      background: var(--accent-subtle);
    }}

    .status-badge {{
      display: inline-block;
      font-size: 0.74rem;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      padding: 2px 8px;
      border-radius: 4px;
    }}
    .status-200 {{
      background: var(--juniper-subtle);
      color: var(--juniper);
      border: 1px solid var(--juniper-border);
    }}
    .status-err {{
      background: var(--rose-subtle);
      color: var(--rose);
      border: 1px solid var(--rose-border);
    }}

    /* Code Snippets Section */
    .endpoint-footer {{
      padding: 18px 24px;
      background: #1c1917;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.82rem;
      color: #d6d3d1;
    }}
    .curl-preview {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: #fed7aa;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      max-width: 760px;
    }}
  </style>
</head>
<body>

  <!-- Left Navigation Sidebar -->
  <aside id="sidebar">
    <a href="/" class="brand">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36" width="30" height="30" fill="none">
        <rect width="36" height="36" rx="8" fill="#18181B"/>
        <path d="M11 25V11L16 22V25H11Z" fill="#C8441B"/>
        <path d="M25 11V25L20 14V11H25Z" fill="#0D5C4E"/>
        <circle cx="18" cy="18" r="2.2" fill="#FAF8F5"/>
      </svg>
      <div>
        <div class="brand-title">Normative<span>.AI</span> <span class="brand-version">v2.8.0</span></div>
        <div style="font-size: 0.74rem; color: var(--text-subtle);">API Studio &amp; Reference</div>
      </div>
    </a>

    <div class="search-box">
      <input type="text" id="searchInput" class="search-input" placeholder="Search endpoints (e.g. analyze, score)..." oninput="filterEndpoints()">
    </div>

    <nav id="navItems" style="flex: 1;">
      <!-- Dynamic Nav Groups populated below -->
    </nav>

    <div class="sidebar-footer">
      <div><strong>OpenAPI Specifications:</strong></div>
      <div style="display: flex; gap: 12px;">
        <a href="/docs/openapi.yaml" download>📄 openapi.yaml</a>
        <a href="/docs/openapi.json" download>📦 openapi.json</a>
      </div>
      <div style="margin-top: 6px; color: var(--text-subtle); font-size: 0.72rem;">
        Autonomous Discourse Infrastructure &bull; 100% Perspective Parity
      </div>
    </div>
  </aside>

  <!-- Main API Reference Content -->
  <main id="content">
    
    <div class="top-banner">
      <div>
        <h1 class="banner-title">Normative Intelligence <em style="font-family: 'Instrument Serif', Georgia, serif; font-style: italic; color: var(--accent); font-weight: normal;">Developer Reference</em> &amp; Interactive Studio</h1>
        <p class="banner-desc">
          Official REST API documentation and live drop-in sandbox for the Google Perspective API sunset cutover. Test requests live against your local engine.
        </p>
      </div>
      <div class="banner-links">
        <a class="btn-link" href="/">Showcase Home</a>
        <a class="btn-link" href="/studio">Workstation Desk</a>
        <a class="btn-link" href="/deck">Pitch Deck</a>
      </div>
    </div>

    <div id="endpointContainer">
      <!-- Dynamic Endpoint Cards populated below -->
    </div>

  </main>

  <script>
    const ENDPOINTS = {endpoints_str};

    function renderNav() {{
      const navContainer = document.getElementById("navItems");
      const groups = {{}};

      ENDPOINTS.forEach((ep) => {{
        if (!groups[ep.category]) groups[ep.category] = [];
        groups[ep.category].push(ep);
      }});

      let html = "";
      for (const [cat, endpoints] of Object.entries(groups)) {{
        html += `<div class="nav-group-title">${{cat}}</div>`;
        endpoints.forEach((ep) => {{
          const methodClass = "badge-" + ep.method.toLowerCase();
          html += `
            <a class="nav-item" href="#${{ep.id}}" id="nav-${{ep.id}}">
              <span class="badge-method ${{methodClass}}">${{ep.method}}</span>
              <span>${{ep.path}}</span>
            </a>
          `;
        }});
      }}
      navContainer.innerHTML = html;
    }}

    function renderCards() {{
      const container = document.getElementById("endpointContainer");
      let html = "";

      ENDPOINTS.forEach((ep) => {{
        const methodClass = "badge-" + ep.method.toLowerCase();
        const hasReqBody = ep.request_body && Object.keys(ep.request_body).length > 0;
        const reqJson = hasReqBody ? JSON.stringify(ep.request_body, null, 2) : "";
        const resJson = JSON.stringify(ep.response_sample, null, 2);

        html += `
          <div class="endpoint-card" id="${{ep.id}}">
            <div class="endpoint-header">
              <div>
                <div class="endpoint-route">
                  <span class="badge-method ${{methodClass}}">${{ep.method}}</span>
                  <span class="endpoint-path">${{ep.path}}</span>
                </div>
                <div class="endpoint-summary">${{ep.summary}}</div>
                <div class="endpoint-desc">${{ep.desc}}</div>
              </div>
              <div>
                <span class="badge-perspective">1:1 PERSPECTIVE PARITY</span>
              </div>
            </div>

            <div class="endpoint-body">
              <div class="panel-req">
                <div class="panel-title">
                  <span>Interactive Request</span>
                  ${{hasReqBody ? `<button class="btn-copy" onclick="copySnippet('req-${{ep.id}}')">Copy JSON</button>` : ""}}
                </div>
                ${{hasReqBody ? `
                  <textarea id="req-${{ep.id}}" class="code-editor">${{reqJson}}</textarea>
                ` : `
                  <div style="color: var(--text-subtle); font-size: 0.85rem; padding: 20px 0;">
                    <em>No request body required for this HTTP ${{ep.method}} endpoint.</em>
                  </div>
                `}}
                <button id="btn-${{ep.id}}" class="btn-send" onclick="sendLiveRequest('${{ep.id}}', '${{ep.method}}', '${{ep.path}}')">
                  ⚡ Send Live Request
                </button>
              </div>

              <div class="panel-res">
                <div class="panel-title">
                  <span>Live Response</span>
                  <div>
                    <span id="status-${{ep.id}}" class="status-badge status-200">200 OK (SAMPLE)</span>
                    <button class="btn-copy" style="margin-left: 6px;" onclick="copySnippet('res-${{ep.id}}')">Copy</button>
                  </div>
                </div>
                <pre class="code-block"><code id="res-${{ep.id}}">${{resJson}}</code></pre>
              </div>
            </div>

            <div class="endpoint-footer">
              <div class="curl-preview">
                <strong>cURL:</strong> curl -X ${{ep.method}} http://localhost:8888${{ep.path}} ${{hasReqBody ? "-H 'Content-Type: application/json' -d '...'" : ""}}
              </div>
            </div>
          </div>
        `;
      }});

      container.innerHTML = html;
    }}

    async function sendLiveRequest(id, method, path) {{
      const btn = document.getElementById("btn-" + id);
      const statusBadge = document.getElementById("status-" + id);
      const resBlock = document.getElementById("res-" + id);
      const reqTextarea = document.getElementById("req-" + id);

      btn.disabled = true;
      btn.innerText = "⏳ Executing...";
      statusBadge.innerText = "Connecting...";

      let headers = {{ 'Accept': 'application/json' }};
      let body = undefined;

      if (reqTextarea && method !== "GET") {{
        try {{
          body = reqTextarea.value.trim();
          headers["Content-Type"] = "application/json";
        }} catch (e) {{
          alert("Invalid JSON format in request body!");
          btn.disabled = false;
          btn.innerText = "⚡ Send Live Request";
          return;
        }}
      }}

      const t0 = performance.now();
      try {{
        const res = await fetch(path, {{ method: method, headers: headers, body: body }});
        const t1 = performance.now();
        const duration = Math.round(t1 - t0);
        
        let data;
        const contentType = res.headers.get("content-type") || "";
        if (contentType.includes("application/json")) {{
          data = await res.json();
          resBlock.innerText = JSON.stringify(data, null, 2);
        }} else {{
          const text = await res.text();
          resBlock.innerText = text.slice(0, 1500) + (text.length > 1500 ? "... [truncated]" : "");
        }}

        statusBadge.innerText = `${{res.status}} ${{res.statusText}} (${{duration}}ms)`;
        statusBadge.className = res.ok ? "status-badge status-200" : "status-badge status-err";
      }} catch (err) {{
        statusBadge.innerText = "Fetch Error";
        statusBadge.className = "status-badge status-err";
        resBlock.innerText = "Network / CORS Error: " + err.message;
      }} finally {{
        btn.disabled = false;
        btn.innerText = "⚡ Send Live Request";
      }}
    }}

    function copySnippet(elementId) {{
      const el = document.getElementById(elementId);
      const text = el.value || el.innerText;
      navigator.clipboard.writeText(text).then(() => {{
        alert("Copied to clipboard!");
      }});
    }}

    function filterEndpoints() {{
      const query = document.getElementById("searchInput").value.toLowerCase();
      ENDPOINTS.forEach((ep) => {{
        const card = document.getElementById(ep.id);
        const navItem = document.getElementById("nav-" + ep.id);
        const match = ep.path.toLowerCase().includes(query) || 
                      ep.summary.toLowerCase().includes(query) || 
                      ep.category.toLowerCase().includes(query);
        if (card) card.style.display = match ? "block" : "none";
        if (navItem) navItem.style.display = match ? "flex" : "none";
      }});
    }}

    // Initialize UI
    renderNav();
    renderCards();
  </script>
</body>
</html>
"""

dest_path = "/tmp/beyond-likes-git/docs/index.html"
with open(dest_path, "w", encoding="utf-8") as f:
    f.write(NEW_DOCS_HTML)

print(f"Warm editorial docs written to: {dest_path}")
