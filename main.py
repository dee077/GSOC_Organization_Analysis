import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
# from scripts.write_in_exel import write_data_to_excel
# from scripts.fetch_ideas import fetch_project_ideas_and_count

YEAR = 2024
LINUX_PATH = '/home/deepanshu/.local/bin/chromedriver'
# URL = f'https://summerofcode.withgoogle.com/archive/{YEAR}/organizations/'
URL = 'https://summerofcode.withgoogle.com/programs/2025/organizations'

def setup_driver():
    """
    Set up and configure the Chrome WebDriver.
    """
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1200,800')
    chrome_service = ChromeService(executable_path=LINUX_PATH)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver

def open_page(driver, url):
    """
    Open a URL in the browser and wait for the page to load.
    """
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'org-wrapper')))

def extract_org_data(driver):
    """
    Extract organization data from the current page and return a list of organizations' details.
    """
    org_data = []
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    
    organizations_info = soup.find_all('div', class_='org-wrapper')
    for org_info in organizations_info:
        org_name = org_info.find('div', class_='name').text.strip()
        org_link = org_info.find('a')['href']
        org_url = f'https://summerofcode.withgoogle.com{org_link}'
        image_url = org_info.find("img")['src']
        org_description = org_info.find("div", class_='short-description').text.strip()
        print(f"Extracting data for: {org_name}")
        print(f"Description: {org_description}")
        print(f"URL: {org_url}")
        print(f"Image URL: {image_url}")

        # Extract organization details in a new window
        org_details = extract_org_details(driver, org_url)
        full_data = {
            "name": org_name,
            "image_url": image_url,
            "image_background_color": "#ffffff",
            "description": org_description,
            "url": org_details['url'],
            "category": '',
            "projects_url": org_url,
            "ideas_url": org_details['ideas_url'],
            "guide_url": org_details['guide_url'],
            "topics": org_details['topics'],
            "technologies": org_details['technologies'],
            "irc_channel": org_details['irc_channel'],
            "contact_email": org_details['contact_email'],
            "mailing_list": org_details['mailing_list'],
            "twitter_url": org_details['twitter_url'],
            "blog_url": org_details['blog_url'],
            "facebook_url": org_details['facebook_url'],
            "num_projects": org_details['num_projects'],
            "projects": org_details['projects']
        }
        org_data.append(full_data)

        print(full_data)
        print("-" * 40)
        
    return org_data

def extract_org_details(driver, org_url):
    """
    Extract detailed information about a specific organization by opening a new tab.
    """
    # Open the organization link in a new tab
    driver.execute_script(f"window.open('{org_url}', '_blank');")
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'section')))
    
    # Extract required details
    try: 
        technologies = driver.find_element(By.CLASS_NAME, 'tech__content').text.strip()
        topics = driver.find_element(By.CLASS_NAME, 'topics__content').text.strip()
        url = driver.find_element(By.CSS_SELECTOR, "div.link__wrapper a").get_attribute("href")
        ideas_url = driver.find_element(By.CSS_SELECTOR, "div.ng-star-inserted a").get_attribute("href")
        guide_url = driver.find_element(By.CSS_SELECTOR, "div.link-wrapper.ng-star-inserted a").get_attribute("href")
    except:
        technologies = ''
        topics = ''
        url = ''
        ideas_url = ''
        guide_url = ''
    links = driver.find_elements(By.CSS_SELECTOR, "ul li.ng-star-inserted a")
    irc_channel = ''
    contact_email = ''
    mailing_list = ''
    twitter_url = ''
    blog_url = ''
    facebook_url = ''
    for link in links:
        url = link.get_attribute("href")
        text = link.text.strip().lower()
        if "chat" in text and not irc_channel:
           irc_channel = url
        elif "email" in text and not contact_email:
           contact_email = url
        elif "mailing" in text or "forum" in text and not mailing_list:
           mailing_list = url
        elif "x" in text and not twitter_url:
           twitter_url = url
        elif "blog" in text and not blog_url:
            blog_url = url
        elif "facebook" in text and not facebook_url:
           facebook_url = url 
    num_projects = 0
    projects = []

    # Close the new tab and switch back to the main window
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return {
        'technologies': technologies,
        'topics': topics,
        'url': url,
        'ideas_url': ideas_url,
        'guide_url': guide_url,
        'irc_channel': irc_channel,
        'contact_email': contact_email,
        'mailing_list': mailing_list,
        'twitter_url': twitter_url,
        'blog_url': blog_url,
        'facebook_url': facebook_url,
        'num_projects': num_projects,
        'projects': projects
    }

def update_categories(driver ,all_org_data):
    open_page(driver, URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "mat-chip-option button"))
    )
    categories_container = driver.find_element(By.CLASS_NAME, "mdc-evolution-chip-set__chips")
    categories = categories_container.find_elements(By.TAG_NAME, "mat-chip-option")
    for category in categories:
        button = category.find_element(By.TAG_NAME, "button")
        driver.execute_script("arguments[0].click();", button)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')     
        organizations_info = soup.find_all('div', class_='org-wrapper')
        for org_info in organizations_info:
            org_name = org_info.find('div', class_='name').text.strip()
            for org in all_org_data:
                if org['name'] == org_name:
                    org['category'] = category.text.strip()
                    break


def navigate_to_next_page(driver):
    """
    Navigate to the next page in the pagination.
    """
    try:
        pagination_next_button = driver.find_element(By.CLASS_NAME, 'mat-mdc-paginator-navigation-next')
        if pagination_next_button.is_enabled():
            driver.execute_script("arguments[0].click();", pagination_next_button)
            return True
        return False
    except Exception as e:
        print(f"Error navigating to the next page: {e}")
        return False

def main():
    """
    Main function to control the flow of data extraction and CSV writing.
    """
    driver = setup_driver()

    try:
        open_page(driver, URL)
        
        all_org_data = []

        # First extraction from the current page
        org_data = extract_org_data(driver)
        all_org_data.extend(org_data)

        # Navigate through pagination and collect data from all pages
        while navigate_to_next_page(driver):
            time.sleep(2)  # Wait a bit before extracting data from the new page
            org_data = extract_org_data(driver)
            all_org_data.extend(org_data)

        update_categories(driver, all_org_data)

        with open("data/2025.json", "w", encoding="utf-8") as json_file:
            json.dump(all_org_data, json_file, indent=4, ensure_ascii=False)
        
        print("Data successfully saved to 2025.json")

    finally:
        driver.quit()  # Ensure the driver is closed after execution

if __name__ == "__main__":
    main()
