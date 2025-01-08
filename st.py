import streamlit as st
import asyncio
from playwright.async_api import async_playwright
import time
#------------------------------------------------------------------------------------------------------------------------------


async def verify_and_click_add_custom_field(page):
    try:
        button_selector = 'button:has-text("Add New Custom Field")'
        await page.wait_for_selector(button_selector, timeout=30000)
        print("Button 'Add New Custom Field' is visible.")
        await page.click(button_selector)
        print("Clicked the 'Add New Custom Field' button.")
    except Exception as e:
        print(f"Error verifying or clicking 'Add New Custom Field' button: {e}")
        await page.screenshot(path="add_custom_field_button_error.png")
async def select_and_verify_dropdown(page, dropdown_selector, option_value):
    try:
        await page.wait_for_selector(dropdown_selector, timeout=30000)
        print(f"Dropdown {dropdown_selector} is visible.")
        await page.select_option(dropdown_selector, value=option_value)
        print(f"Selected option {option_value} from the dropdown.")
    except Exception as e:
        print(f"Error selecting dropdown: {e}")
        await page.screenshot(path=f"{dropdown_selector}_error.png")
async def select_custom_field_option(page,feild_num):
    try:
        dropdown_selector = 'select#fieldKey'
        await select_and_verify_dropdown(page, dropdown_selector, feild_num)
    except Exception as e:
        print(f"Error selecting custom field option: {e}")

# Function to select "FO_day" from dropdown
async def select_fo_day_option(page,number):
    try:
        dropdown_selector = 'select#columnIndex'
        await select_and_verify_dropdown(page, dropdown_selector, number)  # "9" corresponds to "FO_day"
    except Exception as e:
        print(f"Error selecting FO_day option: {e}")

# Function to fill text into the "fieldLabel" input field
async def fill_field_label(page, text_value):
    try:
        input_selector = 'input#fieldLabel'
        await page.wait_for_selector(input_selector, timeout=30000)
        print(f"Field label input is visible.")
        await page.fill(input_selector, text_value)
        print(f"Filled text '{text_value}' in the input field.")
    except Exception as e:
        print(f"Error filling field label input: {e}")
        await page.screenshot(path="field_label_input_error.png")
