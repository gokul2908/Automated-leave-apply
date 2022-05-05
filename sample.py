from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os.path
from getpass import getpass
import tempfile

db_file = os.path.join(tempfile.gettempdir(),
                             'db.txt')
def get_input():
    try:
        with open(db_file, 'r') as file:
            user = file.readline()
            pwd = file.readline()
    except FileNotFoundError:
        with open(db_file, 'w') as file:
            user = input("Enter emailid")
            pwd = getpass()
            file.write(user+ "\n"+ pwd)
    except: 
        print("failed to read the file")
        return (0, 0)
    return (user.rstrip(),pwd)

user = {}
user["email"], user["password"]  = get_input()
        
from_date = "" 
while len(from_date.split("-"))!=3:
    from_date = input("Enter 'from' Date format(dd-mm-yyyy) : ")
    to_date = input("Press 'enter' if todate=fromdate \nEnter 'to' Date: ")
    if (len(from_date.split("-"))!=3): print("invalid input")

if not to_date: to_date = from_date
    

url = "https://erp.zilogic.com"

def open_browser(url):
    service = Service(executable_path=ChromeDriverManager().install())
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options, service=service)
    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(30)
    assert 'Login' in driver.title
    return driver

def enter_login_details(driver):
    sleep(5)
    try:
        element = driver.find_element(By.ID, "login_email")
        element.send_keys(user["email"])
        element = driver.find_element(By.ID, "login_password")
        element.send_keys(user["password"])
        driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div/div/div/div[2]/section[1]/div[1]/form/button").click()
        sleep(1)
        return True
    except: 
        print("Failed: enter_login_details")
        return False
    

    
def profile(driver):
    sleep(5)
    try:
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/i").click()
        sleep(5)
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[3]/div/div[5]/div[3]/div/div/div[1]/div[1]").click()
        sleep(5)

        driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[3]/div/div/div[2]/div[1]/div[2]/div/div[5]/div/div/div[1]/div[1]/div/button/i").click()
        sleep(5)
        return True
    except: 
        print("Failed: apply_leave")
        return False


def form_input(driver):
    sleep(5)
    try:
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[3]/div/div/div[2]/div[2]/div/div[2]/form/div[1]/div/div[2]/div[1]/div/div/input").send_keys("Casual Leave")

        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[3]/div/div/div[2]/div[3]/div/div[1]/form/div[1]/div/div[2]/div[1]/input").send_keys(from_date)

        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[3]/div/div/div[2]/div[3]/div/div[1]/form/div[2]/div/div[2]/div[1]/input").send_keys(to_date)

        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[3]/div/div/div[2]/div[3]/div/div[2]/form/div/div/div[2]/div[1]/textarea").send_keys("fever")

        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[3]/div/div/div[2]/div[4]/div/div[2]/form/div[1]/div/div[2]/div[1]/div/div/input").send_keys("mohamadfazal@zilogic.com")

        print(f"from: {from_date} \nto: {to_date}")
        sure = input("Enter y/n to apply: ")
        print(sure)
        while True:
            if sure=="y" or sure=="n": break
            print("enter valid input")
            sure = input("Enter y/n to apply: ")

        if sure=="y": 
            driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[1]/div/div/div[2]/button[2]").click() #this will click save
            sleep(5)
            return True
    except: 
        print("Failed: form_input")
        return False
    

driver = open_browser(url)
if (enter_login_details(driver) and profile(driver) and form_input(driver)):
    print("Applied!")
else: 
    print("failed to apply")

# sleep(109)
driver.quit()
