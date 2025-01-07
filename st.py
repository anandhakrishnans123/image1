# import streamlit as st
# import cv2
# from PIL import Image as PILImage
# from img2table.ocr import AzureOCR
# from img2table.document import Image
# import os
# # Azure OCR credentials (replace with your actual key and endpoint)
# subscription_key = "GD6ulmqehKFhHTQRGlXrp9KWFnJw1kraJFLMxBIDLjQMYW4OmpRvJQQJ99ALACYeBjFXJ3w3AAAFACOGdPzx"
# endpoint = "https://imagedataextration.cognitiveservices.azure.com/"

# # Initialize AzureOCR
# azure_ocr = AzureOCR(subscription_key=subscription_key, endpoint=endpoint)

# # Streamlit app
# st.title("Image to Table Extraction")

# st.write("Upload images to extract tables and save them as Excel files.")

# # Function to process images and extract tables
# def process_image(image_path, output_xlsx):
#     # Load the input image
#     img = Image(src=image_path)
#     cv_img = cv2.imread(image_path)

#     # Extract tables using Azure OCR
#     extracted_tables = img.extract_tables(
#         ocr=azure_ocr,
#         implicit_rows=True,
#         borderless_tables=False,
#         min_confidence=30  # Lowering confidence to capture possible tables
#     )

#     if not extracted_tables:
#         st.warning(f"No tables were detected in {image_path}.")
#     else:
#         # Process and display the extracted tables
#         for i, table in enumerate(extracted_tables):
#             st.subheader(f"Extracted Table {i+1}")
#             st.write(table.html_repr(title=f"Table {i+1}"), unsafe_allow_html=True)

#             # Highlight table cells on the image
#             for row in table.content.values():
#                 for cell in row:
#                     cv2.rectangle(cv_img, (cell.bbox.x1, cell.bbox.y1), (cell.bbox.x2, cell.bbox.y2), (255, 0, 0), 2)

#         # Display the image with highlighted table cells
#         st.image(PILImage.fromarray(cv_img), caption="Detected Tables")

#     # Save the extracted table(s) to an Excel file
#     img.to_xlsx(output_xlsx,
#                 ocr=azure_ocr,
#                 implicit_rows=True,
#                 borderless_tables=False,
#                 min_confidence=50)

# # Upload first image
# uploaded_file1 = st.file_uploader("Upload the first image", type=["jpg", "png", "jpeg"])
# if uploaded_file1 is not None:
#     with open("uploaded_file1.jpg", "wb") as f:
#         f.write(uploaded_file1.read())
#     output_xlsx_1 = "diesel1.xlsx"
#     process_image("uploaded_file1.jpg", output_xlsx_1)
#     st.success(f"Tables extracted and saved to {output_xlsx_1}")

# # Upload second image
# uploaded_file2 = st.file_uploader("Upload the second image", type=["jpg", "png", "jpeg"])
# if uploaded_file2 is not None:
#     with open("uploaded_file2.jpg", "wb") as f:
#         f.write(uploaded_file2.read())
#     output_xlsx_2 = "diesel.xlsx"
#     process_image("uploaded_file2.jpg", output_xlsx_2)
#     st.success(f"Tables extracted and saved to {output_xlsx_2}")

# # Install required package if needed
# def install_and_restart(package_name, version=None):
#     if version:
#         os.system(f"pip install {package_name}=={version}")
#     else:
#         os.system(f"pip install {package_name}")

#     st.warning("Installation complete. Please restart the Streamlit app.")

# # Check for OpenCV contrib package
# try:
#     import cv2.ximgproc
# except ImportError:
#     st.warning("OpenCV contrib package not found. Installing now...")
#     install_and_restart('opencv-contrib-python-headless', '4.5.5.62')
# # if st.button("Click"):
    
# import pandas as pd
# import streamlit as st
# from io import BytesIO

# # File paths
# file_path = r"C:\Users\DML-LT-36\Desktop\New folder\BRSR-Report_Data-Template custom.xlsx"

# # Define sheets to modify
# sheets_to_modify = ["Trans_Complaints", "Stakeholders_Master"]

# # Load the Excel file
# excel_data = pd.ExcelFile(file_path)

# # Load all sheets into a dictionary
# all_sheets = {sheet: excel_data.parse(sheet) for sheet in excel_data.sheet_names}

# # Modify each sheet in the list
# for sheet_to_modify in sheets_to_modify:
#     # Load the specific sheet into a DataFrame
#     if sheet_to_modify in excel_data.sheet_names:
#         sheet_data = all_sheets[sheet_to_modify]
#     else:
#         raise ValueError(f"Sheet '{sheet_to_modify}' not found in the Excel file.")

#     # Load the DataFrame to append (use different file paths for different sheets)
#     if sheet_to_modify == "Trans_Complaints":
#         df_to_append = pd.read_excel(r'C:\Users\DML-LT-36\Desktop\New folder\diesel1.xlsx')
#         df_to_append = df_to_append.iloc[:, 2:].reset_index(drop=True)
#         df_to_append.columns = df_to_append.iloc[0]
#         df_to_append = df_to_append.drop([0, 1]).reset_index(drop=True)
#         df_to_append = df_to_append.apply(pd.to_numeric, errors='coerce')
#         df_to_append = df_to_append.dropna(thresh=len(df_to_append) - 2, axis=1)
#     elif sheet_to_modify == "Stakeholders_Master":
#         df_to_append = pd.read_excel(r'C:\Users\DML-LT-36\Desktop\New folder\diesel.xlsx')
#         df_to_append = df_to_append.iloc[:, 3:].reset_index(drop=True)
#         df_to_append = df_to_append.apply(pd.to_numeric, errors='coerce')
#         df_to_append = df_to_append.dropna(thresh=len(df_to_append) - 2, axis=1)

#     # Create a null row with the same columns
#     null_row = pd.DataFrame({col: [None] for col in df_to_append.columns})

#     # Concatenate the null row at the top
#     df_to_append = pd.concat([null_row, df_to_append], ignore_index=True)

#     # Append columns from the other DataFrame
#     modified_data = pd.concat([sheet_data, df_to_append], axis=1)

#     # Update the sheet in the dictionary with the modified data
#     all_sheets[sheet_to_modify] = modified_data
    
# # Save the processed Excel file to memory
# output = BytesIO()
# with pd.ExcelWriter(output, engine="openpyxl") as writer:
#     for sheet_name, data in all_sheets.items():
#         data.to_excel(writer, sheet_name=sheet_name, index=False)
# output.seek(0)

# # Streamlit app to download the file
# st.title("Upload File to system")

# # Download button
# st.download_button(
#     label="Download Processed Excel",
#     data=output,
#     file_name="Processed_BRSR_Report.xlsx",
#     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# )
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
        asyncio.set_event_loop(loop)
        title = loop.run_until_complete(main())
        print(title)
