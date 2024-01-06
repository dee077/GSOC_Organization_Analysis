# Google Summer of Code (GSoC) Analysis

The Google Summer of Code is a prestigious program that connects students with open-source organizations, offering them the opportunity to contribute to real-world projects during the summer. Selecting the right organization is crucial for maximizing the chances of being accepted into the program.

## Introduction

This project is designed to scrape and analyze data from the Google Summer of Code (GSoC) official website, specifically focusing on past archive data. The goal is to provide insights into the organizations' selection process and assist potential applicants in making informed choices.

This project aims to streamline the organization selection process by analyzing past GSoC data. By extracting and presenting relevant information, I hope to empower potential applicants with valuable insights into each organization's focus, technologies used, and the number of selected students.

Utilizing web scraping tools such as Selenium for automation and BeautifulSoup for HTML parsing, this project extracts valuable data from the GSoC official website. By harnessing the power of these tools, we aim to provide a seamless and efficient analysis of past GSoC data.


## Features

- Scrape and analyze GSoC data from the official archive.
- Provide statistics on the number of selected students for each organization.
- Present information on the technologies and topics each organization focuses on.
- **Web Scraping with Selenium:** Automates the data extraction process from the GSoC official website.
- HTML Parsing with BeautifulSoup: Parses the HTML content for structured data extraction.
- Statistics on Selected Students: Provides insights into the number of selected students for each organization.
- Focus on Technologies and Topics: Presents information on the technologies and topics each organization focuses on.

## Setup

Provide step-by-step instructions on how to set up the project. Include any necessary prerequisites and configuration steps.

1. **Clone the repository:**
   
   ```bash
   git clone https://github.com/dee077/GSOC_Organization_Analysis.git
   cd GSOC_Organization_Analysis
   ```

2. **Create and Activate Virtual Environment:**

    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Setup Selenium:**
    
    Download the appropriate ChromeDriver executable for your operating system from    
    https://sites.google.com/chromium.org/driver/. Place the downloaded chromedriver.exe inside the 
    `chromedriver-win64/` folder in the project directory.

5. **Run the Script:**

    ```bash
    python main.py
    ```
    After running this script, the application will scrape and analyze GSoC data. Check the generated CSV files in 
    the `data/` directory for detailed information on each organization.
    
    You can see the list of orginization along with the number of selected students in your terminal as well.
    ![terminal_output](images/ss.png)

## Additional Details

