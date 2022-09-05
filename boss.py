import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from openpyxl import load_workbook



import time

s = Service(executable_path=r'./chromedriver.exe')


driver = webdriver.Chrome(service=s)
url = 'https://www.zhipin.com/web/geek/job?query=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&city=101190100&page='

def download(request_url):
    driver.get(url=request_url)
    time.sleep(6)
    driver.implicitly_wait(5)
    html = driver.find_element(By.ID, 'wrap')
    jobnames = html.find_elements(By.XPATH, "//div[@class='job-card-body clearfix']/a[@class='job-card-left']/div[@class='job-title clearfix']/span[@class='job-name']")
    addrs = html.find_elements(By.XPATH, "//div[@class='job-card-body clearfix']/a[@class='job-card-left']/div[@class='job-title clearfix']/span[@class='job-area-wrapper']/span[@class='job-area']")
    salarys = html.find_elements(By.XPATH, "//div[@class='job-card-body clearfix']/a[@class='job-card-left']/div[@class='job-info clearfix']/span[@class='salary']")
    companys = html.find_elements(By.XPATH, "//div[@class='job-card-body clearfix']/div[@class='job-card-right']/div[@class='company-info']/h3[@class='company-name']/a")
    companytags = html.find_elements(By.XPATH, "//div[@class='job-card-body clearfix']/div[@class='job-card-right']/div[@class='company-info']/ul[@class='company-tag-list']/li[1]")
    jobnames1 = []
    addrs1 = []
    salarys1 = []
    companys1 = []
    companytags1 = []
    dess1 = []

    for i in range(len(jobnames)):
        time.sleep(2)
        jobnames1.append(jobnames[i].text)
        addrs1.append(addrs[i].text)
        salarys1.append(salarys[i].text)
        companys1.append(companys[i].text)
        companytags1.append(companytags[i].text)
    df = pd.DataFrame({'jobnames': jobnames1, 'addrs':addrs1, 'salarys': salarys1, 'companys': companys1, 'companytags':companytags1})
    original_data = pd.read_excel('数据分析.xlsx')
    save_data = original_data.append(df)
    # df.to_csv('./HM.csv', mode='a', header=None, index=False, encoding='utf_8_sig')
    save_data.to_excel('数据分析.xlsx', index=False)
    print('总共{0}条数据'.format(len(jobnames)))
    time.sleep(6)


start = 1


for i in range(10):
    print('正在爬取第{0}页'.format(start))
    request_url = url + str(start)
    download(request_url)
    start += 1

print('over')