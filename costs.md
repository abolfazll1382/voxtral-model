# Persian Audio to Text Project - Tools and Cost Analysis

## Project Summary
Building a Telegram bot for converting Persian voice messages to text using:
1. Voxtral Small 24B model for speech-to-text transcription
2. Dorna model for spelling and grammar correction
3. Telegram bot to serve users

---

## 1. Hardware Requirements

### Option A: Personal Server (One-time Purchase)

To run Voxtral Small 24B and Dorna simultaneously:

| Component | Required Specs | Approx. Price (USD) | Approx. Price (Toman) |
|-----------|----------------|--------------------|-----------------------|
| **GPU (Graphics Card)** | RTX 4090 24GB VRAM | $1,600 - $2,000 | 80,000,000 - 100,000,000 |
| or | RTX 3090 24GB VRAM | $1,000 - $1,400 | 50,000,000 - 70,000,000 |
| or | A6000 48GB VRAM (Best) | $4,000 - $5,000 | 200,000,000 - 250,000,000 |
| **CPU (Processor)** | Intel i7/i9 or AMD Ryzen 7/9 | $300 - $600 | 15,000,000 - 30,000,000 |
| **RAM (Memory)** | 64GB DDR4/DDR5 | $200 - $300 | 10,000,000 - 15,000,000 |
| **Storage (SSD)** | 1TB NVMe SSD | $80 - $150 | 4,000,000 - 7,500,000 |
| **Motherboard** | Compatible with GPU | $200 - $400 | 10,000,000 - 20,000,000 |
| **Power Supply** | 1000W+ | $150 - $250 | 7,500,000 - 12,500,000 |
| **Case & Cooling** | - | $100 - $200 | 5,000,000 - 10,000,000 |

**Total Initial Investment:**
- With RTX 3090: **$2,030 - $3,300** (approx. **100,000,000 - 165,000,000 Toman**)
- With RTX 4090: **$2,630 - $3,900** (approx. **130,000,000 - 195,000,000 Toman**)
- With A6000: **$5,030 - $6,900** (approx. **250,000,000 - 345,000,000 Toman**)

**Monthly Operating Costs:**
- Electricity (500-800 watts): $30 - $80 (1,500,000 - 4,000,000 Toman)
- High-speed Internet: $20 - $50 (1,000,000 - 2,500,000 Toman)
- **Total Monthly: $50 - $130** (2,500,000 - 6,500,000 Toman)

---

### Option B: Cloud GPU Rental (Monthly Subscription)

If you don't have personal hardware, you must rent a GPU server:

#### Recommended Services:

**1. RunPod.io**
- GPU: RTX 4090 (24GB VRAM)
- Cost: $0.39/hour
- 24/7 Usage: **$280/month** (14,000,000 Toman)
- 12 hours/day: **$140/month** (7,000,000 Toman)

**2. Vast.ai (Cheaper)**
- GPU: RTX 3090 (24GB VRAM)
- Cost: $0.25 - $0.35/hour
- 24/7 Usage: **$180 - $250/month** (9,000,000 - 12,500,000 Toman)
- 12 hours/day: **$90 - $125/month** (4,500,000 - 6,250,000 Toman)

**3. Lambda Labs**
- GPU: A10 (24GB VRAM)
- Cost: $0.60/hour
- 24/7 Usage: **$432/month** (21,600,000 Toman)
- 12 hours/day: **$216/month** (10,800,000 Toman)

**4. Google Cloud / AWS (More Expensive)**
- GPU: A100 (40GB)
- Cost: $1.5 - $3/hour
- 24/7 Usage: **$1,080 - $2,160/month** (54,000,000 - 108,000,000 Toman)

**Recommendation: Vast.ai for starting** - approx. **9,000,000 Toman/month** for 24/7 operation

---

### Option C: Serverless (Pay-per-use)

For low traffic (less than 1000 requests per day):

**1. Replicate.com**
- Voxtral Small: approx. $0.01 - $0.05 per minute of audio
- 1000 minutes audio/month: **$10 - $50/month** (500,000 - 2,500,000 Toman)

