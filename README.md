# SGNL // SIGNAL EXTRACTION ENGINE 

> **STOP READING GARBAGE.**

## 1. THE MANIFESTO: ANTI-SLOP
The modern internet is broken. It is a landfill of SEO spam, affiliate farms, and AI-generated noise. Google has abdicated its role as a curator, favoring engagement over truth.

**SGNL exists to reclaim the Signal.**

### core_principles = {
  "SIGNAL": "High-density information. Code benchmarks, peer-reviewed research, primary sources.",
  "NOISE": "Listicles, 'SEO-optimized' fluff, anecdotal marketing, 10-minute intros.",
  "METHOD": "We do not 'search'. We 'curate'. LLMs are strict editors, not creative writers."
}

---

## 2. SYSTEM OVERVIEW
SGNL operates on a **Dual-Engine Architecture** designed to balance velocity with depth.

### [A] The Fast Lane (Velocity)
- **Latency:** <1500ms
- **Action:** Retreives raw, unmodified search vectors via `Tavily API`.
- **UX Pattern:** Optimistic UI. The results table renders instantly. We do not wait for intelligence.

### [B] The Deep Scan (Intelligence)
- **Latency:** Asynchronous (Background)
- **Action:** `GPT-4o` analyzes specific high-value artifacts.
- **Output:** An "Intelligence Report" injected into the DOM only when the signal is verified.
- **Strategy:** The "Curator Prompt". We strictly forbid the AI from lecturing. It scans for density and facts only.

---

## 3. DESIGN SYSTEM: SWISS BRUTALISM
We reject smooth scrolling, excessive animations, and "delight". Tolerance for friction is zero.

- **Palette:**
  - `INK_BLACK (#000000)`: The void.
  - `OFF_WHITE (#F4F1EA)`: The paper.
  - `SAFETY_ORANGE (#FF4500)`: The alert.
  - `SIGNAL_GREEN (#00FF00)`: The verified truth.

- **Typography:**
  - Headers: Industrial Sans (Heavy weight).
  - Data: Monospace/Terminal. 

---

## 4. INSTALLATION

### Prerequisites
- Docker & Docker Compose
- valid `OPENAI_API_KEY`
- valid `TAVILY_API_KEY`

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/sgnl/engine.git
cd engine

# 2. Configure Environment
cp .env.example .env
# Edit .env and add your API keys (OPENAI_API_KEY, TAVILY_API_KEY)
# Optionally configure n8n webhook URLs and rate limiting parameters

# 3. Ignite
docker compose up -d --build
```

### Access
- **Frontend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 5. SECURITY

### Production Deployment
- ✅ No hardcoded credentials or IP addresses
- ✅ CORS restricted to specific domains only
- ✅ SSL/TLS encryption via Nginx Proxy Manager
- ✅ Environment variables for all sensitive data
- ✅ Rate limiting enabled by default

### Domain Configuration
- Production: `https://sgnl.metinkorkmaz.quest`
- n8n: `http://n8n.metinkorkmaz.quest` (internal Docker network)

### Environment Setup
```bash
# Copy example file
cp .env.example .env

# Edit with your credentials
nano .env

# Configure n8n URLs using domains (not IP addresses)
N8N_WEBHOOK_URL=http://n8n.metinkorkmaz.quest/webhook/sgnl/scan-topic
N8N_FAST_SEARCH_URL=http://n8n.metinkorkmaz.quest/webhook/fast-search

# Configure allowed CORS origins
ALLOWED_ORIGINS=https://sgnl.metinkorkmaz.quest
```

### Deployment Documentation
For detailed deployment instructions with Nginx Proxy Manager, see [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 6. TECHNICAL CONSTRAINTS
- **Rate Limit:** 20 Requests / Minute / IP (configurable).
- **Enforcement:** Middleware intercepts abuse at the edge. 429 Codes trigger a hard cooldown.
- **Privacy:** No user tracking. Logs are ephemeral.

**Maintained by:** Project SGNL Architects.
**Status:** `OPERATIONAL`
