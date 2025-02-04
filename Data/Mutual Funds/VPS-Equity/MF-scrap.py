from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import pandas as pd

# Path to your WebDriver
driver_path = "E:\\Final Semester\\FYP\\Data\\Scraping\\Mutual Funds\\chromedriver.exe"

# Chrome options
options = Options()
options.add_argument("--disable-gpu")  # Suppress GPU errors
options.add_argument("--ignore-certificate-errors")  # Suppress SSL errors

# Initialize the WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# URL of the page
# url = "https://sarmaaya.pk/mutual-funds/fund/19d82c95-ad27-4b51-bb1d-a2790f22d9eb" # Atlas APFE
# url = "https://sarmaaya.pk/mutual-funds/fund/588f65fb-69cf-44b2-a7ad-5a186dc7effa" # Pakistan Pension PPFE
# url = "https://sarmaaya.pk/mutual-funds/fund/0c35e4f0-835f-481d-a01b-e625227c2f25" # UBL Pension Fund
# url = "https://sarmaaya.pk/mutual-funds/fund/31c18202-70f8-4a33-888e-9d6c7ec76916" # Al Habib AHPF-E
url = "https://sarmaaya.pk/mutual-funds/fund/edde3f8c-0be6-4277-a8e6-c20d59e8beb9" # Al-Falah FPFE

driver.get(url)

# Wait for the page and the "All" tab to load
wait = WebDriverWait(driver, 15)
try:
    # Wait for the "All" tab to be clickable
    all_tab = wait.until(EC.element_to_be_clickable((By.ID, "nav-all-tab")))
    # all_tab = wait.until(EC.element_to_be_clickable((By.ID, "nav-20y-tab")))
    all_tab.click()
    print("Selected the 'All' tab successfully.")

    # Wait for the graph data to update (adjust condition based on the page's behavior)
    WebDriverWait(driver, 10).until(
        lambda d: "active" in d.find_element(By.ID, "nav-all-tab").get_attribute("class")
        # lambda d: "active" in d.find_element(By.ID, "nav-20y-tab").get_attribute("class")
        # lambda d: "active" in d.find_element(By.ID, "nav-20y-tab").get_attribute("class")
    )
    print("Graph data for 'All' loaded.")
except Exception as e:
    print(f"Failed to select the 'All' tab: {e}")
    driver.quit()
    exit()

# Extract the JavaScript variable after clicking "All"
try:
    # Wait for the data to update in the JavaScript variable
    driver.implicitly_wait(5)
    script_content = driver.execute_script("return jsonfile;")  # Assuming `jsonfile` contains the updated data
    print("JavaScript variable fetched.")
except Exception as e:
    print(f"Error while executing JavaScript: {e}")
    script_content = None

# Close the WebDriver
driver.quit()

# Parse the JSON content
if script_content and "data" in script_content:
    data = script_content["data"]
    # Convert to a DataFrame
    df = pd.DataFrame(data)

    # Save to CSV
    csv_path = "graph_data.csv"
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")
else:
    print("Data not found in the extracted JavaScript.")
