# Emirates Line Web Scraper & Data Processor 🚢📊

## 📌 Overview

This Python project automates the extraction of demurrage and detention tariffs from the [Emirates Line](https://www.emiratesline.com) website and processes the downloaded Excel files using AI to create structured CSV files.

---

### 🧠 Key Features

- ✅ **Headless Web Scraping** with Selenium
- 🌍 Loops through **all countries and ports**
- 📥 **Automated Excel Downloads** named by Country-Port
- 🔁 **Session Recovery** to prevent browser crashes
- ⚠️ **Error Handling** for missing data or UI failures
- 🤖 **AI-based Excel Processing** with Gemini
- 📊 Generates individual CSVs and a combined `final.csv`

---

## 🛠️ Setup & Requirements

### 🔗 Prerequisites

- Python 3.8+
- Google Chrome + Matching ChromeDriver

### 📦 Install Python Dependencies

```bash
pip install -r requirements.txt

