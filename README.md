<div align="center">

# <span style="font-family: 'Courier New', Courier, monospace; font-weight: 900; font-size: 2.5em; letter-spacing: 8px; text-transform: uppercase; line-height: 1.1;">SGNL</span>
// SIGNAL EXTRACTION ENGINE

**STOP READING GARBAGE.**
[![License](https://img.shields.io/badge/license-Apache%202.0-orange)](LICENSE)
[![Stars](https://img.shields.io/github/stars/metin-korkmaz/sgnl)](https://github.com/metin-korkmaz/sgnl/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/metin-korkmaz/sgnl)](https://github.com/metin-korkmaz/sgnl/commits/main)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/downloads/release/python-311/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/docker-available-blue)](https://www.docker.com/)

*Signal extraction for information filtering.*

</div>

---

<div align="center">

**🌐 Language Selection / Dil Seçimi**

[🇬🇧 English](README.md) | [🇹🇷 Türkçe](README_TR.md)

</div>

---

## 📖 What Is This Really? (TL;DR)

**SGNL is a smart filter that separates high-quality content from the noise.**

Think of it as a research assistant that reads through articles, papers, and web content, then tells you:
- What's actually worth reading (signal)
- What's just fluff or marketing (noise)

**How it works in 3 seconds:**
1. You search for a topic
2. SGNL finds content and scores it for quality/density
3. You get only the valuable stuff, analyzed by AI

**Perfect for:** Researchers, developers, students, or anyone drowning in information overload.

---

## 🎯 The Approach: Filtering Noise

The web has a lot of content. Some is useful. Some is not.

**SGNL tries to help you find the useful parts.**

```python
core_principles = {
    "SIGNAL": "Code benchmarks, peer-reviewed research, primary sources.",
    "NOISE": "Listicles, excessive intros, generic content.",
    "METHOD": "We filter and analyze. Not perfect, but hopefully helpful."
}
```

---

## 📊 How Signal Score is Calculated

SGNL uses a **multi-layered scoring system** that combines heuristics, density analysis, and LLM evaluation to determine content quality.

### Scoring Architecture

```
┌─────────────────────────────────────────┐
│  Heuristic Analysis (Fast, <100ms) │
│  ────────────────────────────────────  │
│  Code Density (±0 to +20)          │
│  Data Density (±0 to +15)           │
│  Slop Detection (-30 to +10)         │
│  Affiliate Detection (-30)             │
│  Hype Detection (-20)                 │
│                                      │
│  Final Heuristic Score: 0-100          │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  Content Density Analysis (Fast)      │
│  ────────────────────────────────────  │
│  CPIDR Score (0.0-1.0)             │
│  DEPID Score (0.0-1.0)             │
│  Readability Score                    │
│  Combined Density (0.0-1.0)          │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  Domain Reputation                   │
│  ────────────────────────────────────  │
│  High-trust domains (+8% to +15%)  │
│  Neutral domains (0%)                │
│  Spam domains (-)                    │
└─────────────────────────────────────────┘
                  ↓
         FINAL SIGNAL SCORE (0-100)
```

### 1️⃣ Heuristic Analysis (Base Layer)

**Starting Score:** 50 (neutral)

| Factor | Impact | How It's Measured |
|--------|---------|-------------------|
| **Code Density** | +0 to +20 | Counts `<pre>` and `<code>` blocks. Boosts technical content matching coding queries. |
| **Data Density** | +0 to +15 | Detects tables (`<table>`) and structured data. Indicates factual content. |
| **Slop Detection** | -30 to +10 | Analyzes HTML bloat ratio (text vs tags). Excessive markup = lower score. |
| **Affiliate Detection** | -30 flat | Scans for affiliate links, ref IDs, sponsored content. Instant penalty. |
| **Hype Detection** | -20 flat | Detects clickbait words (shocking, miracle, secret, unbelievable, etc.). |

**Example:**
```python
# Technical article with code blocks
Base: 50
+ Code density: +20 (matches query, has 5 code blocks)
+ Data density: +10 (has research tables)
- Slop: -5 (some HTML bloat)
─────────────────────────────────────────
Final: 75 (Good quality)
```

### 2️⃣ Content Density Analysis

Measures **informational density** using specialized libraries:

| Metric | Source | Range | Weight |
|---------|---------|--------|--------|
| **CPIDR** | `ideadensity` library | 0.0-1.0 | 50% |
| **DEPID** | `ideadensity` library | 0.0-1.0 | 30% |
| **Readability** | `textstat` library | 0.0-1.0 | 20% |

**How CPIDR Works:**
- Counts unique idea units (nouns, verbs, concepts)
- Measures lexical density vs. total word count
- High density = information-rich content

**How DEPID Works:**
- Uses spaCy NLP model to tag parts of speech
- Calculates idea density per sentence
- Higher density = more information per sentence

**Combined Formula:**
```
Density Score = (CPIDR × 0.5) + (DEPID × 0.3) + (Readability × 0.2)
```

**Threshold:** Content with `Density < 0.45` is flagged for skipping LLM analysis (too lightweight).

### 3️⃣ Domain Reputation

| Domain Type | Boost | Examples |
|-------------|-------|-----------|
| **Academic** | +15% | arxiv.org, nature.com, science.org |
| **Open Source** | +12% | github.com, openai.com, anthropic.com |
| **Research** | +12% | deepmind.com, distill.pub, huggingface.co |
| **Neutral** | 0% | Unknown domains |
| **Spam** | - | Known spam/affiliate farms |

**Example:**
```python
# Same content on different domains
Medium.com article → 65 (neutral domain)
arxiv.org paper → 75 (+15% academic boost)
```

### 4️⃣ Final Score Calculation

**Step 1: Heuristic Score** (0-100)
```
Base: 50
+ Code Density (+0 to +20)
+ Data Density (+0 to +15)
- Slop (-30 to +10)
- Affiliates (-30)
- Hype (-20)
─────────────────────────────────
Final: Clamped to [0, 100]
```

**Step 2: Apply Domain Boost**
```
Final Score = Heuristic Score × (1 + DomainBoost)
# Example: 75 × 1.15 = 86.25 (arxiv.org)
```

**Step 3: LLM Intelligence Report** (for Deep Scan)
- GPT-OSS-120B reads full content
- Provides semantic analysis
- Extracts key findings
- Assigns technical depth score (overrides heuristics)

### What Makes "High Signal"?

| Score Range | Rating | Characteristics |
|-------------|---------|-----------------|
| **85-100** | ⭐⭐⭐ Exceptional | Peer-reviewed research, code benchmarks, high-density academic papers |
| **70-84** | ⭐⭐ High | Technical documentation, well-structured tutorials, detailed guides |
| **50-69** | ⭐ Good | Solid content, some value, mild fluff |
| **30-49** | ⚠️ Medium | Average quality, excessive intros, listicle format |
| **0-29** | ❌ Low | Clickbait, affiliate spam, low information density |

### Why This Approach?

| Concern | Solution |
|----------|-----------|
| **Speed** | Heuristics work in <100ms, no LLM latency |
| **Accuracy** | Density analysis captures true informational value |
| **Context** | Domain reputation adds trust signals |
| **Depth** | LLM provides semantic understanding for top results |
| **Transparency** | Every score has a reason, not a black box |

---

## ⚡ System Overview

SGNL operates on a **Dual-Engine Architecture** designed to balance velocity with depth.

| Engine | Latency | Action | UX Pattern |
|--------|----------|--------|------------|
| **Fast Lane** | <1500ms | Retrieves raw Tavily search vectors | Optimistic UI — instant results table |
 | **Deep Scan** | Async (Background) | GPT-OSS-120B analyzes high-value artifacts (via Deepinfra/n8n) | Intelligence Report injected on verified signal |

### Architecture Flow

```
User Request → Fast Lane (Tavily) → Instant Results
                    ↓
               Deep Scan (GPT-OSS-120B via Deepinfra/n8n) → Signal Analysis → Intelligence Report
```

**Strategy:** The "Curator Prompt". We strictly forbid AI from lecturing. It scans for density and facts only.

**LLM Architecture:** Deep scan analysis is handled by n8n workflows using Deepinfra API with GPT-OSS-120B model for optimal performance and cost efficiency.

---

## 🎨 Design System: Swiss Brutalism

We reject smooth scrolling, excessive animations, and "delight". Tolerance for friction is zero.

### Color Palette

| Color | Hex Code | Usage |
|-------|----------|-------|
| ⬛ **Ink Black** | `#000000` | The void |
| ⬜ **Off White** | `#F4F1EA` | The paper |
| 🟧 **Safety Orange** | `#FF4500` | Alerts |
| 🟩 **Signal Green** | `#00FF00` | Verified truth |

### Typography

- **Headers:** Industrial Sans (Heavy weight)
- **Data:** Monospace/Terminal

---

## 🚀 Quick Start

### Prerequisites

- [x] Docker & Docker Compose
- [x] Valid `TAVILY_API_KEY` (for web search)
- [x] n8n instance with Deepinfra API configured (for LLM analysis)
- [ ] `OPENAI_API_KEY` (optional, for direct LLM calls)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/metin-korkmaz/sgnl.git
cd sgnl

# 2. Configure environment
cp .env.example .env
nano .env  # Add your API keys

# 3. Ignite
docker compose up -d --build
```

### Access

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |
| **Health Check** | http://localhost:8000/health |

---

## 🔒 Security

### Production Features

| Feature | Status | Description |
|---------|--------|-------------|
| ✅ No Hardcoded Credentials | Enabled | All secrets in environment variables |
| ✅ Restricted CORS | Enabled | Domain-specific access only |
| ✅ SSL/TLS Encryption | Enabled | Via Nginx Proxy Manager |
| ✅ Rate Limiting | Enabled | 3 req/min/IP (configurable) |
| ✅ Network Isolation | Enabled | Docker network security |

### Domain Configuration

```
Production: https://your-domain.com
n8n:       http://n8n.your-domain.com (internal)
```

### Environment Setup

```bash
# Copy example file
cp .env.example .env

# Edit with your credentials
nano .env

# Configure n8n URLs (use domains, not IP addresses)
N8N_WEBHOOK_URL=http://n8n.your-domain.com/webhook/sgnl/scan-topic
N8N_FAST_SEARCH_URL=http://n8n.your-domain.com/webhook/fast-search

# Configure CORS origins
ALLOWED_ORIGINS=https://your-domain.com
```

📖 **Full deployment guide:** [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 📊 API Endpoints

### Health & Status

```bash
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "version": "2.0.0",
  "openai_configured": true
}
```

### Content Extraction

```bash
POST /extract
Content-Type: application/json

{
  "url": "https://example.com/article"
}
```

### Deep Scan (with LLM Analysis)

```bash
POST /deep-scan
Content-Type: application/json

{
  "url": "https://example.com/technical-article"
}
```

### Fast Search (Raw Results)

```bash
POST /fast-search
Content-Type: application/json

{
  "topic": "machine learning benchmarks",
  "max_results": 10
}
```

### Topic Scan (Full Analysis)

```bash
POST /scan-topic
Content-Type: application/json

{
  "topic": "rust vs go performance",
  "max_results": 10
}
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ❌ No | - | OpenAI API key (optional, for direct LLM calls) |
| `TAVILY_API_KEY` | ✅ Yes | - | Tavily API key for web search |
| `N8N_WEBHOOK_URL` | ✅ Yes | - | n8n deep scan webhook URL |
| `N8N_FAST_SEARCH_URL` | ✅ Yes | - | n8n fast search webhook URL |
| `ALLOWED_ORIGINS` | ❌ No | `https://sgnl.metinkorkmaz.quest` | CORS allowed origins |
| `RATE_LIMIT` | ❌ No | 3 | Max requests per IP/minute |
| `RATE_WINDOW_SECONDS` | ❌ No | 60 | Rate limiting time window |
| `HOST` | ❌ No | 0.0.0.0 | API server host |
| `PORT` | ❌ No | 8000 | API server port |
| `LOG_LEVEL` | ❌ No | INFO | Logging verbosity |
| `DENSITY_THRESHOLD` | ❌ No | 0.45 | Content density threshold (0.0-1.0) |
| `LLM_MAX_CHARS` | ❌ No | 12000 | Max content length for LLM |

---

## 🛠️ Development

### Local Development

```bash
# Use development config
cp .env.dev .env
nano .env  # Add your dev API keys

# Start with port mapping
docker-compose -f docker-compose.dev.yml up --build

# Access at http://localhost:8000
```

### Running Tests

```bash
cd app
pytest tests/
```

### Project Structure

```
sgnl/
├── app/
│   ├── main.py              # FastAPI application
│   ├── extractor.py         # Content extraction engine
│   ├── models.py           # Pydantic models
│   ├── services/
│   │   └── analyzer.py     # Heuristic content analysis
│   ├── static/             # CSS, JS assets
│   ├── templates/          # HTML templates
│   └── tests/             # Test suite
├── docs/                  # Documentation
│   ├── ARCHITECTURE.md     # System architecture
│   ├── DEPLOYMENT.md       # Deployment guide
│   └── DEPLOYMENT_CHECKLIST.md
├── docker-compose.yml      # Production config
├── docker-compose.dev.yml # Development config
└── .env.example           # Environment template
```

---

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Container won't start** | Check `docker-compose logs sgnl-api` and verify `.env` exists |
| **n8n connection failed** | Verify `N8N_WEBHOOK_URL` is set and n8n is running |
| **CORS errors** | Check `ALLOWED_ORIGINS` includes your domain |
| **Rate limiting too strict** | Increase `RATE_LIMIT` in `.env` |
| **SSL certificate issues** | See [docs/DEPLOYMENT.md#troubleshooting](docs/DEPLOYMENT.md#troubleshooting) |

### Debug Commands

```bash
# Check container logs
docker-compose logs -f sgnl-api

# Check container status
docker ps | grep sgnl-api

# Test health endpoint
curl http://localhost:8000/health

# Enter container shell
docker exec -it sgnl-api bash

# Check environment variables
docker exec sgnl-api env | grep -E "API_KEY|N8N"
```

---

## 📈 Performance

### Technical Constraints

| Metric | Value | Notes |
|--------|-------|-------|
| **Rate Limit** | 3 req/min/IP (default) | Configurable via `RATE_LIMIT` |
| **Max Content Size** | 12,000 chars | Configurable via `LLM_MAX_CHARS` |
| **Density Threshold** | 0.45 | Configurable via `DENSITY_THRESHOLD` |
| **Fast Search Latency** | <1500ms | Raw Tavily results |
 | **Deep Scan Latency** | 2-5s | With GPT-OSS-120B analysis (via Deepinfra/n8n) |

### Enforcement

- **Rate Limiting:** Middleware intercepts abuse at edge. 429 codes trigger hard cooldown.
- **Privacy:** No user tracking. Logs are ephemeral.
- **Content Filtering:** Low-density content skipped automatically (CPIDR scoring).

---

## 📚 Documentation

- **[docs/](docs/)** - Complete documentation index
  - **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture and design
  - **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Full deployment guide with Nginx Proxy Manager
  - **[DEPLOYMENT_CHECKLIST.md](docs/DEPLOYMENT_CHECKLIST.md)** - Step-by-step deployment verification

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the Apache License 2.0.

---

## 👤 Maintainer

**Metin Samet Korkmaz**

[![GitHub](https://img.shields.io/badge/GitHub-metin--korkmaz-blue)](https://github.com/metin-korkmaz)

---

## 🏷️ Status

```
Status:        OPERATIONAL (see badge above)
Last Updated:  December 29, 2025
```

---

<div align="center">

**Information filtering tool.**

*Trying to help you find better content.*

</div>
