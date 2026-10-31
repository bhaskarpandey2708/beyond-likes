/**
 * Beyond Likes In-Composer Discourse Assistant (Content Script)
 * Attaches a floating prosocial score pill to textareas and contenteditable inputs.
 */

let debounceTimer = null;

function createBadgeForInput(target) {
  if (target.dataset.beyondLikesAttached) return;
  target.dataset.beyondLikesAttached = "true";

  // Create Badge Container
  const badge = document.createElement("div");
  badge.className = "beyond-likes-pill";
  badge.style.cssText = `
    position: absolute;
    right: 12px;
    bottom: 12px;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 3px 10px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 11px;
    font-weight: 600;
    color: #8b949e;
    cursor: pointer;
    z-index: 9999;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    transition: all 0.2s ease;
    display: none;
  `;
  badge.innerText = "Beyond Likes: Ready";

  // Position relative to parent
  const parent = target.parentElement;
  if (getComputedStyle(parent).position === "static") {
    parent.style.position = "relative";
  }
  parent.appendChild(badge);

  // Tooltip
  const tooltip = document.createElement("div");
  tooltip.style.cssText = `
    position: absolute;
    right: 0;
    bottom: 32px;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    color: #e6edf3;
    width: 280px;
    display: none;
    z-index: 10000;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
  `;
  badge.appendChild(tooltip);

  badge.addEventListener("mouseenter", () => tooltip.style.display = "block");
  badge.addEventListener("mouseleave", () => tooltip.style.display = "none");

  // Input listener
  target.addEventListener("input", () => {
    const text = target.value || target.innerText || "";
    if (text.trim().length < 5) {
      badge.style.display = "none";
      return;
    }

    badge.style.display = "block";
    badge.innerText = "Evaluating...";

    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
      try {
        const resp = await fetch("http://localhost:8888/v1/score", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text })
        });
        const data = await resp.json();

        // Update badge appearance
        const score = data.composite_score;
        badge.innerText = `Quality: ${score}/100`;

        if (data.status === "APPROVED_PROMOTED") {
          badge.style.borderColor = "#238636";
          badge.style.color = "#3fb950";
        } else if (data.status === "FLAGGED_UNCIVIL" || data.status === "FLAGGED_SPAM") {
          badge.style.borderColor = "#da3633";
          badge.style.color = "#f87171";
        } else {
          badge.style.borderColor = "#1f6feb";
          badge.style.color = "#58a6ff";
        }

        // Update tooltip
        let tipHtml = `<strong>Discourse Status:</strong> ${data.status}<br/>`;
        tipHtml += `Civility: ${data.dimensions.civility}% | Constructive: ${data.dimensions.constructiveness}%<br/>`;
        if (data.guidance && data.guidance.suggested_revision) {
          tipHtml += `<div style="margin-top: 6px; padding: 6px; background: rgba(35,134,54,0.15); border-left: 2px solid #3fb950; font-style: italic;">"${data.guidance.suggested_revision}"</div>`;
        }
        tooltip.innerHTML = tipHtml;

      } catch (err) {
        badge.innerText = "Beyond Likes: Offline";
        badge.style.color = "#8b949e";
      }
    }, 450);
  });
}

// Observe DOM for textareas
function attachListeners() {
  document.querySelectorAll("textarea").forEach(createBadgeForInput);
}

setInterval(attachListeners, 2000);
attachListeners();
console.log("Beyond Likes Discourse Assistant Active.");
