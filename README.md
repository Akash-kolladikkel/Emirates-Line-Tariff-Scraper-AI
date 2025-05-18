# Emirates Line Web Scraper & Data Processor 🚢📊

## 📌 Overview

This Python project automates the extraction of demurrage tariffs from the [Emirates Line](https://www.emiratesline.com) website and processes the downloaded Excel files using AI to create structured CSV files.
It includes a headless web scraper, an AI-powered data processor using Gemini, and an interactive Streamlit web app powered by LangChain for querying the final dataset.

---

## 🌐 Web App – AI-powered CSV Agent
I've developed an interactive web application using LangChain that allows users to query the final CSV dataset using natural language, the app is deployed on Streamlit Cloud

🔗 Try it here: [*Web App*](https://emirates-line-tariff-scraper-ai.streamlit.app/)
![ss1](https://github.com/Akash-kolladikkel/Emirates-Line-Tariff-Scraper-AI/blob/d713ee02d8bc3074b9510189310131c3995ad168/ESL-AI.png)

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
├── src/                   # Streamlit Webapp code
└── Final.csv              # Final combined CSV output
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
- Downloads Excel files into `Data/`
- Resets the browser session every 3 countries to avoid crashes

## 2️⃣ Data Processing 

- Reads Excel files from `Excel-files/`
- Uses `gemini-2.0-flash` model to parse Excel into structured Markdown → JSON
- Saves individual CSVs to `CSV-files/`
- Combines into a single `final.csv`

## 3️⃣ LangChain CSV Agent Web App

- Built a LangChain CSV agent to query `final.csv` using natural language.
- Uses a Pandas DataFrame agent with Python code execution under the hood.
- Adapted the agent from OpenAI to support Gemini with custom prompts and parameters.
- Designed a custom prompt template for domain-specific understanding.

---

## 📌 Final Notes
This project automates a normally tedious and error-prone process in the shipping industry using Python, Selenium, and Generative AI. It's reliable, extensible, and production-ready.
