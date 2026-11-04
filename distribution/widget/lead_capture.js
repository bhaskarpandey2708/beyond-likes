/**
 * Normative Intelligence — Visitor Telemetry & 1-Minute Lead Capture Engine
 * Captures visitor geo-origin, engagement interest, and prompts an executive
 * consultation modal after 60 seconds (or on high engagement).
 */
(function() {
  if (typeof window === 'undefined') return;

  const LEAD_STORAGE_KEY = 'normative_lead_status';
  const SNOOZE_HOURS = 24;
  const MODAL_DELAY_MS = 60000; // 60 seconds (1 minute)

  // Track session details
  const sessionData = {
    sessionId: 'sess_' + Math.random().toString(36).substring(2, 11) + '_' + Date.now(),
    page: window.location.pathname,
    referrer: document.referrer || 'direct',
    startTime: Date.now(),
    country: 'United States',
    countryCode: 'US',
    dialCode: '+1',
    interests: []
  };

  // Comprehensive International Dial Codes
  const COUNTRY_DIAL_CODES = [
    { name: "United States", code: "US", dial: "+1", flag: "🇺🇸" },
    { name: "United Kingdom", code: "GB", dial: "+44", flag: "🇬🇧" },
    { name: "India", code: "IN", dial: "+91", flag: "🇮🇳" },
    { name: "Germany", code: "DE", dial: "+49", flag: "🇩🇪" },
    { name: "Canada", code: "CA", dial: "+1", flag: "🇨🇦" },
    { name: "Australia", code: "AU", dial: "+61", flag: "🇦🇺" },
    { name: "France", code: "FR", dial: "+33", flag: "🇫🇷" },
    { name: "Japan", code: "JP", dial: "+81", flag: "🇯🇵" },
    { name: "Singapore", code: "SG", dial: "+65", flag: "🇸🇬" },
    { name: "Netherlands", code: "NL", dial: "+31", flag: "🇳🇱" },
    { name: "Sweden", code: "SE", dial: "+46", flag: "🇸🇪" },
    { name: "Switzerland", code: "CH", dial: "+41", flag: "🇨🇭" },
    { name: "United Arab Emirates", code: "AE", dial: "+971", flag: "🇦🇪" },
    { name: "Ireland", code: "IE", dial: "+353", flag: "🇮🇪" },
    { name: "Brazil", code: "BR", dial: "+55", flag: "🇧🇷" },
    { name: "Israel", code: "IL", dial: "+972", flag: "🇮🇱" },
    { name: "South Korea", code: "KR", dial: "+82", flag: "🇰🇷" },
    { name: "Spain", code: "ES", dial: "+34", flag: "🇪🇸" },
    { name: "Italy", code: "IT", dial: "+39", flag: "🇮🇹" },
    { name: "South Africa", code: "ZA", dial: "+27", flag: "🇿🇦" }
  ];

  // 1. Detect Visitor Country via IP / Locale
  async function detectGeoOrigin() {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 2200);
      const res = await fetch('https://ipapi.co/json/', { signal: controller.signal });
      clearTimeout(timeoutId);
      if (res.ok) {
        const data = await res.json();
        if (data.country_name) sessionData.country = data.country_name;
        if (data.country_code) sessionData.countryCode = data.country_code;
        if (data.country_calling_code) sessionData.dialCode = data.country_calling_code;
      }
    } catch (e) {
      // Fallback: Timezone-based country approximation
      try {
        const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
        if (tz.includes('Calcutta') || tz.includes('Kolkata') || tz.includes('Asia/Colombo')) {
          sessionData.country = 'India'; sessionData.countryCode = 'IN'; sessionData.dialCode = '+91';
        } else if (tz.includes('London')) {
          sessionData.country = 'United Kingdom'; sessionData.countryCode = 'GB'; sessionData.dialCode = '+44';
        } else if (tz.includes('Berlin') || tz.includes('Frankfurt')) {
          sessionData.country = 'Germany'; sessionData.countryCode = 'DE'; sessionData.dialCode = '+49';
        } else if (tz.includes('Tokyo')) {
          sessionData.country = 'Japan'; sessionData.countryCode = 'JP'; sessionData.dialCode = '+81';
        }
      } catch (err) {}
    }

    // Send initial telemetry ping
    sendTelemetryPing('initial_visit');
  }

  function sendTelemetryPing(action) {
    const elapsedSec = Math.round((Date.now() - sessionData.startTime) / 1000);
    const payload = {
      session_id: sessionData.sessionId,
      page: sessionData.page,
      referrer: sessionData.referrer,
      country: sessionData.country,
      country_code: sessionData.countryCode,
      time_spent: elapsedSec,
      action: action,
      interests: sessionData.interests
    };
    try {
      fetch('/v1/telemetry/visit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).catch(() => {});
    } catch (e) {}
  }

  // 2. Track Interest Clicks
  function setupInterestTracking() {
    document.addEventListener('click', (e) => {
      const target = e.target.closest('a, button, [data-interest]');
      if (!target) return;
      
      let interest = target.getAttribute('data-interest') || target.innerText.trim();
      if (interest.length > 50) interest = interest.substring(0, 50);

      if (interest && !sessionData.interests.includes(interest)) {
        sessionData.interests.push(interest);
      }
    }, true);
  }

  // 3. Check Modal Eligibility
  function isEligibleForModal() {
    try {
      const stored = localStorage.getItem(LEAD_STORAGE_KEY);
      if (!stored) return true;
      const parsed = JSON.parse(stored);
      if (parsed.submitted) return false;
      if (parsed.snoozedUntil && Date.now() < parsed.snoozedUntil) return false;
      return true;
    } catch (e) {
      return true;
    }
  }

  function markModalSnoozed() {
    try {
      const snoozeUntil = Date.now() + (SNOOZE_HOURS * 60 * 60 * 1000);
      localStorage.setItem(LEAD_STORAGE_KEY, JSON.stringify({ submitted: false, snoozedUntil: snoozeUntil }));
    } catch (e) {}
  }

  function markModalSubmitted() {
    try {
      localStorage.setItem(LEAD_STORAGE_KEY, JSON.stringify({ submitted: true, timestamp: Date.now() }));
    } catch (e) {}
  }

  // 4. Build and Inject Modal DOM
  function injectModalCSS() {
    if (document.getElementById('normative-lead-modal-css')) return;
    const style = document.createElement('style');
    style.id = 'normative-lead-modal-css';
    style.textContent = `
      .nlm-backdrop {
        position: fixed;
        inset: 0;
        background: rgba(15, 23, 42, 0.72);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        z-index: 99999999;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.3s ease, visibility 0.3s ease;
      }
      .nlm-backdrop.nlm-visible {
        opacity: 1;
        visibility: visible;
      }
      .nlm-card {
        background: #FAF8F5;
        border: 1px solid #E7E5E4;
        border-radius: 16px;
        max-width: 540px;
        width: 100%;
        box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.35);
        padding: 32px;
        position: relative;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #18181B;
        transform: translateY(20px) scale(0.97);
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      }
      .nlm-backdrop.nlm-visible .nlm-card {
        transform: translateY(0) scale(1);
      }
      .nlm-close {
        position: absolute;
        top: 18px;
        right: 20px;
        background: transparent;
        border: none;
        font-size: 24px;
        line-height: 1;
        color: #78716C;
        cursor: pointer;
        padding: 4px 8px;
        border-radius: 6px;
        transition: color 0.15s, background 0.15s;
      }
      .nlm-close:hover {
        color: #18181B;
        background: #E7E5E4;
      }
      .nlm-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(200, 68, 27, 0.1);
        color: #C8441B;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        padding: 4px 10px;
        border-radius: 4px;
        margin-bottom: 12px;
      }
      .nlm-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #18181B;
        line-height: 1.25;
        margin-bottom: 8px;
      }
      .nlm-subtitle {
        font-size: 0.92rem;
        color: #78716C;
        line-height: 1.5;
        margin-bottom: 22px;
      }
      .nlm-form-group {
        margin-bottom: 14px;
        text-align: left;
      }
      .nlm-label {
        display: block;
        font-size: 0.8rem;
        font-weight: 700;
        color: #44403C;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.03em;
      }
      .nlm-input, .nlm-select {
        width: 100%;
        box-sizing: border-box;
        padding: 10px 14px;
        border: 1px solid #D6D3D1;
        border-radius: 8px;
        background: #FFFFFF;
        font-size: 0.92rem;
        color: #18181B;
        outline: none;
        transition: border-color 0.15s, box-shadow 0.15s;
      }
      .nlm-input:focus, .nlm-select:focus {
        border-color: #C8441B;
        box-shadow: 0 0 0 3px rgba(200, 68, 27, 0.15);
      }
      .nlm-phone-flex {
        display: flex;
        gap: 8px;
      }
      .nlm-dial-select {
        width: 140px;
        flex-shrink: 0;
      }
      .nlm-btn-submit {
        width: 100%;
        background: #C8441B;
        color: #FFFFFF;
        border: none;
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 700;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        margin-top: 20px;
        transition: background 0.15s, transform 0.1s;
      }
      .nlm-btn-submit:hover {
        background: #A83614;
        transform: translateY(-1px);
      }
      .nlm-footer-note {
        font-size: 0.76rem;
        color: #A8A29E;
        text-align: center;
        margin-top: 14px;
      }
      .nlm-success-box {
        text-align: center;
        padding: 24px 0;
      }
      .nlm-success-icon {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: rgba(13, 92, 78, 0.12);
        color: #0D5C4E;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        margin: 0 auto 16px auto;
      }
    `;
    document.head.appendChild(style);
  }

  function showLeadCaptureModal() {
    if (!isEligibleForModal()) return;

    injectModalCSS();

    let backdrop = document.getElementById('normative-lead-modal');
    if (!backdrop) {
      backdrop = document.createElement('div');
      backdrop.id = 'normative-lead-modal';
      backdrop.className = 'nlm-backdrop';

      // Pre-populate country options
      let dialOptionsHTML = '';
      let matchedDial = false;
      COUNTRY_DIAL_CODES.forEach(c => {
        const isSelected = (c.code === sessionData.countryCode || c.dial === sessionData.dialCode) && !matchedDial;
        if (isSelected) matchedDial = true;
        dialOptionsHTML += `<option value="${c.dial}" ${isSelected ? 'selected' : ''}>${c.flag} ${c.code} (${c.dial})</option>`;
      });
      if (!matchedDial) {
        dialOptionsHTML = `<option value="${sessionData.dialCode}" selected>🌍 ${sessionData.countryCode} (${sessionData.dialCode})</option>` + dialOptionsHTML;
      }

      backdrop.innerHTML = `
        <div class="nlm-card" role="dialog" aria-modal="true">
          <button class="nlm-close" id="nlm-btn-close" title="Close assessment">&times;</button>
          
          <div id="nlm-form-container">
            <div class="nlm-tag">⚡ Perspective EOL Migration Assessment</div>
            <h2 class="nlm-title">Google Perspective Shuts Down December 31, 2026.</h2>
            <p class="nlm-subtitle">
              Secure your confidential 1:1 drop-in migration timeline, zero false-positive benchmark analysis, and 30-day sandbox credentials.
            </p>

            <form id="nlm-lead-form">
              <div class="nlm-form-group">
                <label class="nlm-label" for="nlm-name">Full Name</label>
                <input class="nlm-input" type="text" id="nlm-name" placeholder="e.g. Alex Morgan" required autocomplete="name" />
              </div>

              <div class="nlm-form-group">
                <label class="nlm-label" for="nlm-email">Work Email</label>
                <input class="nlm-input" type="email" id="nlm-email" placeholder="alex@newsroom.com" required autocomplete="email" />
              </div>

              <div class="nlm-form-group">
                <label class="nlm-label" for="nlm-phone">Mobile / Direct Phone Number</label>
                <div class="nlm-phone-flex">
                  <select class="nlm-select nlm-dial-select" id="nlm-dial-code">
                    ${dialOptionsHTML}
                  </select>
                  <input class="nlm-input" type="tel" id="nlm-phone" placeholder="Contact number" required autocomplete="tel" />
                </div>
              </div>

              <div class="nlm-form-group">
                <label class="nlm-label" for="nlm-interest">Primary Architecture Interest</label>
                <select class="nlm-select" id="nlm-interest">
                  <option value="Google Perspective API Migration (Urgent Cutover)" selected>Google Perspective API Migration (Urgent Cutover)</option>
                  <option value="Digital Newsroom & Media Comment Moderation">Digital Newsroom & Media Comment Moderation</option>
                  <option value="Enterprise Discourse / WordPress VIP / Coral Project">Enterprise Discourse / WordPress VIP / Coral Project</option>
                  <option value="Substantive Epistemic Governance & In-Composer Coaching">Substantive Epistemic Governance & In-Composer Coaching</option>
                  <option value="Empirical Benchmarks & Custom Policy Modeling">Empirical Benchmarks & Custom Policy Modeling</option>
                </select>
              </div>

              <button type="submit" class="nlm-btn-submit" id="nlm-submit-btn">
                <span>Claim Architecture Packet &amp; Sandbox Access</span>
                &rarr;
              </button>

              <div class="nlm-footer-note">
                Sovereign enterprise infrastructure &bull; Zero spam &bull; Confidentiality guaranteed
              </div>
            </form>
          </div>

          <div id="nlm-success-container" style="display: none;">
            <div class="nlm-success-box">
              <div class="nlm-success-icon">✓</div>
              <h3 style="font-size: 1.4rem; font-weight: 800; color: #0D5C4E; margin-bottom: 8px;">
                Migration Assessment Registered
              </h3>
              <p style="font-size: 0.95rem; color: #78716C; margin-bottom: 24px; line-height: 1.5;">
                Thank you. Our principal systems architect has been dispatched to coordinate your zero-downtime cutover.
              </p>
              <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                <a href="/docs" class="nlm-btn-submit" style="display: inline-flex; width: auto; text-decoration: none; padding: 10px 24px;">
                  Access API Reference &rarr;
                </a>
                <button type="button" class="nlm-btn-submit" id="nlm-dismiss-success" style="background: #18181B; width: auto; padding: 10px 24px;">
                  Continue Exploring
                </button>
              </div>
            </div>
          </div>
        </div>
      `;

      document.body.appendChild(backdrop);

      // Event handlers
      document.getElementById('nlm-btn-close').addEventListener('click', () => {
        closeLeadModal();
        markModalSnoozed();
      });

      backdrop.addEventListener('click', (e) => {
        if (e.target === backdrop) {
          closeLeadModal();
          markModalSnoozed();
        }
      });

      document.getElementById('nlm-lead-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = document.getElementById('nlm-submit-btn');
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Securing Access...';

        const name = document.getElementById('nlm-name').value.trim();
        const email = document.getElementById('nlm-email').value.trim();
        const dial = document.getElementById('nlm-dial-code').value;
        const phone = dial + ' ' + document.getElementById('nlm-phone').value.trim();
        const interest = document.getElementById('nlm-interest').value;

        const payload = {
          name: name,
          email: email,
          phone: phone,
          country: sessionData.country,
          country_code: sessionData.countryCode,
          interest: interest,
          page: sessionData.page,
          time_on_site: Math.round((Date.now() - sessionData.startTime) / 1000),
          referrer: sessionData.referrer
        };

        try {
          const res = await fetch('/v1/leads', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          const data = await res.json();
          markModalSubmitted();

          document.getElementById('nlm-form-container').style.display = 'none';
          document.getElementById('nlm-success-container').style.display = 'block';

          document.getElementById('nlm-dismiss-success').addEventListener('click', () => {
            closeLeadModal();
          });
        } catch (err) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = 'Claim Architecture Packet &rarr;';
          alert('Could not submit assessment request. Please check your network.');
        }
      });
    }

    // Trigger visibility with subtle delay
    requestAnimationFrame(() => {
      backdrop.classList.add('nlm-visible');
    });
  }

  function closeLeadModal() {
    const backdrop = document.getElementById('normative-lead-modal');
    if (backdrop) {
      backdrop.classList.remove('nlm-visible');
    }
  }

  // 5. Lifecycle Initialization
  function init() {
    detectGeoOrigin();
    setupInterestTracking();

    // 60-Second Trigger (1 minute)
    setTimeout(() => {
      showLeadCaptureModal();
    }, MODAL_DELAY_MS);

    // Global hook for manual trigger buttons (e.g. "Request Audit")
    window.triggerLeadModal = function(customInterest) {
      if (customInterest) {
        sessionData.interests.push(customInterest);
      }
      showLeadCaptureModal();
    };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
