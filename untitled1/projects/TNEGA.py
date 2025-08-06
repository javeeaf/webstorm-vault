from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Auto-handles ChromeDriver with Selenium 4.6+
driver = webdriver.Chrome()

# Step 1: Open TN eSevai
driver.get("https://tnedistrict.tn.gov.in/tneda/out_status.xhtml?outApp=jUcM3vV2nYtbRhhzaXKXqn3XRsltva9Z")
print("🔐 Please log in manually and solve CAPTCHA within 60 seconds...")
time.sleep(60)

# Step 2: Extract Application Status (after you navigate to status page)
try:
    # 👉 Replace this XPath with actual one after inspecting the page
    status_element = driver.find_element(By.XPATH, '//span[@id="statusText"]')
    status = status_element.text
    print("📌 Application Status:", status)

    if "Certificate Issued" in status or "Download" in status:
        print("🎉 Your certificate is ready for download!")
    else:
        print("⏳ Still in progress. Be patient, it's on the way.")

except Exception as e:
    print("❌ Error fetching status:", e)

# Close browser
driver.quit()
