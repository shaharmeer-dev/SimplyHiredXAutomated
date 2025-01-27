# SimplyHired Job Scraper

This project is a Python-based web scraping tool designed to extract job listings from SimplyHired.com. It uses Selenium WebDriver and related libraries to automate browser interactions, filter job listings based on specific criteria, and save the collected data into a CSV file for further analysis.

## Features

- Automated browser interaction using Selenium.
- Supports undetected ChromeDriver to bypass bot detection.
- Extracts job details including:
  - Job link
  - Job description
  - Job type
  - Compensation
  - Posted time
  - Qualifications
- Filters job listings based on specified titles and location (`Remote` in this case).
- Pagination handling to scrape multiple pages of job listings.
- Saves scraped data to a CSV file.

## Prerequisites

Before running the script, ensure the following tools and libraries are installed:

1. **Python 3.7+**
2. Python libraries:
   - `selenium`
   - `pandas`
   - `webdriver_manager`
   - `undetected_chromedriver`
   - `pyyaml`
   - Other dependencies (install using `requirements.txt` provided)

## Installation

1. Clone the repository or download the script.
2. Install the required dependencies by running:

   ```bash
   pip install -r requirements.txt
