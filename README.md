# Emirates Line Web Scraper & Data Processor 🚢📊

## 📌 Overview

This Python project automates the extraction of demurrage and detention tariffs from the [Emirates Line](https://www.emiratesline.com) website and processes the downloaded Excel files using AI to create structured CSV files.

---

### 🧠 Key Features

-  **Headless Web Scraping** with Selenium
-  Loops through **all countries and ports**
-  **Automated Excel Downloads** named by Country-Port
-  **Session Recovery** to prevent browser crashes
-  **Error Handling** for missing data or UI failures
-  **AI-based Excel Processing** with Gemini
-  Generates individual CSVs and a combined `final.csv`

---

## 🗂️ Folder Structure
```bash
├── main-code/             # Main scraper and processing scripts (including downloaded Excel and processed CSV files)
├── Base-code/             # Jupyter notebooks for initial testing
└── Final/                 # Final combined CSV output
```
---

### 🗝️ Set Up API Key

- Create a .env file with your Gemini API key:
- GOOGLE_API_KEY=your_api_key_here

---

### ⚙️ Workflow
## 1️⃣ Web Scraping 

- Launches Chrome in headless mode
- Loops through all countries and ports
- Downloads Excel files into Data/
- Resets the browser session every 3 countries to avoid crashes

## 2️⃣ Data Processing 

- Reads Excel files from Excel-files/
- Converts them to Markdown
- Parses using Gemini AI to structured JSON
- Saves individual CSVs to CSV-files/
- Combines into a single final.csv

---
## 🌐 Web App – AI-powered CSV Agent
We’ve built an interactive web app using LangChain that allows users to query the final CSV data using natural language.

🔗 Try it here: emirates-line-tariff-scraper-ai.streamlit.app


---

## 📌 Final Notes
This project automates a normally tedious and error-prone process in the shipping industry using Python, Selenium, and Generative AI. It's reliable, extensible, and production-ready.