**2. Hugging Face Inference Endpoints**
- Cost: $0.60/hour (only when active)
- 100 hours/month: **$60/month** (3,000,000 Toman)

---

## 2. Software Requirements

### Free Software:

| Software | Purpose | Cost |
|----------|---------|------|
| Python 3.9+ | Programming language | **FREE** |
| PyTorch + CUDA | Machine learning framework | **FREE** |
| Transformers (Hugging Face) | Load models | **FREE** |
| Ollama | Local Dorna model execution | **FREE** |
| FFmpeg | Audio format conversion | **FREE** |
| python-telegram-bot | Telegram bot library | **FREE** |
| Git | Code management | **FREE** |

### Optional Software (for improvements):

| Software | Purpose | Cost |
|----------|---------|------|
| Docker | Containerize application | **FREE** |
| Nginx | Web server | **FREE** |
| PostgreSQL | Store logs | **FREE** |
| Redis | Cache results | **FREE** |

---

## 3. Model Download and Storage Costs

### Model Downloads (One-time):

| Model | Size | Download Cost |
|-------|------|---------------|
| Voxtral Small 24B | ~48GB | **FREE** (from Hugging Face) |
| Whisper Large-v3-Turbo | ~3GB | **FREE** (from Hugging Face) |
| Dorna (Ollama) | ~4-7GB | **FREE** (from Ollama) |

**Note:** Need high-speed internet for initial download (total ~55-60GB)

### Storage:
- Required space: Minimum **100GB** for models and temporary data
- Cost: Included in SSD price or cloud storage fees

---

## 4. Telegram Bot Costs

### Telegram API:
- **Completely FREE** - No user limit
- Need to register bot with BotFather (free)

### Bot Hosting:

**Option 1: Same GPU Server**
- Additional cost: **$0** (use same server)

**Option 2: Separate VPS (Recommended)**
- Simple server for Telegram bot (no GPU needed)
- Providers: DigitalOcean, Linode, Hetzner
- Specs: 2GB RAM, 1 CPU
- Cost: **$5 - $12/month** (250,000 - 600,000 Toman)

**Option 3: Free Service (Limited)**
- Heroku Free Tier (550 hours/month limit)
- Railway.app ($5 free credit)
- **Cost: $0 - $5/month**

---

## 5. Internet and Bandwidth Costs

### For Personal Server:
- Upload/Download: Minimum 50 Mbps
- Monthly traffic: ~500GB - 2TB (depends on user count)
- Cost in Iran: **1,000,000 - 5,000,000 Toman/month**

### For Cloud Server:
- Usually includes 1-5TB free traffic
- Additional traffic: $0.08 - $0.12 per GB
- Estimate: **Free to $20/month** additional

---

## 6. Optional Costs (for quality improvement)

