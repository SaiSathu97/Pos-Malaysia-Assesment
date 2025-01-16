from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Use webdriver_manager to automatically manage and download the driver
service = Service(ChromeDriverManager().install())

# Initialize WebDriver with the service object
driver = webdriver.Chrome(service=service)

# Open a website
driver.get("https://www.google.com")

# Find the search box using its name attribute and print its placeholder text
search_box = driver.find_element(By.NAME, "q")
print("Search box placeholder text:", search_box.get_attribute("placeholder"))

# Close the browser
driver.quit()
