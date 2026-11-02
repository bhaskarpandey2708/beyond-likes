/**
 * Normative Intelligence Universal Embeddable Discourse Widget (v1.0)
 * Drop-in <script> tag for any comment box, forum, or CMS.
 * Usage: <script src="http://localhost:8888/widget/beyond-likes.js" data-api="http://localhost:8888"></script>
 */
(function() {
  const currentScript = document.currentScript;
  const API_BASE = (currentScript && currentScript.dataset.api) || "http://localhost:8888";
  const POLICY = (currentScript && currentScript.dataset.policy) || "newsroom";

  function injectStyles() {
    if (document.getElementById("beyond-likes-widget-style")) return;
    const style = document.createElement("style");
    style.id = "beyond-likes-widget-style";
    style.innerHTML = `
      .bl-widget-container {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 10px 14px;
        margin-top: 8px;
        color: #e6edf3;
        font-size: 12px;
        display: none;
        transition: all 0.2s ease;
      }
      .bl-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
      }
      .bl-title {
        font-weight: 700;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #8b949e;
      }
      .bl-score-badge {
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
        font-family: monospace;
      }
      .bl-badge-green { background: rgba(46,160,67,0.2); color: #3fb950; border: 1px solid rgba(46,160,67,0.4); }
      .bl-badge-blue { background: rgba(56,139,253,0.2); color: #58a6ff; border: 1px solid rgba(56,139,253,0.4); }
      .bl-badge-red { background: rgba(248,81,73,0.2); color: #f85149; border: 1px solid rgba(248,81,73,0.4); }
      .bl-badge-amber { background: rgba(210,153,34,0.2); color: #d29922; border: 1px solid rgba(210,153,34,0.4); }

      .bl-bars {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin: 8px 0;
      }
      .bl-bar-item {
        display: flex;
        flex-direction: column;
        gap: 2px;
      }
      .bl-bar-label {
        font-size: 10px;
        color: #8b949e;
        display: flex;
        justify-content: space-between;
      }
      .bl-bar-track {
        height: 4px;
        background: #21262d;
        border-radius: 2px;
        overflow: hidden;
      }
      .bl-bar-fill {
        height: 100%;
        border-radius: 2px;
        transition: width 0.3s ease;
      }

      .bl-suggestion-box {
        margin-top: 8px;
        background: rgba(35,134,54,0.1);
        border-left: 3px solid #3fb950;
        border-radius: 0 4px 4px 0;
        padding: 8px 10px;
        font-size: 11px;
        line-height: 1.4;
      }
      .bl-btn-apply {
        background: #238636;
        color: white;
        border: none;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
        cursor: pointer;
        margin-top: 4px;
      }
      .bl-btn-apply:hover { background: #2ea043; }
    `;
    document.head.appendChild(style);
  }

  function attachWidget(textarea) {
    if (textarea.dataset.blAttached) return;
    textarea.dataset.blAttached = "true";

    const container = document.createElement("div");
    container.className = "bl-widget-container";
    container.innerHTML = `
      <div class="bl-header">
        <span class="bl-title">Normative Intelligence Score</span>
        <span class="bl-score-badge bl-badge-blue" id="bl-score">--</span>
      </div>
      <div class="bl-bars">
        <div class="bl-bar-item">
          <div class="bl-bar-label"><span>Constructiveness</span><span id="bl-val-const">--</span></div>
          <div class="bl-bar-track"><div class="bl-bar-fill" id="bl-fill-const" style="width:0%; background:#3fb950;"></div></div>
        </div>
        <div class="bl-bar-item">
          <div class="bl-bar-label"><span>Civility</span><span id="bl-val-civ">--</span></div>
          <div class="bl-bar-track"><div class="bl-bar-fill" id="bl-fill-civ" style="width:0%; background:#58a6ff;"></div></div>
        </div>
      </div>
      <div class="bl-suggestion-box" id="bl-sug-box" style="display:none;">
        <div style="font-weight:600; color:#3fb950; margin-bottom:2px;">💡 Prosocial Suggestion:</div>
        <div id="bl-sug-text" style="font-style:italic; color:#e6edf3;"></div>
        <button class="bl-btn-apply" id="bl-btn-apply">Apply Suggestion</button>
      </div>
    `;

    textarea.parentNode.insertBefore(container, textarea.nextSibling);

    let timer = null;
    let latestSuggestion = "";

    const applyBtn = container.querySelector("#bl-btn-apply");
    applyBtn.addEventListener("click", (e) => {
      e.preventDefault();
      if (latestSuggestion) {
        textarea.value = latestSuggestion;
        textarea.dispatchEvent(new Event("input", { bubbles: true }));
      }
    });

    textarea.addEventListener("input", () => {
      const text = textarea.value.trim();
      if (text.length < 5) {
        container.style.display = "none";
        return;
      }

      container.style.display = "block";
      clearTimeout(timer);
      timer = setTimeout(async () => {
        try {
          const resp = await fetch(`${API_BASE}/v1/score`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, policy: POLICY })
          });
          const data = await resp.json();

          const scoreBadge = container.querySelector("#bl-score");
          scoreBadge.innerText = `${data.composite_score}/100`;

          if (data.status === "APPROVED_PROMOTED") {
            scoreBadge.className = "bl-score-badge bl-badge-green";
          } else if (data.status === "FLAGGED_UNCIVIL" || data.status === "FLAGGED_SPAM") {
            scoreBadge.className = "bl-score-badge bl-badge-red";
          } else {
            scoreBadge.className = "bl-score-badge bl-badge-blue";
          }

          const d = data.dimensions;
          container.querySelector("#bl-val-const").innerText = `${d.constructiveness}%`;
          container.querySelector("#bl-fill-const").style.width = `${d.constructiveness}%`;

          container.querySelector("#bl-val-civ").innerText = `${d.civility}%`;
          container.querySelector("#bl-fill-civ").style.width = `${d.civility}%`;

          const sugBox = container.querySelector("#bl-sug-box");
          if (data.guidance && data.guidance.needs_revision && data.guidance.suggested_revision) {
            sugBox.style.display = "block";
            latestSuggestion = data.guidance.suggested_revision;
            container.querySelector("#bl-sug-text").innerText = `"${latestSuggestion}"`;
          } else {
            sugBox.style.display = "none";
          }
        } catch (err) {
          console.warn("Normative Intelligence widget error:", err);
        }
      }, 400);
    });
  }

  function init() {
    injectStyles();
    document.querySelectorAll("textarea").forEach(attachWidget);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
