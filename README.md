# Beyond Likes: Discourse Intelligence Engine

> Clean-room commercial engine converting normative academic feedback research into a drop-in replacement for Google Perspective API and community quality moderation.

---

## ⚡ Quickstart

### 1. Launch the Server & Live Dashboard
```bash
python3 api/server.py
```
Open **[http://localhost:8888](http://localhost:8888)** in your browser for the interactive testing playground.

### 2. Run R&D Benchmarks
```bash
python3 benchmarks/run_benchmark.py
```

### 3. Check Token Economics & Margins
```bash
python3 economics/token_calculator.py
```

---

## 🔌 API Endpoints

### 1. Score Comment (`POST /v1/score`)
```bash
curl -X POST http://localhost:8888/v1/score \
  -H "Content-Type: application/json" \
  -d '{"text": "While I see your point, the California solar data shows battery costs dropped 18%."}'
```

### 2. Google Perspective API Drop-in (`POST /v1/comments:analyze`)
```bash
curl -X POST http://localhost:8888/v1/comments:analyze \
  -H "Content-Type: application/json" \
  -d '{"comment": {"text": "You are a clown"}, "requestedAttributes": {"TOXICITY": {}}}'
```
