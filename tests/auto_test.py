import os
import uuid
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")


def new_user(role="student"):
    unique = uuid.uuid4().hex[:8]
    return {
        "username": f"{role}_{unique}",
        "email":f"{role}_{unique}@placeholder.com",
        "password": f"this_is_a_password",
        "role" : role,
    }
HOME_TITLE = {
    "student": "Student Home",
    "vendor": "Vendor Home",
}

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new") 
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def wait_for_url(driver, url_part, timeout=5):
    WebDriverWait(driver, timeout).until(EC.url_contains(url_part))
    
def wait_for_home(driver, role, timeout=5):
    WebDriverWait(driver, timeout).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), HOME_TITLE[role])
    )

def register(driver, user, skip_browser_validation=True):
    driver.get(f"{BASE_URL}/register")
    if skip_browser_validation:
        driver.execute_script("document.querySelector('form').noValidate = true;")

    driver.find_element(By.NAME, "username").send_keys(user["username"])
    driver.find_element(By.NAME, "email").send_keys(user["email"])
    driver.find_element(By.NAME, "password").send_keys(user["password"])
    Select(driver.find_element(By.NAME, "role")).select_by_value(user["role"])
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

def test_duplicate_reject_login(driver):
    user = new_user("student")
    wait = WebDriverWait(driver, 5)

    register(driver, user)
    wait_for_url(driver, "/login")

    duplicate = {**user, "username": f"dup_{uuid.uuid4().hex[:8]}"}
    register(driver, duplicate)
    warning = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".messages .message[data-category='warning']"))
    )

    assert warning.text == "Email is already registered."
    assert "/register" in driver.current_url

    driver.get(f"{BASE_URL}/login")
    login(driver, user)
    wait_for_home(driver, user["role"])

    
def visual_warning(driver, expected_text, timeout=5):
    return {e.text for e in driver.find_elements(By.CSS_SELECTOR, ".messages .message[data-category='warning']")}


def login(driver, user):
    driver.find_element(By.NAME, "email").send_keys(user["email"])
    driver.find_element(By.NAME, "password").send_keys(user["password"])
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

@pytest.mark.parametrize("role", ["student", "vendor"])
def test_register_and_login(driver, role):
    user = new_user(role)
    wait = WebDriverWait(driver, 5)

    register(driver, user)
    wait_for_url(driver, "/login")

    login(driver, user)
    wait_for_home(driver, role)
               


def missing_field(driver, blank_fields):

    user = new_user("student")
    form_field = {**user, **{f: "" for f in blank_fields}}

    register(driver, form_field)
    expected = {f"{field.capitalize()} is required." for field in blank_fields}
    wait = WebDriverWait(driver, 5)
    warnings = wait.until(
        lambda d: visual_warning(d, expected) == expected
    )
    assert warnings == expected
    assert "/register" in driver.current_url

    register(driver, user)
    wait_for_url(driver, "/login")

    login(driver, user)
    wait_for_home(driver, user["role"])

@pytest.mark.parametrize("blank_fields", [["username"], ["email"], ["password"], ["username", "email", "password"]])
def test_empty_field(driver, blank_fields):
    missing_field(driver, blank_fields)

def test_all_fields_empty(driver):
    missing_field(driver, ["username", "email", "password"])
    

def test_wrong_password(driver):
    user = new_user("student")
    wait = WebDriverWait(driver, 5)

    register(driver, user)
    wait_for_url(driver, "/login")

    login(driver, {**user, "password": "wrongpassword"})
    warning = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".messages .message[data-category='warning']"))
    )
    assert warning.text == "Invalid email/password."
    assert "/login" in driver.current_url
    






