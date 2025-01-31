# Book Scraper 📚🕷️

**Book Scraper** is a web scraping application built using Scrapy to extract book details from [Books to Scrape](https://books.toscrape.com). The spider navigates through multiple pages and gathers essential information about each book, including:

- 📌 **Title**
- 📌 **Category**
- 📌 **Description**
- 📌 **Price (Excl. & Incl. Tax)**
- 📌 **Stock availability**
- 📌 **Product type**
- 📌 **Number of reviews**
- 📌 **Star rating**
- 📌 **Book URL**

The scraped data can be stored in various formats like JSON, CSV, or a database, making it useful for data analysis, price comparison, or cataloging books.

## 🚀 How It Works
1. The spider starts at the homepage and extracts book links.
2. It follows each book's link to collect detailed information.
3. The scraper also handles pagination to ensure all books are extracted.

## 🛠️ Setup & Usage
1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd <repo_name>
