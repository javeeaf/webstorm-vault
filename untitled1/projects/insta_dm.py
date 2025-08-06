from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

USERNAME = "javee_af"
PASSWORD = "Nafila@00965"
MAX_DELETE = 5

mobile_emulation = {
    "deviceName": "Pixel 2"
}

chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

# Step 1: Login
driver.get("https://www.instagram.com/accounts/login/")
wait.until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys(USERNAME)
driver.find_element(By.NAME, 'password').send_keys(PASSWORD)
driver.find_element(By.NAME, 'password').submit()

print("🔐 Logging in...")
time.sleep(6)

# Step 2: Bypass popups
try:
    not_now = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]")))
    not_now.click()
except:
    pass
time.sleep(3)

# Step 3: Go to messages
driver.get("https://www.instagram.com/direct/inbox/")
time.sleep(4)

# Step 4: Delete chats
try:
    chats = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/direct/t/')]")))
    print(f"💬 Found {len(chats)} chats.")
except:
    print("⚠️ No chats found.")
    driver.quit()
    exit()

for i in range(min(MAX_DELETE, len(chats))):
    try:
        chats[i].click()
        time.sleep(2)

        # Click 3-dot menu
        menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][@aria-label='Conversation information']")))
        menu.click()
        time.sleep(1)

        delete_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Delete')]")))
        delete_btn.click()
        time.sleep(1)

        confirm = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Delete']")))
        confirm.click()
        print(f"✅ Deleted chat {i+1}")
        time.sleep(3)
        driver.get("https://www.instagram.com/direct/inbox/")
        time.sleep(3)

    except Exception as e:
        print(f"⚠️ Couldn’t delete chat {i+1}: {e}")
        driver.get("https://www.instagram.com/direct/inbox/")
        time.sleep(3)
        continue

print("🏁 Done.")
driver.quit()
