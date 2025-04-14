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

### 🗝️ Set Up API Key

- Create a .env file with your Gemini API key:
- GOOGLE_API_KEY=your_api_key_here

---

### ⚙️ Workflow
## 1️⃣ Web Scraping (emirates_scraper.py)

- Launches headless Chrome
- Loops through all countries and ports
- Downloads Excel files into Data/
- Handles browser crashes every 3 countries

## 2️⃣ Data Processing (Data_processing.py)

- Reads Excel files from Excel-files/
- Uses Gemini AI to parse to structured format
- Saves individual CSVs to CSV-files/
- Combines into a single final.csv

---


