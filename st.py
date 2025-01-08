import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to initialize WebDriver
def initialize_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (remove if you need UI)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver

# Main automation workflow
def main_workflow():
    driver = initialize_webdriver()

    try:
        # Open login page
        driver.get("https://esgbeta.samcorporate.com/auth/login")
        print("Page loaded.")

        # Log in
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        email_input.send_keys("your_email@example.com")  # Replace with your email
        password_input.send_keys("your_password")  # Replace with your password
        submit_button.click()
        print("Login submitted.")

        # Wait for dashboard or page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "dashboard"))
        )
        print("Dashboard loaded successfully.")

        # Navigate to the required page and interact with elements
        file_month_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fileMonth"))
        )
        ActionChains(driver).move_to_element(file_month_dropdown).perform()
        file_month_dropdown.click()

        # Select a value in the dropdown (e.g., "January")
        january_option = driver.find_element(By.XPATH, "//option[text()='January']")
        january_option.click()
        print("Dropdown value selected.")

        # File upload
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys("/path/to/your/file.xlsx")  # Replace with your file path
        print("File uploaded.")

        # Submit the form
        upload_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        upload_button.click()
        print("Form submitted.")

        # Wait for the upload to complete and verify success
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "upload-success"))
        )
        print("File uploaded successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the driver
        driver.quit()

# Streamlit integration
st.title("Selenium Automation")
if st.button("Run Automation"):
    st.write("Running automation workflow...")
    main_workflow()
    st.write("Automation workflow completed.")
