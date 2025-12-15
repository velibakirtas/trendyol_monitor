# Trendyol Price Monitor & Analyzer

Trendyol Price Monitor is a high-performance web scraping tool designed to overcome dynamic and static content challenges on e-commerce sites (starting with Trendyol), utilizing Hybrid Architecture.
This project collects data by combining the speed of Scrapy and the power of Playwright with modern web technologies (React/Vue-based SPA), cleans it, and stores it in a database with a history.

![Python Version](https://img.shields.io/badge/python-3.11.9-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🏗️ Architectural and Technical Approach
The project combines two different engines on a single spider for situations where traditional scraping methods fall short:
### 1. Renderer Mode (Playwright - Browser Rendering)
* **Issue:** Listing pages use “Infinite Scrolling” and products are loaded later using JavaScript.
* **Solution:** With the scrapy-playwright integration, the listing page opens in a real Chromium browser. Automatic scrolling ensures that all products are loaded into the DOM.

### 2. Requests Mode (Scrapy - Native Requests)
* **Issue:** Opening a browser for each product detail increases CPU/RAM costs and slows down the process.
* **Solution:** Requests are sent directly to the links collected from the list using Scrapy's Request object without opening a browser. This speeds up the process by 10x-20x.

### 3. JSON Parsing
* **Method:** Instead of parsing the fragile HTML structure (CSS/XPath Selectors) on detail pages, the Initial State JSON data (window.__envoy__PROPS) embedded in the page's source code is targeted.
* **Technique:** Using Regex (Regular Expressions), this JSON block is extracted from the script tags and converted into a Python dictionary. This way, the bot continues to work even if the HTML design changes.

---

## ✨ Key Features

### 🔄 Asynchronous Architecture
* Non-blocking data flow using asyncio and Twisted reactors.
### 🛡️ Bypassing Bot Protection
**Note:** *The actions taken in this regard are minimal interventions to avoid pushing ethical boundaries.*<br>
* Automatic User-Agent Rotation (It has not been implemented yet. It will be included in the next release.)
* Hiding automation-controlled flags on Playwright.
### 💾 Smart Database (UPSERT) 
* Using the product URL as the PRIMARY KEY in SQLite; if the product exists, it updates the price/stock, otherwise it creates a new record (duplicate prevention).
### 🪟 Windows Compatibility 
* Configuration that prevents SelectorEventLoop conflicts in Windows operating systems.
### 🛡️ Defensive Coding:
* Safe navigation (.get chain) and error handling for empty incoming data or changing API responses.
* *Note:Since the project is still in draft form, this discipline has not been applied throughout the entire project.* 

---

## 🛠️ Installation

**Note:** This project was developed using ![Python Version](https://img.shields.io/badge/python-3.11.9-blue). For best compatibility, it is recommended to use Python 3.11+ versions.
1. Clone the repo
```bash
git clone https://github.com/velibakirtas/trendyol_monitor
cd trendyol_monitor
```
2. Set up the virtual environment
```bash
python -m venv venv
# for Windows users
venv\Scripts\activate

# for macOS and Linux users
source venv/bin/activate
```
3. Install the requirements
```bash
pip install -r requirements.txt
```
4. Install playwright browsers
```bash
playwright install

# The project is based on Chromium. If you prefer, you can choose to install only Chromium.
playwright install chromium
```
---

## 🚀 Usage
To start the spider, run the following command from the terminal:
```bash
scrapy crawl trendyol_spider
```
To avoid mistakes, check and paste the target URL asked for at the terminal.
<br><br>
**Process**
* The Chromium browser opens and goes to the category you are looking for.
* The page automatically scrolls down
* Product links are collected and the browser closes.
* The price and stock information of the products collected at the terminal flows.
* The results are saved to the trendyol.db file.
---
## 📊 Data Structure
The following columns are found in the products table in the trendyol.db SQLite database:


| **Column**      | **Type**   | **Description**            |
| -------------- | --------- | ----------------------- |
| `url`          | TEXT (PK) | The product's unique link. |
| `title`        | TEXT      | Product title.           |
| `price`        | REAL      | Selling price.           |
| `stock_status` | BOOLEAN   | Is it in stock? (1/0)    |
| `last_updated` | TEXT      | Last inspection date.     |

**Note:** The trendyol.db file in the folder is a sample output file. You can delete it before running the spider. It will be recreated by the program.

---

## 📁 Project Structure
```text
trendyol_monitor/
├── scrapy.cfg            # Deploy configuration file
├── requirements.txt      # Project dependencies
├── trendyol.db           # SQLite Database (Auto-generated)
└── trendyol_monitor/     # Project module
    ├── items.py          # Project items definition
    ├── middlewares.py    # Project middlewares
    ├── pipelines.py      # Pipelines for DB operations
    ├── settings.py       # Project settings
    └── spiders/
        └── trendyol_spider.py  # The main spider
```

---
## ⚖️ Legal Disclaimer
This project has been developed solely for educational and portfolio purposes. Please respect Trendyol's `robots.txt` file and terms of use. It is recommended that you obtain permission from the relevant platform before using it for commercial purposes.

---
## 👨‍💻 Contact
For questions, suggestions, and complaints: [Send an Email](mailto:velibakirts@gmail.com)