import json
from selenium import webdriver
#创建驱动
def create_chrmoe_driver(*,headless = False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
#伪装模拟器反爬去
    options.add_experimental_option("excludeSwitches",['enable-automation'])
    options.add_experimental_option("useAutomationExtension",False)
    driver = webdriver.Chrome(options=options)
    with open('/Users/huanghanhua/PycharmProjects/django_house_term/lianjia/stealth.min.js') as f:
        js = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })

    # driver.execute_cdp_cmd(
    #     'Page.addScripToEvaluateOnNewDocument',
    #     {'source':'Object.defineProperty(navigator,"webdriver",{get:() => undefined})'}
    # )
    return driver

  #添加cookie
def add_cookies(driver,cookie_file):
    with open (cookie_file,"r") as file:
        cookie_list = json.load(file)
        for cookie_dict in cookie_list:
            if cookie_dict['secure']:
                driver.add_cookie(cookie_dict)

driver = create_chrmoe_driver()
driver.get(url="https://gz.lianjia.com/ershoufang/")
driver.close()