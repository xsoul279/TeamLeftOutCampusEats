import uuid
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


BASE_URL = "http://127.0.0.1:5000"

def new_User(role="student"):
    unique = uuid.uuid4().hex[:8]
    return {
        "username": f"{role}_{unique}",
        "email":f"{role}_{unique}@placeholder.com",
        "password": f"this_is_a_password",
        "role" : role,
    }

def registration(driver, user, skip_browser_validation=True):
    driver.get(f"{BASE_URL}/register")
    if skip_browser_validation:
        driver.execute_script("document.querySelector('form).noValidate = true;")
        driver.find_element(By.NAME, "username").send_keys(user["username"])
        driver.find_element(By.NAME, "email").send_keys(user["email"])
        driver.find_element(By.NAME, "password").send_keys(user["password"])
        Select(driver.find_element(By.NAME, "role")).select_by_value(user["role"])
    

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new") 
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_register_and_login_student(driver):
    unique = uuid.uuid4().hex[:8]
    email = f"testing_{unique}@placeholder.com"
    

    driver.get(f"{BASE_URL}/register")
    driver.find_element(By.NAME, "username").send_keys(f"user_{unique}")
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys("holder_of_place8")
    driver.find_element(By.NAME, "role").send_keys("student")
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

    assert "/login" in driver.current_url

    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys("holder_of_place8")
    driver.find_element(By.CSS_SELECTOR, "buttom[type=submit]").click()

    assert "/home" in driver.current_url


def test_register_and_login_vendor(driver):
    unique = uuid.uuid4().hex[:8]
    email = f"test_{unique}@workinprogress.com"
    

    driver.get(f"{BASE_URL}/register")
    driver.find_element(By.NAME, "username").send_keys(f"user_{unique}")
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys("this_is_a_password")
    driver.find_element(By.NAME, "role").send_keys("vendor")
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

    assert "/login" in driver.current_url

    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys("this_is_a_password")
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

    assert "/home" in driver.current_url


