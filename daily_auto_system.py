import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

if os.getenv("GITHUB_ACTIONS") == "true":
    for flag in ["--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--window-size=1920,1080"]:
        options.add_argument(flag)

driver = webdriver.Chrome(options=options)

driver.get("https://labsafety.jbnu.ac.kr/ushm/main/home.do")
wait = WebDriverWait(driver, 15)

# 연구실안전관리시스템 홈화면에서 로그인 페이지 넘어가기
login = driver.find_element(By.XPATH, "//*[@id='Integration_remote_area_wrap']/div/div/a[4]")
login.click()

wait.until(EC.url_contains("/account/login.do"))

# 로그인
id_locator = (By.CSS_SELECTOR,
              "input#userId:not([type='hidden']):not([disabled]), input[name='userId']:not([type='hidden']):not([disabled])")
pw_locator = (By.CSS_SELECTOR,
              "input#userPwd:not([type='hidden']):not([disabled]), input[name='userName']:not([type='hidden']):not([disabled])")

ID = os.environ.get("ID")
PASSWORD = os.environ.get("PASSWORD")

id_box = wait.until(EC.element_to_be_clickable(id_locator))
pw_box = wait.until(EC.element_to_be_clickable(pw_locator))

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", id_box)
id_box.click(); id_box.clear(); id_box.send_keys(ID)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", pw_box)
pw_box.click(); pw_box.clear(); pw_box.send_keys(PASSWORD)

login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='btnUser']")))
login_btn.click()

# 홈화면에서 일상 점검 페이지 들어가기
daily_test_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main_bg_area_wrap']/div/div[2]/div[1]/ul/li[1]/a")))
daily_test_btn.click()

# 점검 화면 들어가기
test_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='divList']/div[3]/table/tbody/tr/td/p/a[2]")))
test_btn.click()

# 점검
general_check = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='check_tblList']/tbody/tr[1]/th[2]/input")))
electrical_check = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='check_tblList']/tbody/tr[8]/th[2]/input")))
fire_check = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='check_tblList']/tbody/tr[13]/th[2]/input")))
battery_check = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='check_tblList']/tbody/tr[17]/th[2]/input")))

general_check.click()
electrical_check.click()
fire_check.click()
battery_check.click()

save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='frmOn']/div/div[2]/a[1]")))
save_btn.click()