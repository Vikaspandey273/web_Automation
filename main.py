from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import URL, USERNAME, PASSWORD
from db import get_connection
import time

# Start browser
driver = webdriver.Edge()
driver.get(URL)
driver.maximize_window()

try:
    # Login
    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "loginBtn").click()

    # Wait for dashboard
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "dashboard")))

    # Extract table data
    rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
    extracted_data = []

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        name = cols[0].text
        value = cols[1].text
        extracted_data.append((name, value))

    # Insert into MySQL
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO report_data (name, value) VALUES (%s, %s)"
    cursor.executemany(query, extracted_data)

    conn.commit()
    conn.close()

    print("Data inserted successfully")

except Exception as e:
    print("Error occurred:", e)

finally:
    time.sleep(20)
    driver.quit()