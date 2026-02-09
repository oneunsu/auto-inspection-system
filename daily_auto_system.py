import os
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

def close_popup(driver):
    popup_btn = (By.XPATH, '//*[@id="Incidentsfooter_myEduPop"]/div[2]/a/input')

    try:
        el = WebDriverWait(driver, 2).until(EC.element_to_be_clickable(popup_btn))
        el.click()
        print("[POPUP] popup dismissed (today)", flush=True)
        return True
    except TimeoutException:
        return False

def mark(code: int, msg: str):
    print(f"[CHECK {code}] {msg}", flush=True)

def fail(code: int, msg: str, err: Exception | None = None, driver: webdriver.Chrome | None = None):
    print(f"::error title=FAILED {code}::{msg}", flush=True)
    if err:
        print(f"[EXCEPTION] {repr(err)}", flush=True)
        tb = "".join(traceback.format_exception(type(err), err, err.__traceback__))
        print(tb, flush=True)

    if driver:
        try:
            print(f"[DEBUG] title={driver.title}", flush=True)
        except Exception:
            pass
    raise

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

if os.getenv("GITHUB_ACTIONS") == "true":
    for flag in ["--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--window-size=1920,1080"]:
        options.add_argument(flag)

    try:
        options.experimental_options["detach"] = False
    except Exception:
        pass

try:
    driver = webdriver.Chrome(options=options)
except WebDriverException as e:
    fail(90, "Chrome 드라이버 초기화 실패", e)

try:
    wait = WebDriverWait(driver, 20)

    # 100: 홈 진입
    try:
        driver.get("https://labsafety.jbnu.ac.kr/ushm/main/home.do")
        mark(100, "홈 페이지 접속")
    except Exception as e:
        fail(101, "홈 페이지 접속 중 오류", e, driver)

    # 110: 로그인 페이지로 이동 클릭
    try:
        login = driver.find_element(By.XPATH, "//*[@id='Integration_remote_area_wrap']/div/div/a[4]")
        login.click()
        mark(110, "로그인 버튼 클릭")
    except NoSuchElementException as e:
        fail(111, "홈에서 로그인 버튼 요소 찾지 못함", e, driver)
    except Exception as e:
        fail(112, "로그인 버튼 클릭 중 오류", e, driver)

    # 120: 로그인 페이지 접속
    try:
        wait.until(EC.url_contains("/account/login.do"))
        mark(120, "로그인 페이지 도착")
    except TimeoutException as e:
        fail(121, "로그인 페이지로 이동하지 않음", e, driver)

    # 130: 로그인 요소
    id_locator = (By.CSS_SELECTOR,
                  "input#userId:not([type='hidden']):not([disabled]), input[name='userId']:not([type='hidden']):not([disabled])")
    pw_locator = (By.CSS_SELECTOR,
                  "input#userPwd:not([type='hidden']):not([disabled]), input[name='userName']:not([type='hidden']):not([disabled])")

    ID = os.environ.get("ID")
    PASSWORD = os.environ.get("PASSWORD")
    if not ID or not PASSWORD:
        fail(135, "환경변수(ID/PASSWORD) 누락 또는 비어 있음", driver=driver)

    # 140: ID/PW 입력
    try:
        id_box = wait.until(EC.element_to_be_clickable(id_locator))
        pw_box = wait.until(EC.element_to_be_clickable(pw_locator))
        mark(140, "ID/PW 입력칸 불러오기")
    except TimeoutException as e:
        fail(141, "ID 또는 PW 입력칸 찾지 못함", e, driver)

    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", id_box)
        id_box.click(); id_box.clear(); id_box.send_keys(ID)

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", pw_box)
        pw_box.click(); pw_box.clear(); pw_box.send_keys(PASSWORD)

        mark(150, "ID/PW 입력 완료")
    except Exception as e:
        fail(151, "ID/PW 입력 중 오류", e, driver)

    # 160: 로그인 버튼 클릭
    try:
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='btnUser']")))
        login_btn.click()
        mark(160, "로그인 버튼 클릭")
        close_popup(driver)
        
    except TimeoutException as e:
        fail(161, "로그인 버튼 찾지 못함", e, driver)
    except Exception as e:
        fail(162, "로그인 버튼 클릭 중 오류", e, driver)

    # 200: 일상 점검 페이지 진입
    try:
        daily_test_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main_bg_area_wrap']/div/div[2]/div[1]/ul/li[1]/a")))
        daily_test_btn.click()
        mark(200, "일상 점검 페이지 진입")
    except TimeoutException as e:
        fail(201, "일상 점검 버튼 찾지 못함", e, driver)
    except Exception as e:
        fail(202, "일상 점검 버튼 클릭 중 오류", e, driver)

    # 210: 점검 화면 진입
    try:
        test_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='divList']/div[3]/table/tbody/tr/td/p/a[2]")))
        test_btn.click()
        mark(210, "점검 화면 들어가기")
    except TimeoutException as e:
        fail(211, "점검 화면 이동 버튼 찾지 못함", e, driver)
    except Exception as e:
        fail(212, "점검 화면 이동 버튼 클릭 중 오류", e, driver)

    # 300: 점검
    try:
        general_check = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='check_tblList']/tbody/tr[1]/th[2]/input")))
        electrical_check = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='check_tblList']/tbody/tr[8]/th[2]/input")))
        fire_check = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='check_tblList']/tbody/tr[13]/th[2]/input")))
        mark(300, "체크박스 찾기")
    except TimeoutException as e:
        fail(304, "체크박스 요소 찾기 실패", e, driver)

    try:
        general_check.click()
        electrical_check.click()
        fire_check.click()
        mark(310, "체크 항목 클릭 완료")
    except Exception as e:
        fail(311, "체크 항목 클릭 중 오류", e, driver)

    # 400: 저장
    try:
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='frmOn']/div/div[2]/a[1]")))
        save_btn.click()
        mark(400, "저장 버튼 클릭 완료")
    except TimeoutException as e:
        fail(401, "저장버튼 찾지 못함", e, driver)
    except Exception as e:
        fail(402, "저장 버튼 클릭 중 오류", e, driver)

    mark(999, "전체 플로우 성공")

finally:
    try:
        driver.quit()
    except Exception:
        pass










