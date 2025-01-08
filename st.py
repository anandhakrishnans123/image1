import streamlit as st
import asyncio
from playwright.async_api import async_playwright
import time

# Helper function to verify and click a button
async def verify_and_click_button(page, button_selector, screenshot_path=None):
    try:
        await page.wait_for_selector(button_selector, timeout=30000)
        print(f"Button '{button_selector}' is visible.")
        await page.click(button_selector)
        print(f"Clicked the button: {button_selector}.")
    except Exception as e:
        print(f"Error verifying or clicking button '{button_selector}': {e}")
        if screenshot_path:
            await page.screenshot(path=screenshot_path)

# Helper function to select an option from a dropdown
async def select_and_verify_dropdown(page, dropdown_selector, option_value):
    try:
        await page.wait_for_selector(dropdown_selector, timeout=30000)
        print(f"Dropdown {dropdown_selector} is visible.")
        await page.select_option(dropdown_selector, value=option_value)
        print(f"Selected option {option_value} from the dropdown.")
    except Exception as e:
        print(f"Error selecting dropdown: {e}")
        await page.screenshot(path=f"{dropdown_selector}_error.png")

# Function to fill text into an input field
async def fill_input_field(page, input_selector, text_value):
    try:
        await page.wait_for_selector(input_selector, timeout=30000)
        print(f"Input field {input_selector} is visible.")
        await page.fill(input_selector, text_value)
        print(f"Filled text '{text_value}' in the input field.")
    except Exception as e:
        print(f"Error filling input field {input_selector}: {e}")
        await page.screenshot(path="input_field_error.png")

# Main function to automate the workflow
async def main_workflow():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Navigate to the login page
        await page.goto('https://esgbeta.samcorporate.com/auth/login')
        await page.fill('input[name="email"]', "annmariajoseph@samcorporate.com")  # Replace with your email
        await page.fill('input[name="password"]', "123456789")  # Replace with your password
        await verify_and_click_button(page, 'button[type="submit"]')

        # Wait for login to complete and navigate to the upload page
        await page.wait_for_url('**/page/default/data-upload/etl/brsr-reports', timeout=60000)
        await page.goto('https://esgbeta.samcorporate.com/app/ih0w9cralvbmwlou0fo0jgpayrx/page/default/data-upload/etl/brsr-reports')
        await verify_and_click_button(page, 'text=Upload New File')

        # Select month and year for upload
        await select_and_verify_dropdown(page, 'select#fileMonth', "3")  # Select March
        await select_and_verify_dropdown(page, 'select#fileYear', "2023")

        # Upload the file
        file_path = r"C:\Users\DML-LT-36\Desktop\New folder\BRSR-Report_Data-Template custom 2 (4).xlsx"
        await page.set_input_files('input#file[accept=".xlsx, .xls"]', file_path)
        print(f"Uploaded file: {file_path}")
        await verify_and_click_button(page, 'button:text("Upload File")')

        # Map sheets to custom fields
        dropdown_options_list = [
            ("Bus_Prod_Ser_Master", "button[type='submit'][form='fromMappingBusinessProductsServiceMaster']"),
            ("Trans-Prod_Ser", "button[type='submit'][form='fromMappingTransactionProductService']"),
            ("Trans_Emp-Work", "button[type='submit'][form='fromMappingTransactionEmployeeWork']"),
            ("Trans_Financials", "button[type='submit'][form='fromMappingTransactionFinancials']"),
            ("Trans_Trainings", "button[type='submit'][form='fromMappingTransactionTrainings']"),
        ]

        for option, next_button in dropdown_options_list:
            await select_and_verify_dropdown(page, 'select#sheetName', option)
            await verify_and_click_button(page, next_button)

        # Add custom fields
        custom_fields_data = [
            {"custom_field": "custom_field_12", "fo_day": "25", "field_label": "Battery Voltage"},
            {"custom_field": "custom_field_13", "fo_day": "26", "field_label": "Engine RPM"},
            {"custom_field": "custom_field_14", "fo_day": "27", "field_label": "Lub Oil Press."},
        ]

        for field_data in custom_fields_data:
            await verify_and_click_button(page, 'button:has-text("Add New Custom Field")')
            await select_and_verify_dropdown(page, 'select#fieldKey', field_data["custom_field"])
            await select_and_verify_dropdown(page, 'select#columnIndex', field_data["fo_day"])
            await fill_input_field(page, 'input#fieldLabel', field_data["field_label"])
            await verify_and_click_button(page, 'button[type="submit"][form="addEditCustomFieldForm"]')

        # Final validation and import
        await verify_and_click_button(page, 'button:has-text("Validate and Import")')

        # Take a screenshot after completing the process
        screenshot_path = "final_screenshot.png"
        await page.screenshot(path=screenshot_path)
        print("Workflow completed successfully. Screenshot saved.")

        # Close the browser
        await browser.close()

# Streamlit button to trigger the workflow
if st.button("Upload file to the system"):
    st.write("Starting the upload workflow...")
    asyncio.run(main_workflow())
