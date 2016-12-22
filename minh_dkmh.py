import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
# import winsound
Freq = 2500 # Set Frequency To 2500 Hertz
Dur = 100000 # Set Duration To 1000 ms == 1 second
# Create a new instance of the Firefox driver
driver = webdriver.Firefox()
url = 'http://dangkyhoc.daotao.vnu.edu.vn/dang-nhap'
url2 = 'http://dangkyhoc.daotao.vnu.edu.vn/dang-ky-mon-hoc-nganh-1/'
username = 15020907
password = 'deadp00l'
while(True):
    driver.get(url)
    usernameInput = driver.find_element_by_id('LoginName')
    passwordInput = driver.find_element_by_id('Password')

    usernameInput.send_keys(username)
    passwordInput.send_keys(password)
    driver.find_element_by_class_name("icon-signin").click()
    try:
        driver.find_element_by_class_name('icon-signout')
    except:
         continue

    driver.get(url2)
    try:
        element = WebDriverWait(driver, 10000).until(
            EC.presence_of_element_located((By.CLASS_NAME, "conflict"))
        )
    finally:
        pass
    try:
        # subjectCode = driver.find_element_by_xpath(""".//*[@id='divDSDK']/table/tbody/tr[51]/td[1]/input""") #chuyen nghiep
        subjectCode = driver.find_element_by_xpath(""".//*[@id='divDSDK']/table/tbody/tr[267]/td[1]/input""") #toi uu
        subjectCodeText = subjectCode.click()
        driver.find_element_by_xpath(""".//*[@id='registration-container']/div[2]/div/div[3]/button""").click()
        # print subjectCodeText
        # time.sleep(10000)
        # winsound.Beep(Freq, Dur)
    except:
        print ''