| Service | Purpose | Monthly Cost |
|---------|---------|--------------|
| CDN (Cloudflare) | Faster audio download | **FREE - $20** |
| Monitoring (Grafana Cloud) | Server monitoring | **FREE - $50** |
| Backup Storage (S3/Backblaze) | Backups | **$5 - $20** |
| Domain Name | Custom domain | **$10 - $15/year** |
| SSL Certificate | Security (or free Let's Encrypt) | **FREE** |

---

## 7. Cost Summary - Different Scenarios

### Scenario 1: Buy Personal Server (Long-term recommendation)

**Initial Cost:**
- Hardware (RTX 3090): **100,000,000 - 165,000,000 Toman**

**Monthly Cost:**
- Electricity: 1,500,000 - 4,000,000 Toman
- Internet: 1,000,000 - 5,000,000 Toman
- VPS for Telegram bot: 250,000 - 600,000 Toman
- **Total: 2,750,000 - 9,600,000 Toman/month**

**Break-even point:** After 10-20 months of use

---

### Scenario 2: Full Cloud Server (No initial investment)

**Initial Cost:** **0 Toman**

**Monthly Cost:**
- Vast.ai GPU (24/7): 9,000,000 Toman
- or RunPod (12 hours/day): 7,000,000 Toman
- VPS for Telegram bot: 250,000 - 600,000 Toman
- Internet: 1,000,000 Toman
- **Total: 8,250,000 - 10,600,000 Toman/month**

---

### Scenario 3: Hybrid Solution (Recommended for starting)

**Phase 1 (Testing & Development):**
- Use Whisper instead of Voxtral (cheaper GPU)
- GPU: GTX 1050 Ti or RTX 3060 (12GB) - your current hardware
- Dorna on CPU (slow but acceptable)
- Cost: **0 Toman** (use existing hardware)

**Phase 2 (Production):**
- When you have users, migrate to Vast.ai
- Upgrade to Voxtral Small
- Pipeline optimization
- **Cost: 4,500,000 - 7,000,000 Toman/month**

**Phase 3 (Scaling - Month 5+):**
- Increase GPU hours or buy personal server
- Add new features
- **Cost: 7,000,000 - 15,000,000 Toman/month**

---

### Scenario 4: Minimum Cost (Serverless)

**For low users (<1000 requests/day):**

**Monthly Cost:**
- Replicate.com (500 minutes audio): 500,000 - 1,250,000 Toman
- VPS for Telegram bot: 250,000 Toman
- **Total: 750,000 - 1,500,000 Toman/month**

**Limitation:** Only suitable for low volume

---

## 8. Development Costs (One-time)

| Activity | Estimated Time | Cost (if hiring developer) |
|----------|---------------|----------------------------|
| Telegram bot development | 2-3 weeks | 20,000,000 - 40,000,000 Toman |
| Model integration | 1-2 weeks | 10,000,000 - 20,000,000 Toman |
| Testing & optimization | 1-2 weeks | 10,000,000 - 20,000,000 Toman |
| **Total (if you do it yourself)** | **4-7 weeks** | **FREE (only time)** |

---

## 9. Cost Estimates Based on User Count

### For 100 active users/day:
- Average audio: 2 minutes/user = 200 minutes/day
- Processing: ~6000 minutes/month
- **Cost: 750,000 - 1,500,000 Toman** (Serverless)

### For 1000 active users/day:
- Audio: 60,000 minutes/month
- **Cost: 7,000,000 - 9,000,000 Toman** (GPU Server)

### For 10,000 active users/day:
- Need multiple GPU servers
- **Cost: 25,000,000 - 40,000,000 Toman/month**

---

## 10. Final Recommendations by Budget

### Low Budget (under 2,000,000 Toman/month):
✅ Use **Whisper** instead of Voxtral Small
✅ Run Dorna on CPU
✅ Existing hardware (GTX 1050 Ti)
✅ Free or cheap Telegram bot hosting

### Medium Budget (5,000,000 - 10,000,000 Toman/month):
✅ Rent GPU from **Vast.ai** (12 hours/day)
✅ Use Voxtral Small + Dorna
✅ Separate VPS for Telegram bot

### High Budget (over 10,000,000 Toman/month):
✅ Rent GPU from RunPod or Lambda (24/7)
✅ Or buy personal RTX 4090 server
✅ Professional monitoring and backup services

---

## 11. Main Options Comparison Table

| Option | Initial Cost | Monthly Cost | Quality | Flexibility | Recommended For |
|--------|-------------|--------------|---------|-------------|-----------------|
| **Personal Hardware (RTX 3090)** | 100M Toman | 3-10M Toman | Excellent | Low | Long-term use |
| **Vast.ai (12h/day)** | 0 | 7M Toman | Excellent | High | Professional start |
| **Serverless** | 0 | 0.7-1.5M Toman | Good | High | Initial testing, low traffic |
| **Whisper Local** | 0 | 0.5-3M Toman | Good | Medium | **START HERE** |

---

## 12. Recommended Project Phases

### Phase 1: MVP with Minimum Cost (Months 1-2)
1. Use Whisper Large-v3-Turbo (free, local)
2. Install Ollama + Dorna (free)
3. Build simple Telegram bot
4. Test with 10-50 users
5. **Cost: 0 - 500,000 Toman/month**

### Phase 2: Quality Improvement (Months 3-4)
1. If users are satisfied, migrate to Voxtral Small
2. Rent GPU from Vast.ai (part-time)
3. Optimize pipeline
4. **Cost: 4,000,000 - 7,000,000 Toman/month**

### Phase 3: Scaling (Month 5+)
1. Increase GPU hours or buy personal server
2. Add new features
3. **Cost: 7,000,000 - 15,000,000 Toman/month**

---

## 13. Important Notes about Voxtral Small and Dorna

### Voxtral Small 24B Limitations:
⚠️ **Requires powerful GPU:** Minimum 24GB VRAM (RTX 3090/4090 or A6000)
⚠️ **Slow speed:** 5-20 seconds per minute of audio (depends on GPU)
⚠️ **High power consumption:** 300-500 watts during use
⚠️ **Requires high memory:** Minimum 64GB RAM for stability
⚠️ **CANNOT run on GTX 1050 Ti** (only has 4GB VRAM)

### Dorna Limitations:
⚠️ **CPU execution:** If no GPU, must run on CPU (10-30 seconds per sentence)
⚠️ **RAM requirement:** Minimum 16GB RAM for smooth operation
⚠️ **Correction quality:** May not always be 100% accurate
⚠️ **Requires Ollama:** Must install and configure Ollama

### Hidden Costs:
💰 **Bandwidth:** Downloading/uploading audio files - can be expensive with high traffic
💰 **Storage:** Storing audio files and logs - 10-50GB/month depending on users
💰 **Backup:** Data backups - $5-20/month
💰 **Maintenance:** Time spent on maintenance and bug fixes

---

## Final Conclusion

### ✅ Minimum Possible Cost (Recommended Start):
**Solution:** Whisper + Dorna on your existing hardware (GTX 1050 Ti)
- **Initial Cost:** 0 Toman
- **Monthly Cost:** 0 - 1,000,000 Toman (only VPS for Telegram bot)
- **Quality:** Good (70-85% accuracy)
- **Suitable for:** Testing MVP, 100-500 users

---

### 💎 Realistic Cost for Voxtral Small:
**Solution:** Rent GPU from Vast.ai (12 hours/day) + VPS
- **Initial Cost:** 0 Toman
- **Monthly Cost:** 7,000,000 - 10,000,000 Toman
- **Quality:** Excellent (85-95% accuracy)
- **Suitable for:** Professional use, 1000-5000 users

---

### 🚀 Long-term Investment:
**Solution:** Buy dedicated server with RTX 3090/4090
- **Initial Cost:** 100,000,000 - 165,000,000 Toman
- **Monthly Cost:** 3,000,000 - 10,000,000 Toman (electricity + internet + VPS)
- **Break-even:** 10-20 months
- **Quality:** Excellent
- **Suitable for:** Long-term business, 10,000+ users

---

## 🎯 My Final Recommendation:

**Phase 1 (Months 1-2):** Start with local Whisper - Cost: **0 Toman**
- Proof of Concept
- Gather user feedback
- Measure demand

**Phase 2 (Months 3-6):** If successful, rent Vast.ai - Cost: **7M Toman/month**
- High quality with Voxtral Small
- Better scalability
- Real market testing

**Phase 3 (Month 7+):** If profitable, buy personal server - Cost: **100M initial + 5M/month**
- Complete independence
- Long-term cost reduction
- Full control

---

## ⚡ CRITICAL NOTE:
**Your GTX 1050 Ti CANNOT run Voxtral Small 24B. It can only run Whisper or Voxtral Mini.**

**You MUST either:**
1. Start with Whisper (works on GTX 1050 Ti) - FREE
2. Rent cloud GPU for Voxtral Small - 7-10M Toman/month
3. Buy RTX 3090/4090 - 100-165M Toman initial investment
