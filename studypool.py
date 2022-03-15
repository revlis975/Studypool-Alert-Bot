from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import ssl
import telegram_send

from win10toast import ToastNotifier
toaster = ToastNotifier()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--output=/dev/null")


driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.studypool.com/questions/newest#")

account = '//*[@id="root"]/div/div/span[1]/div/div[1]/div[2]/div[2]/a'
username_input = '//*[@id="overlays"]/div[5]/div/div[2]/form/div[1]/div[1]/div[1]/label/div/input'
password_input = '//*[@id="overlays"]/div[5]/div/div[2]/form/div[1]/div[1]/div[2]/label/div[1]/input'
login_submit = '//*[@id="overlays"]/div[5]/div/div[2]/form/div[1]/button/span'


WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="navbar-main"]/div/ul/li[5]/a'))).click()
time.sleep(0.5)


# TODO 
# Add your own Email and Password into the next two lines where prompted
driver.find_element_by_css_selector("input[name='UserLogin[username]']").send_keys("Enter Email")
driver.find_element_by_css_selector("input[name='UserLogin[password]']").send_keys("Enter Password")
time.sleep(0.5)
driver.find_element_by_css_selector("input[id='login-button']").click()
time.sleep(2)
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="containerNav"]/div[1]/ul/li[3]/a/div'))).click()
time.sleep(2)

#turns off alert sound
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="alert-row"]/div[2]/div[1]/div/div'))).click()

#Adds Computer Science and Programming filter (Comment out if not required)
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="priority-filters-row"]/div[2]/div/div/div[3]/div'))).click()
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="priority-filters-row"]/div[2]/div/div/div[11]/div'))).click()

WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="selected-filters-row"]/div/div[2]/div'))).click()

cat = []
cat1 = ''
while True:
    time.sleep(3)
    ques_table = driver.find_elements_by_xpath('//div[@class="question-list-entry"]')
    print("\n\n--------------------------------------\n\nSUBJECTS ARE AS FOLLOWS\n\n")
    l = len(ques_table)
    # print(f'\n l = {l}\n')
    cat = []
    for ques in ques_table:
        try:
            description = ques.find_element_by_css_selector(".category-name")
            cat.append(description.text+' | ')
            print(description.text)
        except:
            print("No description.")
    
    toaster.show_toast("New Question Alert",cat1.join(cat), duration = 20, threaded = True,)
    telegram_send.send(messages=[cat1.join(cat)])

    time.sleep(10)
    driver.refresh()
    time.sleep(5)
    ques_table = driver.find_elements_by_xpath('//div[@class="question-list-entry"]')
    i=0
    list = []
    list.extend([0,0,0])
    while(len(ques_table)<=l):
        if(i==3):
            i=0
            list = []
            list.extend([0,0,0])
        time.sleep(20)
        ques_table = driver.find_elements_by_xpath('//div[@class="question-list-entry"]')
        
        list[i] = len(ques_table)
        if(list[1]>list[0] or (list[0]==list[1] and list[1]<list[2])):
            break

        i=i+1
        
        driver.refresh()