#---------------------------------------------------------------------------------------------------------------------------------
if st.button("Upload file to the system"):
# Streamlit output
    st.write("Starting the test…")

    # Define the login and file upload function
    async def main():
        async with async_playwright() as p:
            # Launch the browser with visibility
            browser = await p.chromium.launch(headless=False)  # This will open the browser so you can see what's happening
            page = await browser.new_page()
            
            # Clear cookies before starting
            await page.context.clear_cookies()
            
            # Navigate to the website login page
            await page.goto('https://esgbeta.samcorporate.com/auth/login')
            
            # Wait for the "Login" button and click it
            await page.wait_for_selector('text=Login', timeout=60000)
            await page.click('text=Login')
            
            # Wait for the login page to load completely
            await page.wait_for_url('**/login', timeout=60000)
            
            # Fill in the login credentials (replace with actual values)
            email = "annmariajoseph@samcorporate.com"  # Replace with actual email
            password = "123456789"  # Replace with actual password
            
            # Fill in the email and password fields
            await page.fill('input[name="email"]', email)
            await page.fill('input[name="password"]', password)
            
            # Click the submit button to log in
            await page.click('button[type="submit"]')
            
            # Wait for the page to load after login
            await page.wait_for_load_state('load', timeout=60000)  # Wait for the page to finish loading
            await asyncio.sleep(20)
            
            # Navigate to the target page after logging in
            target_url = 'https://esgbeta.samcorporate.com/app/ih0w9cralvbmwlou0fo0jgpayrx/page/default/data-upload/etl/brsr-reports'
            await page.goto(target_url)
            
            # Wait for the target page to load completely
            await page.wait_for_load_state('load', timeout=60000)
            await page.wait_for_selector('text=Upload New File', timeout=30000)
            await page.click('text=Upload New File')
            
            # Select the month and year for the file upload
            await page.wait_for_selector('select#fileMonth', timeout=30000)
            await page.select_option('select#fileMonth', value="3")  # Select March
            await page.wait_for_selector('select#fileYear', timeout=30000)
            await page.select_option('select#fileYear', value="2023")
            file_path = r"C:\Users\DML-LT-36\Desktop\New folder\BRSR-Report_Data-Template custom 2 (4).xlsx"
            file_input_selector = 'input#file[accept=".xlsx, .xls"]'
            await page.wait_for_selector(file_input_selector, timeout=30000)
            file_input = await page.query_selector(file_input_selector)
            if file_input:
                await file_input.set_input_files(file_path)
                print(f"Uploaded file: {file_path}")
            
            await page.click('button:text("Upload File")')
            dropdown_options_list = [
                ("Bus_Prod_Ser_Master", "button[type='submit'][form='fromMappingBusinessProductsServiceMaster']"),
                ("Trans-Prod_Ser", "button[type='submit'][form='fromMappingTransactionProductService']"),
                ("Trans_Emp-Work", "button[type='submit'][form='fromMappingTransactionEmployeeWork']"),
                ("Trans_Financials", "button[type='submit'][form='fromMappingTransactionFinancials']"),
                ("Trans_Trainings", "button[type='submit'][form='fromMappingTransactionTrainings']"),

            ]

            for option, next_button in dropdown_options_list:
                await select_and_verify_dropdown(page, 'select#sheetName', option)
                await page.click(next_button)
            await select_and_verify_dropdown(page, 'select#sheetName', 'Trans_Complaints')
            
            # Verify and click "Add New Custom Field" button
            custom_fields_data = [
    {"custom_field": "custom_field_12", "fo_day": "25", "field_label": "Battery Voltage"},
    {"custom_field": "custom_field_13", "fo_day": "26", "field_label": "Engine RPM"},
    {"custom_field": "custom_field_14", "fo_day": "27", "field_label": "Lub Oil Press."},
    {"custom_field": "custom_field_15", "fo_day": "28", "field_label": "Engine Hour Meter Reading"},
    {"custom_field": "custom_field_16", "fo_day": "29", "field_label": "Voltage"},
    {"custom_field": "custom_field_7", "fo_day": "30", "field_label": "Frequency (Hz)"},
    {"custom_field": "custom_field_8", "fo_day": "31", "field_label": "KW"},
    {"custom_field": "custom_field_9", "fo_day": "32", "field_label": "Energy Meter Reading (KWH)"},
    {"custom_field": "custom_field_10", "fo_day": "33", "field_label": "Consumption In Ltr"}
]
            # # Click the upload button
            # await asyncio.sleep(5)
            for field_data in custom_fields_data:
                await verify_and_click_add_custom_field(page)
                await select_custom_field_option(page, field_data["custom_field"])
                await select_fo_day_option(page, field_data["fo_day"])
                await fill_field_label(page, field_data["field_label"])
                button_selector = 'button[type="submit"][form="addEditCustomFieldForm"]'
                await page.wait_for_selector(button_selector, timeout=30000)
                # print("Button 'Add Custom Field' is visible.")
                await page.click(button_selector)
            await page.click("button[type='submit'][form='fromMappingTransactionComplaints']")
            await select_and_verify_dropdown(page, 'select#sheetName', 'Stakeholders_Master')
            custom_fields_data = [
    {"custom_field": "custom_field_12", "fo_day": "9", "field_label": "Soft water in (liter)"},
    {"custom_field": "custom_field_13", "fo_day": "10", "field_label": "Condensate recovery (liter)"},
    {"custom_field": "custom_field_14", "fo_day": "11", "field_label": "Total water Consumption"},
    {"custom_field": "custom_field_15", "fo_day": "12", "field_label": "Total steam generation in Kg"},
    {"custom_field": "custom_field_7", "fo_day": "13", "field_label": "FO day tank level cm"},
    {"custom_field": "custom_field_8", "fo_day": "14", "field_label": "FO consumption in kg"},
    {"custom_field": "custom_field_9", "fo_day": "15", "field_label": "Ratio (Steam / FO)"}
]
            # Wait for a moment before taking a screenshot
            # await asyncio.sleep(4)
            for field_data in custom_fields_data:
                await verify_and_click_add_custom_field(page)
                await select_custom_field_option(page, field_data["custom_field"])
                await select_fo_day_option(page, field_data["fo_day"])
                await fill_field_label(page, field_data["field_label"])
                button_selector = 'button[type="submit"][form="addEditCustomFieldForm"]'
                await page.wait_for_selector(button_selector, timeout=30000)
                # print("Button 'Add Custom Field' is visible.")
                await page.click(button_selector)
            await page.click('button[type="submit"][form="fromMappingStakeholderMasters"]')
            validate_button_selector = 'button:has-text("Validate and Import")'
            await page.wait_for_selector(validate_button_selector, timeout=30000)
            # print("Button 'Validate and Import' is visible.")
            await page.click(validate_button_selector)
            # print("Clicked the 'Validate and Import' button.")
            # Take a screenshot after uploading the file
            screenshot_path = "upload_screenshot.png"
            await page.screenshot(path=screenshot_path)  # Save the screenshot as an image file
            
            # Optionally, display the screenshot in Streamlit
            st.image(screenshot_path)

            # Optionally, check if the target page loaded successfully by checking the title or specific element
            title = await page.title()
            st.write(title)
            
            # Wait before closing the browser
            await asyncio.sleep(5)  # Wait for 5 seconds before closing the browser
            
            # Close the browser
            await browser.close()
            return title


    # Run the async function
    if __name__ == '__main__':
        loop = asyncio.ProactorEventLoop()
        asyncio.run(main())
        title = loop.run_until_complete(main())
        print(title)
    st.write("hy")
