from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from scripts.write_in_csv import write_data_to_csv

year=2024

# Set up the Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--start-maximized')

chrome_service = ChromeService(executable_path='chromedriver-win64/chromedriver.exe')  # Update the relative path
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# GSoC ke official website ka URL
url = f'https://summerofcode.withgoogle.com/programs/2024/organizations'

# Open the URL in the browser
driver.get(url)

# Wait for the dynamic content to be fully loaded (increase the timeout if needed)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'org-wrapper')))

i=1
org_data = [] 

def extract_info_from_current_page():
    
    global i
    # Get the HTML content after dynamic content is loaded
    html_content = driver.page_source

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Continue with your scraping logic using BeautifulSoup
    organizations_info = soup.find_all('div', class_='org-wrapper')
    for org_info in organizations_info:

        # Extracting name of organization
        org_name = org_info.find('div', class_='name').text.strip()

        # Click on the organization div to open a new window
        org_link = org_info.find('a')['href']
        org_url = f'https://summerofcode.withgoogle.com{org_link}'
        driver.execute_script(f"window.open('{org_url}', '_blank');")

        # Wait for the new window to open
        wait = WebDriverWait(driver, 10)
        wait.until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[1])

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'section')))
        selected_students = len(driver.find_elements(By.CLASS_NAME, 'project-card-wrapper'))
        # Extracting technologies
        selected_students='Na'
        technologies = driver.find_element(By.CLASS_NAME, 'tech__content').text.strip()

        # Extracting topics
        topics = driver.find_element(By.CLASS_NAME, 'topics__content').text.strip()
        
        # Close new window
        driver.close()

        driver.switch_to.window(driver.window_handles[0])

        print(i, org_name, selected_students)
        i=i+1
        org_data.append({'Organization': org_name, 'Technologies':technologies, 'Topics':topics, 'Selected_Students': selected_students})

# Initial extraction from the first page
extract_info_from_current_page()

# # Navigate through pagination
pagination_next_button = driver.find_element(By.CLASS_NAME, 'mat-paginator-navigation-next')

while pagination_next_button.is_enabled():
    driver.execute_script("arguments[0].click();", pagination_next_button)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'org-wrapper')))
    extract_info_from_current_page()

# Close the browser
driver.quit()

write_data_to_csv(year, org_data)


