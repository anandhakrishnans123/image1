import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Selenium Grid or BrowserStack Configuration
SELENIUM_GRID_URL = "http://your-selenium-grid-url:4444/wd/hub"  # Replace with your Selenium Grid URL
BROWSERSTACK_USER = "your_username"  # For BrowserStack
BROWSERSTACK_KEY = "your_access_key"  # For BrowserStack

def initialize_webdriver():
    """
    Initializes the WebDriver to connect to a remote Selenium Grid or cloud service.
    """
    # For BrowserStack or Sauce Labs, use custom capabilities
    capabilities = {
        "browserName": "chrome",
        "browserVersion": "latest",
        "platformName": "Windows 10",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "local": "false",
            "seleniumVersion": "4.0.0"
        }
    }

    # For Selenium Grid, use simpler capabilities
    # capabilities = DesiredCapabilities.CHROME

    driver = webdriver.Remote(
        command_executor=SELENIUM_GRID_URL,
        desired_capabilities=capabilities
    )
    return driver


def main_workflow():
    """
    Main workflow function to perform browser automation tasks.
    """
    st.title("Automated Selenium Workflow on Streamlit")
    
    st.write("Initializing WebDriver...")
    driver = initialize_webdriver()

    try:
        # Example: Open Google and perform a search
        st.write("Navigating to Google...")
        driver.get("https://www.google.com")

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys("Streamlit Selenium Integration" + Keys.RETURN)

        st.write("Performing search...")

        # Wait for results and fetch titles
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3"))
        )
        for result in results[:5]:
            st.write(result.text)
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        driver.quit()
        st.write("WebDriver session ended.")


# Streamlit app entry point
if __name__ == "__main__":
    main_workflow()
