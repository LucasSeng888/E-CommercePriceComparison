# Cross-Platform E-Commerce Price Tracking & Fluctuation Analysis System  
Tracking product prices from multiple e-commerce platforms with automated scraping, persistence, and reporting.

---

## 📌 1. Project Overview

### **Project Name**  
**Cross-Platform E-Commerce Price Tracking & Fluctuation Analysis System**

### **Project Objective**  
Build an automated system that scrapes the same product from at least three e-commerce platforms, compares the price differences, and tracks price fluctuations over time.

### **Primary Target Product**  
**Razer Viper V3 Pro Wireless Esports Gaming Mouse**

### **Platforms Tracked**
| Status | Platform | Notes |
|--------|----------|--------|
| ✅ Successful | Amazon, Lazada | Stable and reliable |
| ❌ Failed | Shopee, Temu, eBay | Strong anti-bot mechanisms, removed from tracking |

### **System Features**
- **Automated Data Scraping**  
  Extracts product name, price, and URL from Amazon and Lazada using Playwright.
- **Persistent Data Storage**  
  Saves price, timestamp, and platform into a local `price_history.csv`, forming a historical price database.
- **Run Summary Output**  
  Shows scraping success/failure counts and detailed results in the console.

### **System Architecture**
Script-based architecture optimized for I/O-heavy tasks (network requests & file operations).


---

## 📌 2. Planning Process

### **7-Day Development Timeline**

| Phase | Day | Focus | Result |
|-------|------|--------|---------|
| I. MVP | Day 1–2 | Environment setup, Playwright installation, Amazon scraping | Title & price extracted successfully |
| II. Dynamic Scraping | Day 3 | Add Lazada support; handle JS rendering & long loads | Lazada scraping works but less stable |
| III. Persistence | Day 4 | Implement CSV storage | All successful results stored |
| IV. Anti-Bot Challenges | Day 5 | Debug Shopee/Temu/eBay failures | Removed due to strong protection |
| V. Reporting | Day 6–7 | Code cleanup, integrate reporting | Final stable version complete |

### **MVP Definition**  
Successfully fetch Amazon product title & price and print to console.

### **Feature Prioritization**

| Priority | Feature | Reason |
|---------|----------|---------|
| ⭐ High | Playwright stable lifecycle | Prevents “Event loop is closed!” crash |
| ⭐ Medium | Lazada scraping | Tests performance on dynamic JS sites |
| ⭐ Medium | CSV data persistence | Required for price comparison |
| Low | Scheduled daily scraping | Non-core feature |
| Low | Visualization/charts | Planned after data stabilizes |

---

## 📌 3. System Design

### **Handling Platform Differences**  
Design follows **configuration-driven architecture**:
- All platform-specific details stored in `config.py`
- Scraper uses generic Playwright logic
- Cleaner separation, easier maintenance

### **Dynamic Content Strategies**
- **Amazon** → `wait_until="domcontentloaded"`  
- **Lazada** → `wait_until="networkidle"` with timeout up to 150s  
  (Handles heavy JS rendering)

### **Anti-Bot Mitigation**
1. **Error handling with try/except**
2. **Lifecycle control using try/finally**
3. **User behavior simulation**  
   - Page scrolling  
   - Mouse hover  
4. **Content validation**  
   - Use `aria-label` for hidden price spans (Temu technique)

### **Data Storage**
- Stored as dictionaries
- Written using Python’s built-in `csv` module
- Lightweight and easy for later analysis (with Pandas)

---

## 📌 4. Tech Stack

| Category | Technology | Reason |
|----------|------------|--------|
| Language | Python 3.x | Mature ecosystem, strong tooling |
| Scraping Framework | Playwright (Sync API) | Faster and more reliable than Selenium |
| Data Handling | CSV + Pandas | Simple persistence + future analytics |
| Scheduling (Optional) | schedule | Easy daily automation |

### **Why not other tools?**
- **Requests/BeautifulSoup** → Cannot execute JavaScript  
- **Scrapy** → Unnecessary complexity for JS-heavy e-commerce sites  
- **Selenium** → Slower, heavier, less efficient than Playwright  
- **Databases** → CSV is sufficient for MVP  

---

## 📌 5. Development Challenges & Solutions

### **Major Error:**
### ❌ `Event loop is closed! Is Playwright already stopped?`
**Cause:** Browser lifecycle was incorrectly terminated.  
**Solution:** Ensure `browser.close()` runs inside `finally` and outside the Playwright context block.

---

### **Hardest Difficulty: Anti-Bot Mechanisms**
- **Lazada** → Solved via scrolling + hover + network idle
- **Temu** → Solved via reading hidden `aria-label` attributes  
- **Shopee / eBay** → Hard-blocked by IP/fingerprint → Removed

---

### **Validation**
- Run multiple repeated scrapes → No lifecycle errors
- Validate data not null and matches website values
- Observed hidden price attributes using headful mode

---

## 📌 6. Testing

### **Testing Method**
Full integration testing via `main.py` + unit tests for key functions.

### **Test Cases**
| # | Input | Expected Output | Result |
|----|--------|------------------|---------|
| 1 | Amazon scraping | Price saved to CSV | ✅ |
| 2 | Lazada scraping | Price saved to CSV | ✅ |
| 3 | Invalid URL | Handled error gracefully | ✅ |
| 4 | `clean_price("RM1,299.50")` | `1299.50` | ✅ |
| 5 | Shopee scraping | Returns `None`, continues | ✅ |

---

## 📌 7. How to Run

### **Requirements**
- Windows / macOS / Linux  
- Python 3.8+  
- Playwright + Chromium

### **1. Create Virtual Environment**
```bash
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

2. Install Dependencies
pip install playwright pandas jinja2 schedule

3. Install Playwright Browsers
playwright install chromium

4. Run
python main.py

📌 8. What I Learned
Area	Key Learning
Playwright	Browser lifecycle, avoiding event loop errors
Anti-Bot	DOM obfuscation, JS rendering, hidden attributes
Hidden Data Extraction	Using aria-label to bypass obfuscated elements
Architecture	Config-driven design for cleaner scalability
📌 9. Future Improvements
Performance

Switch to async Playwright

Block images/CSS/fonts to speed up scraping

Architecture

Move from CSV → SQLite/PostgreSQL

Build REST API using Flask/FastAPI

Stability

Integrate rotating proxy pool

Use headful persistent context for heavy anti-bot sites

New Features

Automatic currency conversion

Price fluctuation charts

AI-generated buying recommendation summary

Next Step

Implement currency conversion API to normalize Amazon (USD) and Lazada (MYR) prices.

📌 Author

Your Name
Cross-platform price tracking system for academic/portfolio use.




