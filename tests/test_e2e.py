from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import uuid

def test_login_page():
    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost:8000/static/frontend/login.html")

        # Fill in username and password
        user_name = driver.find_element(By.ID, "username")
        user_name.send_keys("aa")

        password = driver.find_element(By.ID, "password")
        password.send_keys("securepassword2")

        # Click the login button
        driver.find_element(By.ID, "loginButton").click()

        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.ID, "responseMessage").text.strip() != ""
        )

        # Check the response message
        message = driver.find_element(By.ID, "responseMessage").text
        print("Response message:", message)
        assert "Login successful" in message

    finally:
        driver.quit()

def test_register_page():
    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost:8000/static/frontend/register.html")

        #Use a unique username evrytime the test run
        unique_username = f"user_{uuid.uuid4().hex[:6]}"

        driver.find_element(By.ID, "full_name").send_keys("Test User")
        #driver.find_element(By.ID, "username").send_keys("Testuser")
        #driver.find_element(By.ID, "email").send_keys("Testuser@example.com")
        driver.find_element(By.ID, "username").send_keys(unique_username)
        driver.find_element(By.ID, "email").send_keys(f"{unique_username}@example.com")
        driver.find_element(By.ID, "password").send_keys("securepass123")
        driver.find_element(By.ID, "currency").send_keys("USD")

        # Click the register button
        driver.find_element(By.ID, "registerButton").click()

        # Wait for the response message to be populated
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.ID, "responseMessage").text.strip() != ""
        )

        message = driver.find_element(By.ID, "responseMessage").text
        print("Response message:", message)
        assert "Registration successful" in message

    finally:
        driver.quit()

def test_account_page():
    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost:8000/static/frontend/account.html")

        # Fill in login credentials
        driver.find_element(By.NAME, "username").send_keys("cc")
        driver.find_element(By.NAME, "password").send_keys("securepassword4")

        # Submit the login form
        driver.find_element(By.ID, "loginButton").click()

        # Wait for account section to appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "accountSection"))
        )

        # Verify account info is populated
        account_id = driver.find_element(By.ID, "accountId").text
        balance = driver.find_element(By.ID, "balance").text
        currency = driver.find_element(By.ID, "currency").text

        print("Account ID:", account_id)
        print("Balance:", balance)
        print("Currency:", currency)

        #assert account_id != ""
        #assert balance != ""
        #assert currency in {"USD", "EUR", "GBP"}
        assert account_id == '3'
        assert balance != ""
        assert currency == "EUR"

    finally:
        driver.quit()

def test_transaction_page():
    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost:8000/static/frontend/transactions.html")

        # Login
        driver.find_element(By.NAME, "username").send_keys("bb")
        driver.find_element(By.NAME, "password").send_keys("securepassword3")
        driver.find_element(By.ID, "loginButton").click()

        # Wait for transaction section to appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "transactionSection"))
        )

        # Fill in transaction form
        driver.find_element(By.NAME, "recipient_acc_id").send_keys("4")
        driver.find_element(By.NAME, "amount").send_keys("10")
        driver.find_element(By.ID, "sendButton").click()

        # Wait for success message
        WebDriverWait(driver, 10).until(
            lambda d: "✅ Sent 10." in d.find_element(By.ID, "sendMessage").text
        )

        # Check transaction history
        history_items = driver.find_elements(By.CSS_SELECTOR, "#historyList li")
        assert any("💸 10 USD" in item.text for item in history_items)

        print("Transaction test passed.")

    finally:
        driver.quit()

def test_admin_dashboard():
    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost:8000/static/frontend/admin.html")

        # Login as admin
        driver.find_element(By.NAME, "username").send_keys("Yunis")
        driver.find_element(By.NAME, "password").send_keys("securepassword1")
        driver.find_element(By.ID, "loginButton").click()

        # Wait for admin section to appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "adminSection"))
        )

        # Submit user ID to view transactions
        driver.find_element(By.NAME, "user_id").send_keys("1")
        driver.find_element(By.ID, "viewButton").click()

        # Wait for transaction list to populate
        WebDriverWait(driver, 10).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "#adminHistoryList li")) > 0
        )

        # Check that at least one transaction is there
        items = driver.find_elements(By.CSS_SELECTOR, "#adminHistoryList li")
        assert any("🧾" in item.text for item in items)

        print("Admin dashboard test passed.")

    finally:
        driver.quit()
