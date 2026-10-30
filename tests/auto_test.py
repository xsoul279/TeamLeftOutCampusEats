import os
import uuid
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = os.environ.get("BASE_URL", "https://localhost:5000")


def new_user(role="student"):
    unique = uuid.uuid4().hex[:8]
    return {
        "username": f"{role}_{unique}",
        "email":f"{role}_{unique}@placeholder.com",
        "password": f"this_is_a_password",
        "role" : role,
    }

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new") 
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def register(driver, user, skip_browser_validation=True):
    driver.get(f"{BASE_URL}/register")
    if skip_browser_validation:
        driver.execute_script("document.querySelector('form').noValidate = true;")

    driver.find_element(By.NAME, "username").send_keys(user["username"])
    driver.find_element(By.NAME, "email").send_keys(user["email"])
    driver.find_element(By.NAME, "password").send_keys(user["password"])
    Select(driver.find_element(By.NAME, "role")).select_by_value(user["role"])
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

def duplicate_reject_login():
    user = new_user("student")
    wait = WebDriverWait(driver, 5)

    register(driver, user)
    wait.until(EC.url_contains("/login"))

    duplicate = {**user, "username": f"dup_{uuid.uuid4().hex[:8]}"}
    register(driver, duplicate)
    warning = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".messages .message[data-category='warning]"))
    )

    assert warning.text == "Email is already registered."
    assert "/register" in driver.current_url

    driver.get(f"{BASE_URL}/login")
    login(driver, user)
    wait.until(EC.url_contains("/home"))
    


def login(driver, user):
    driver.find_element(By.NAME, "email").send_keys(user["email"])
    driver.find_element(By.NAME, "password").send_keys(user["password"])
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

@pytest.mark.parametrize("role", ["student", "vendor"])
def test_register_and_login(driver, role):
    user = new_user(role)
    wait = WebDriverWait(driver, 5)

    register(driver, user)
    wait.until(EC.url_contains("/login"))

    login(driver, user)
    wait.until(EC.url_contains("/home"))






