# Google Perspective API Drop-in Migration Guide

> **Sunset Notice:** Google Perspective API will be completely shut down on **December 31, 2026**.  
> Beyond Likes provides a 100% schema-compatible drop-in endpoint with zero code changes required in your parsing logic.

---

## ⚡ The 1-Line Migration

Replace the Google endpoint URL with the Beyond Likes endpoint:

### Before (Google Perspective API)
```text
POST https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=YOUR_GOOGLE_KEY
```

### After (Beyond Likes Engine)
```text
POST https://api.beyondlikes.io/v1/comments:analyze (or http://localhost:8888/v1/comments:analyze)
```

---

## 💻 Code Examples

### 1. Python (`requests`)

```python
import requests

# OLD:
# url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=AIzaSy..."

# NEW (Beyond Likes Drop-in):
url = "http://localhost:8888/v1/comments:analyze"

payload = {
    "comment": {"text": "You are a clown and an absolute idiot"},
    "requestedAttributes": {
        "TOXICITY": {},
        "INSULT": {},
        "PROFANITY": {}
    },
    "languages": ["en"]
}

response = requests.post(url, json=payload).json()

# Existing parsing logic works unchanged:
toxicity = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
print(f"Toxicity Probability: {toxicity * 100:.1f}%")

# BONUS: Access Beyond Likes Prosocial Guidance Metadata:
meta = response.get("_beyond_likes_metadata", {})
print(f"Beyond Likes Quality Score: {meta.get('composite_quality_score')}/100")
```

---

### 2. Node.js / JavaScript (`fetch`)

```javascript
// NEW (Beyond Likes Drop-in):
const res = await fetch("http://localhost:8888/v1/comments:analyze", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    comment: { text: "While I disagree with the conclusion, here is the data..." },
    requestedAttributes: { TOXICITY: {} }
  })
});

const data = await res.json();
console.log("Toxicity Score:", data.attributeScores.TOXICITY.summaryScore.value);
```

---

### 3. cURL Command

```bash
curl -X POST http://localhost:8888/v1/comments:analyze \
  -H "Content-Type: application/json" \
  -d '{
    "comment": {"text": "You are an idiot"},
    "requestedAttributes": {"TOXICITY": {}}
  }'
```

---

## 🎯 What You Gain Beyond Google Perspective

| Feature | Google Perspective (Legacy) | Beyond Likes Engine |
| :--- | :--- | :--- |
| **API Availability** | ❌ Sunsetting Dec 31, 2026 | ✅ Supported & Actively Maintained |
| **Moderation Type** | Purely Punitive (Flag & Delete) | Normative & Elevating (Guidance) |
| **In-Composer Guidance** | ❌ None | ✅ Real-time constructive rewrites |
| **Epistemic Scoring** | ❌ None | ✅ Evaluates citations, evidence & logic |
| **Sarcasm Handling** | ⚠️ High False Positives | ✅ Contextual multi-factor rubric |
| **Custom Policies** | ❌ Fixed Google thresholds | ✅ Newsroom, Academic, Dev Forum packs |
