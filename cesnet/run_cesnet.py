from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import json

url = 'https://hub.cloud.e-infra.cz/hub/home'

# read config
with open('config.json') as json_file:
    config = json.load(json_file)

# set options
AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1920x1080")
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-gpu')
opts.add_argument("user-agent={0}".format(AGENT))

# set driver
driver = webdriver.Chrome(options=opts)
driver.minimize_window
driver.get(url)

# login
element = driver.find_element("xpath", "//a[@role='button']")
driver.execute_script("arguments[0].click();", element)

time.sleep(2)

# try again if the element was nout found
while True:
    try:
        element = driver.find_element(
            "xpath", "//div[@title='Brno University of Technology']")
        driver.execute_script("arguments[0].click();", element)
        break
    except:
        time.sleep(2)

# add vut login into input field based on the name LDAPlogin
driver.find_element(
    "xpath", "//input[@name='LDAPlogin']").send_keys(config['vutlogin'])
# add vut password into input field
driver.find_element(
    "xpath", "//input[@name='LDAPpasswd']").send_keys(config['vutpassword'])

element = driver.find_element("xpath", "//button[@name='login']")
driver.execute_script("arguments[0].click();", element)

time.sleep(2)

try:
    element = driver.find_element("xpath", "//button[@id='yesbutton']")
    driver.execute_script("arguments[0].click();", element)
except:
    pass

time.sleep(5)

element = driver.find_element(
    "xpath", f"//a[@id='start-{config['server_name']}']")
driver.execute_script("arguments[0].click();", element)

time.sleep(2)

# select properties
# select image from dropdown
select = Select(driver.find_element("xpath", "//select[@name='dockerimage']"))
select.select_by_visible_text(config['image'])

# select persisten home type
select = Select(driver.find_element("xpath", "//select[@id='sphid']"))
select.select_by_visible_text('Existing')

select = Select(driver.find_element("xpath", "//select[@id='phid']"))
select.select_by_visible_text(config['home'])

# select number of CPU but replace old value
driver.find_element("xpath", "//input[@id='cpuselection']").clear()
driver.find_element(
    "xpath", "//input[@id='cpuselection']").send_keys(config['cpu'])

select = Select(driver.find_element("xpath", "//select[@name='memselection']"))
select.select_by_visible_text(str(config['ram']))

select = Select(driver.find_element("xpath", "//select[@id='gpuid']"))
select.select_by_visible_text(config['gpu'])

element = driver.find_element("xpath", f"//input[@value='Start']")
driver.execute_script("arguments[0].click();", element)

driver.quit()
